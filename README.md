ckanext-frontpage
=============

This extension gives you an easy way to add simple frontpage to CKAN.

By default you can add frontpage to the main CKAN menu.

Works for ckan>=2.3

## Installation

Use `pip` to install this plugin. This example installs it in `/home/www-data/pyenv`, assuming you have [setup a virtualenv](http://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html#install-ckan-into-a-python-virtual-environment) there:

```
source /home/www-data/pyenv/bin/activate
pip install -e 'git+https://github.com/ckan/ckanext-frontpage.git#egg=ckanext-frontpage'
```

Make sure to add `frontpage` to `ckan.plugins` in your config file:

```
ckan.plugins = frontpage
```

## Configuration


Extra config options allow you to control the creation of extra frontpage against groups and organizations.

To swich on this behaviour, to your config add:

```
ckanext.frontpage.organization = True
ckanext.frontpage.group = True
```

These options are False by default and this feature is experimental.


This module also gives you a quick way to remove default elements from the CKAN menu and you may need todo this
in order for you to have space for the new items you add.  These options are:

```
ckanext.frontpage.about_menu = False
ckanext.frontpage.group_menu = False
ckanext.frontpage.organization_menu = False
```

By default these are all set to True, like on a default install.

To enable HTML output for the frontpage (along with Markdown), add the following to your config:

```
ckanext.frontpage.allow_html = True
```

By default this option is set to False. Note that this feature is only available for CKAN >= 2.3. For older versions of CKAN, this option has no effect.
Use this option with care and only allow this if you trust the input of your users.

If you want to use the WYSIWYG editor instead of Markdown:
```
ckanext.frontpage.editor = medium
```
or
```
ckanext.frontpage.editor = ckeditor
```
This enables either the [medium](https://jakiestfu.github.io/Medium.js/docs/) or [ckeditor](http://ckeditor.com/)

## Helper Functions

TODO

Add info about all helper functions paster tracking export test.csv 2017-01-01 -c /etc/ckan/default/development.ini
Dependencies
------------

* lxml



