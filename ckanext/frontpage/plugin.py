import logging
from pylons import config
import ckan.plugins.toolkit as toolkit
ignore_missing = toolkit.get_validator('ignore_missing')

import ckan.plugins as p
import ckan.lib.helpers as h
import actions
import auth

if p.toolkit.check_ckan_version(min_version='2.5'):
    from ckan.lib.plugins import DefaultTranslation

    class FrontpagePluginBase(p.SingletonPlugin, DefaultTranslation):
        p.implements(p.ITranslation, inherit=True)
else:
    class FrontpagePluginBase(p.SingletonPlugin):
        pass

log = logging.getLogger(__name__)

def build_frontpage_nav_main(*args):

    about_menu = p.toolkit.asbool(config.get('ckanext.frontpage.about_menu', True))
    group_menu = p.toolkit.asbool(config.get('ckanext.frontpage.group_menu', True))
    org_menu = p.toolkit.asbool(config.get('ckanext.frontpage.organization_menu', True))

    new_args = []
    for arg in args:
        if arg[0] == 'about' and not about_menu:
            continue
        if arg[0] == 'organizations_index' and not org_menu:
            continue
        if arg[0] == 'group_index' and not group_menu:
            continue
        new_args.append(arg)

    output = h.build_nav_main(*new_args)

    # do not display any private datasets in menu even for sysadmins
    frontpage_list = p.toolkit.get_action('ckanext_frontpage_list')(None, {'order': True, 'private': False})

    page_name = ''

    if (p.toolkit.c.action in ('frontpage_show', 'blog_show')
       and p.toolkit.c.controller == 'ckanext.frontpage.controller:FrontpageController'):
        page_name = p.toolkit.c.environ['routes.url'].current().split('/')[-1]

    for page in frontpage_list:
        if page['page_type'] == 'blog':
            link = h.literal('<a href="/blog/%s">%s</a>' % (str(page['name']), str(page['title'])))
        else:
            link = h.literal('<a href="/frontpage/%s">%s</a>' % (str(page['name']), str(page['title'])))

        if page['name'] == page_name:
            li = h.literal('<li class="active">') + link + h.literal('</li>')
        else:
            li = h.literal('<li>') + link + h.literal('</li>')
        output = output + li

    return output


def render_content(content):
    allow_html = p.toolkit.asbool(config.get('ckanext.frontpage.allow_html', False))
    try:
        return h.render_markdown(content, allow_html=allow_html)
    except TypeError:
        # allow_html is only available in CKAN >= 2.3
        return h.render_markdown(content)


def get_wysiwyg_editor():
    return config.get('ckanext.frontpage.editor', '')


def get_recent_blog_posts(number=5, exclude=None):
    blog_list = p.toolkit.get_action('ckanext_frontpage_list')(
        None, {'order_publish_date': True, 'private': False,
               'page_type': 'blog'}
    )
    new_list = []
    for blog in blog_list:
        if exclude and blog['name'] == exclude:
            continue
        new_list.append(blog)
        if len(new_list) == number:
            break

    return new_list


def get_frontpage_content(page_type='page', page=None ):
    page_content = p.toolkit.get_action('ckanext_frontpage_show')(
        None, {'page_type': page_type, 'page': page}
    )

    return page_content


class FrontpagePlugin(FrontpagePluginBase):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)


    def update_config(self, config):
        self.organization_frontpage = p.toolkit.asbool(config.get('ckanext.frontpage.organization', False))
        self.group_frontpage = p.toolkit.asbool(config.get('ckanext.frontpage.group', False))

        p.toolkit.add_template_directory(config, 'theme/templates_main')
        if self.group_frontpage:
            p.toolkit.add_template_directory(config, 'theme/templates_group')
        if self.organization_frontpage:
            p.toolkit.add_template_directory(config, 'theme/templates_organization')

        p.toolkit.add_resource('fanstatic', 'frontpage')
        p.toolkit.add_public_directory(config, 'public')

        p.toolkit.add_resource('theme/public', 'ckanext-frontpage')
        p.toolkit.add_resource('theme/resources', 'frontpage-theme')
        p.toolkit.add_public_directory(config, 'theme/public')

    def configure(self, config):
        return

    def get_helpers(self):
        return {
            'build_nav_main': build_frontpage_nav_main,
            'render_content': render_content,
            'get_wysiwyg_editor': get_wysiwyg_editor,
            'get_recent_blog_posts': get_recent_blog_posts,
            'get_frontpage_content': get_frontpage_content
        }

    def after_map(self, map):
        controller = 'ckanext.frontpage.controller:FrontpageController'

        if self.organization_frontpage:
            map.connect('organization_frontpage_delete', '/organization/frontpage_delete/{id}{page:/.*|}',
                        action='org_delete', ckan_icon='delete', controller=controller)
            map.connect('organization_frontpage_edit', '/organization/frontpage_edit/{id}{page:/.*|}',
                        action='org_edit', ckan_icon='edit', controller=controller)
            map.connect('organization_frontpage_index', '/organization/frontpage/{id}',
                        action='org_show', ckan_icon='file', controller=controller, highlight_actions='org_edit org_show', page='')
            map.connect('organization_frontpage', '/organization/frontpage/{id}{page:/.*|}',
                        action='org_show', ckan_icon='file', controller=controller, highlight_actions='org_edit org_show')

        if self.group_frontpage:
            map.connect('group_frontpage_delete', '/group/frontpage_delete/{id}{page:/.*|}',
                        action='group_delete', ckan_icon='delete', controller=controller)
            map.connect('group_frontpage_edit', '/group/frontpage_edit/{id}{page:/.*|}',
                        action='group_edit', ckan_icon='edit', controller=controller)
            map.connect('group_frontpage_index', '/group/frontpage/{id}',
                        action='group_show', ckan_icon='file', controller=controller, highlight_actions='group_edit group_show', page='')
            map.connect('group_frontpage', '/group/frontpage/{id}{page:/.*|}',
                        action='group_show', ckan_icon='file', controller=controller, highlight_actions='group_edit group_show')


        map.connect('frontpage_delete', '/frontpage_delete{page:/.*|}',
                    action='frontpage_delete', ckan_icon='delete', controller=controller)
        map.connect('frontpage_edit', '/frontpage_edit{page:/.*|}',
                    action='frontpage_edit', ckan_icon='edit', controller=controller)
        map.connect('frontpage_index', '/frontpage',
                    action='frontpage_index', ckan_icon='file', controller=controller, highlight_actions='frontpage_edit frontpage_index frontpage_show')
        map.connect('frontpage_show', '/frontpage{page:/.*|}',
                    action='frontpage_show', ckan_icon='file', controller=controller, highlight_actions='frontpage_edit frontpage_index frontpage_show')
        map.connect('frontpage_upload', '/frontpage_upload',
                    action='frontpage_upload', controller=controller)

        map.connect('blog_delete', '/blog_delete{page:/.*|}',
                    action='blog_delete', ckan_icon='delete', controller=controller)
        map.connect('blog_edit', '/blog_edit{page:/.*|}',
                    action='blog_edit', ckan_icon='edit', controller=controller)
        map.connect('blog_index', '/blog',
                    action='blog_index', ckan_icon='file', controller=controller, highlight_actions='blog_edit blog_index blog_show')
        map.connect('blog_show', '/blog{page:/.*|}',
                    action='blog_show', ckan_icon='file', controller=controller, highlight_actions='blog_edit blog_index blog_show')
        return map


    def get_actions(self):
        actions_dict = {
            'ckanext_frontpage_show': actions.frontpage_show,
            'ckanext_frontpage_update': actions.frontpage_update,
            'ckanext_frontpage_delete': actions.frontpage_delete,
            'ckanext_frontpage_list': actions.frontpage_list,
            'ckanext_frontpage_upload': actions.frontpage_upload,
        }
        if self.organization_frontpage:
            org_actions={
                'ckanext_org_frontpage_show': actions.org_frontpage_show,
                'ckanext_org_frontpage_update': actions.org_frontpage_update,
                'ckanext_org_frontpage_delete': actions.org_frontpage_delete,
                'ckanext_org_frontpage_list': actions.org_frontpage_list,
            }
            actions_dict.update(org_actions)
        if self.group_frontpage:
            group_actions={
                'ckanext_group_frontpage_show': actions.group_frontpage_show,
                'ckanext_group_frontpage_update': actions.group_frontpage_update,
                'ckanext_group_frontpage_delete': actions.group_frontpage_delete,
                'ckanext_group_frontpage_list': actions.group_frontpage_list,
            }
            actions_dict.update(group_actions)
        return actions_dict

    def get_auth_functions(self):
        return {
            'ckanext_frontpage_show': auth.frontpage_show,
            'ckanext_frontpage_update': auth.frontpage_update,
            'ckanext_frontpage_delete': auth.frontpage_delete,
            'ckanext_frontpage_list': auth.frontpage_list,
            'ckanext_frontpage_upload': auth.frontpage_upload,
            'ckanext_org_frontpage_show': auth.org_frontpage_show,
            'ckanext_org_frontpage_update': auth.org_frontpage_update,
            'ckanext_org_frontpage_delete': auth.org_frontpage_delete,
            'ckanext_org_frontpage_list': auth.org_frontpage_list,
            'ckanext_group_frontpage_show': auth.group_frontpage_show,
            'ckanext_group_frontpage_update': auth.group_frontpage_update,
            'ckanext_group_frontpage_delete': auth.group_frontpage_delete,
            'ckanext_group_frontpage_list': auth.group_frontpage_list,
       }

class TextBoxView(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)

    def update_config(self, config):
        p.toolkit.add_resource('textbox/theme', 'textbox')
        p.toolkit.add_template_directory(config, 'textbox/templates')

    def info(self):
        schema = {
            'content': [ignore_missing],
        }

        return {'name': 'wysiwyg',
                'title': 'Free Text',
                'icon': 'pencil',
                'iframed': False,
                'schema': schema,
                }

    def can_view(self, data_dict):
        return True

    def view_template(self, context, data_dict):
        return 'textbox_view.html'

    def form_template(self, context, data_dict):
        return 'textbox_form.html'

    def setup_template_variables(self, context, data_dict):
        return