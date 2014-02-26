from pyramid.view import view_config
from pyramid.httpexceptions import HTTPClientError
from pyramid.httpexceptions import HTTPFound
from project.models import Question
from bson import ObjectId
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    questions = Question.objects
    return {'questions': questions}

@view_config(route_name='ask')
def ask_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # save question
            log.debug('Adding question content: "%s"', content)
            question = Question(content=content)
            question.save()
        else:
            # invalid question
            log.debug('Invalid question content: "%s"', content)
            return HTTPClientError('Invalid Request: Question content cannot be empty.')
    return HTTPFound(location=request.route_url('list'))

@view_config(route_name='remove')
def remove_view(request):
    id = request.matchdict['id']
    question = Question.objects(id=id)
    if question:
        log.debug('Removing question with id: "%s"', id)
        question.delete()
    else:
        log.debug('Invalid question id: "%s"', id)
        return HTTPClientError('Invalid Request: Question does not exist.')
    return HTTPFound(location=request.route_url('list'))