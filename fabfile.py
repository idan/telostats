from fabric.api import local


def deploy_staticfiles():
    local('STATIC_S3=1 ./manage.py collectstatic --noinput')


def deploy_heroku():
    local('git push heroku master')


def deploy():
    deploy_staticfiles()
    deploy_heroku()
