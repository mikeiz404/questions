from pyramid.config import Configurator
from pyramid.events import NewRequest
from pymongo import MongoClient

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
    # setup mongodb
    db_uri = settings['mongodb.url']
    dbc = MongoClient(db_uri)
    config.registry.settings['mongodb_conn'] = dbc
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db_conn = settings['mongodb_conn']
        db = db_conn[db_name]
        event.request.db_conn = db_conn
        event.request.db = db
    config.add_subscriber(add_mongo_db, NewRequest)
    # setup routes
    config.add_route('list', '/')
    config.add_route('ask', '/ask')
    config.add_route('remove', '/remove/{id}')
    config.add_route('search', '/search')
    # scan project
    config.scan('project')
    return config.make_wsgi_app()
