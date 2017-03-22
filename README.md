ckanext-frontpage
=============

This extension gives you an easy way to add simple frontpage to CKAN. THis extension should be installed
with the [ckanext-monsanto theme](https://github.com/MonsantoCo/ckanext-monsanto)

By default you can add frontpage to the main CKAN menu.

Works for ckan>=2.5

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

custom helpers available to the templates

``` 
get_frontpage_content -- returns the content when the ID is passed for that content
get_frontpage_list -- retuns all non private content defaults to 5 but you can pass a number this will order them by publish data and will exclude entries without one
get_featured_org_count -- get the number or orgs featured
get_tracking -- returns tracking results for a package ID
get_tracking_total -- process tracking totals and exports them to file 
```

all helpers will be available as h.<helper name>(<vars>)

Add info about all helper functions paster tracking export test.csv 2017-01-01 -c /etc/ckan/default/development.ini

##Tracking and Main Page View Count

A cron has to be setup like so to run at an interval you would like you pageview tracking to be updated.

```/usr/lib/ckan/default/bin/paster --plugin=ckan tracking update -c /etc/ckan/default/development.ini && /usr/lib/ckan/default/bin/paster --plugin=ckan search-index rebuild -r -c /etc/ckan/default/development.ini```
 
 you must also have a cron nightly to update overall tracking and push the file to the path below
 
 ```paster tracking export /usr/lib/ckan/default/src/pagewiecount30day.csv 2017-01-01 -c /etc/ckan/default/development.ini```

Dependencies
------------

* lxml



