from fabric.api import local
from fabric.context_managers import lcd
from unipath import FSPath as _Path

FABFILE_PATH = _Path(__file__).absolute().ancestor(1)


def deploy_staticfiles():
    local('STATIC_S3=1 ./manage.py collectstatic --noinput')


def deploy_heroku():
    local('git push heroku')


def deploy():
    deploy_staticfiles()
    deploy_heroku()


def sass():
    """Watch sass files for changes and recompile"""
    with lcd(FABFILE_PATH.child('sass')):
        css_path = FABFILE_PATH.child('telostats', 'static', 'css')
        sass_watch = 'sass --watch .:{} -r ./bourbon/lib/bourbon.rb'
        local(sass_watch.format(css_path))
