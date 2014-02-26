from pyramid.view import view_config
from pyramid.httpexceptions import HTTPClientError
from pyramid.httpexceptions import HTTPFound
from bson import ObjectId
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    return {'questions': [{'content': 'q1', 'id': 0}, {'content': 'q1', 'id': 1}, {'content': 'q1', 'id': 2}]}

@view_config(route_name='ask')
def ask_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # save question
            #todo: db
            log.debug('Adding question content: "%s"', content)
        else:
            # invalid question
            log.debug('Invalid question content: "%s"', content)
            return HTTPClientError('Invalid Request: Question content cannot be empty.')
    return HTTPFound(location=request.route_url('list'))

@view_config(route_name='remove')
def remove_view(request):
    id = request.matchdict['id']
    log.debug('Removing question with id: "%s"', id)
    #todo: db
    return HTTPFound(location=request.route_url('list'))