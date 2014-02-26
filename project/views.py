from pyramid.view import view_config
from pyramid.httpexceptions import HTTPClientError
from pyramid.httpexceptions import HTTPFound
from project.models import Question
from bson import ObjectId
import logging
from elasticsearch.exceptions import NotFoundError
from pymongo.errors import OperationFailure

log = logging.getLogger(__name__)

def add_question(request, question):
    pass

def remove_requestion(question):
    pass

def search_questions(es, keywords):
    print keywords
    try:
        #questions = es_search({"query": {"match_all": {}}})
        questions = Question.search(es, {"query":{"term":{"content": keywords}}})
        print questions
    except NotFoundError as error:
        log.debug('Search NotFoundError: %s.' % error)
        questions = []
    return questions

@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    if request.method == 'POST':
        # search
        log.debug('Searching questions.')
        action = 'search'
        keywords = request.POST.get('keywords', '')
        query = {'query': {'term': {'content': keywords}}}
        questions = [q for q in Question.search_elastic(query)]
    else:
        # list
        log.debug('Listing questions.')
        keywords = ''
        action = 'list'
        questions = [q for q in Question.search_mongo()]
    return {'questions': questions, 'action': action, 'keywords': keywords}

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
    question = Question(_id=id)
    try:
        log.debug('Removing question with id: "%s"', id)
        question.delete()
    except (NotFoundError, OperationFailure) as e:
        log.debug('Invalid question id: "%s"', id)
        return HTTPClientError('Invalid Request: Question does not exist.')
    return HTTPFound(location=request.route_url('list'))