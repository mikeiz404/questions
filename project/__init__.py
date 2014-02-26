from pyramid.config import Configurator
import os

def main(global_config, **settings):
    """
    This function returns a WSGI application.
    """
    # heroku addons
    elastic_uri = os.environ.get('BONSAI_URL')
    settings['elastic.uri'] = elastic_uri
    mongo_uri = os.environ.get('MONGOHQ_URL')
    settings['mongo.uri'] = mongo_uri
    config = Configurator(settings=settings)
    # set static dir
    config.add_static_view('static', 'project:static')
    # add mako templating
    config.include('pyramid_mako')
    # add document
    config.include('project.document')
    # setup routes
    config.add_route('list', '/')
    config.add_route('ask', '/ask')
    config.add_route('remove', '/remove/{id}')
    # scan project
    config.scan('project')
    return config.make_wsgi_app()
