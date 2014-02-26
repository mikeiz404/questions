from pyramid.config import Configurator
from pyramid.events import NewRequest
from pymongo import MongoClient
import mongoengine
from project.elastic import get_elastic_search
from project.elastic import get_es_search
from project.elastic import get_es_index

from project.resources import Root

def main(global_config, **settings):
    """
    This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    # set static dir
    config.add_static_view('static', 'project:static')
    # add mako templating
    config.include('pyramid_mako')
    # add mongo db
    config.include('pyramid_mongo')
    # add elastic
    config.set_request_property(get_elastic_search, 'elastic_search')
    config.set_request_property(get_es_search, 'es_search')
    config.set_request_property(get_es_index, 'es_index')
    # setup routes
    config.add_route('list', '/')
    config.add_route('ask', '/ask')
    config.add_route('remove', '/remove/{id}')
    # scan project
    config.scan('project')
    return config.make_wsgi_app()
