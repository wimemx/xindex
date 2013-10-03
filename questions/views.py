# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import Http404

from xindex.models import Question
from xindex.models import Question_Type
from xindex.models import Option
from xindex.models import Xindex_User
from xindex.models import Catalog
from xindex.models import Survey

from collections import namedtuple
import json

from django.http import HttpResponseRedirect, HttpResponse


def index(request):
    all_questions = Question.objects.filter(active=True).order_by('type')
    return render_to_response('questions/index.html',
                              {'all_questions': all_questions})


def add(request):
    question_types = Question_Type.objects.all().order_by('name');
    c = {}
    c.update(csrf(request))
    return render_to_response('questions/add.html',
                              {'question_types': question_types})

#TODO: Create the factory for the questions


def create_matrix(request, data):
    type = int(data.type)
    title = data.title
    cols = data.cols
    rows = data.rows

    question = Question()
    #TODO: Get the user id from session
    question.user = Xindex_User.objects.get(pk=1)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    for subquestion in rows:
        q = Question(user=Xindex_User.objects.get(pk=1),
                     title=subquestion.label,
                     type=Question_Type.objects.get(pk=type),
                     parent_question=question)
        q.save()
        i = 1
        for option in cols:
            new_option = Option(question=q, label=option.label,
                            value = i, order = i)
            new_option.save()
            i += 1

    json_response = json.dumps(
        {'messagesent': "Question added successfully!"}
    )

    return HttpResponse(json_response, content_type="application/json")


def create_multiple_choice(request, data):
    print data
    type = int(data.type)
    title = data.title
    options = data.options
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        i = 1
        for option in options:
            new_option = Option(question=catalog_question, label=option.label,
                            value = i, order = i)
            new_option.save()
            i += 1

            print new_option

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

        print catalog



    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)

    '''type = int(request.POST["type"])
    title = request.POST["title"]
    options = request.POST.getlist('options')'''

    i = 1
    for option in options:
        new_option = Option(question=question, label=option.label,
                        value = i, order = i)
        new_option.save()
        i += 1

    json_response = json.dumps(
        {
            'question_added' : True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")


def create_open_question(data):
    type = int(data.type)
    title = data.title

    question = Question()
    #TODO: Get the user id from session
    question.user = Xindex_User.objects.get(pk=1)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    json_response = json.dumps(
        {'messagesent' : "Question added successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")


def create_range_question(data):
    type = int(data.type)
    title = data.title
    start_number = int(float(data.options.start_number))
    end_number = int(float(data.options.end_number))

    if start_number < 0 or end_number > 20:
        json_response = json.dumps(
                    {'messagesent' : "Error - Limits are not valid for range"}
            )
        return HttpResponse(json_response, content_type="application/json",
                            status=400)

    question = Question()
    #TODO: Get the user id from session
    question.user = Xindex_User.objects.get(pk=1)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    new_option = Option(question=question, label=data.options.start_label,
                        value = start_number, order = start_number)
    new_option.save()

    start_number += 1

    for i in range(start_number, end_number):
        new_option = Option(question=question, label="",
                    value = i, order = i)
        new_option.save()

    new_option = Option(question=question, label=data.options.end_label,
                        value = end_number, order = end_number)
    new_option.save()

    json_response = json.dumps(
        {'messagesent' : "Question added successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")


def create_true_and_false(request, data):
    type = int(data.type)
    title = data.title
    options = ['False', 'True']
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        for i in range(len(options)):
            new_option = Option(question=catalog_question, label=options[i],
                                value=i + 1, order=i + 1)
            new_option.save()

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)


    for i in range(len(options)):
        new_option = Option(question=question, label=options[i],
                            value=i + 1, order=i + 1)
        new_option.save()

    json_response = json.dumps(
        {
            'question_added' : True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")

#TODO: Fix this; DO NOT use in production
@csrf_exempt
def add_ajax(request):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )
            #TODO: Search for types in the table question_type to avoid hardcoding
            if data.type_name == "matrix":
                return create_matrix(request, data)
            elif data.type_name == "multiple_choice":
                print(data)
                return create_multiple_choice(request, data)
            elif data.type_name == "open_question":
                return create_open_question(data)
            elif data.type_name == "range":
                return create_range_question(data)
            elif data.type_name == "true_and_false":
                return create_true_and_false(request, data)

            #If the type of question is not defined, throw an error
            json_response = json.dumps(
                    {'messagesent' : "Error - Not a valid type of question"}
            )
            return HttpResponse(json_response,
                                content_type="application/json",
                                status=400)
        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response,
                                content_type="application/json",
                                status=400)
    else:
        raise Http404


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #TODO: Try to sort this client side
    options = question.option_set.all().order_by('id')
    return render_to_response('questions/detail.html', {'question': question,
                                                        'options': options})

#TODO: Fix this; DO NOT use in production
@csrf_exempt
def remove(request, question_id):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )

            #question_id = data.question_id
            try:
                question = Question.objects.get(pk=question_id)

                #TODO: Delete all options and subquestions too
                question.active = False
                question.save()

                json_response = json.dumps(
                    {'messagesent' : "Question deleted successfully!"}
                )
                return HttpResponse(json_response,
                                    content_type="application/json")

            except Question.DoesNotExist:
                #If the type of question is not found, throw an error
                json_response = json.dumps(
                        {'messagesent': "Error - Question not found"}
                )
                return HttpResponse(json_response,
                                    content_type="application/json",
                                    status=400)

        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response,
                                content_type="application/json",
                                status=400)
    else:
        raise Http404


def edit(request, question_id):
    question_types = Question_Type.objects.all().order_by('name')
    question = get_object_or_404(Question, pk=question_id)

    #TODO: Refactor using the factory
    if question.type.name == "Matrix":
        #We get the pattern of the options based on the first child
        rows = Question.objects.filter(parent_question=question).order_by('id')
        options = rows[0].option_set.all().order_by('id')
        return render_to_response('questions/edit.html',
                                  {'question': question,
                                   'question_types': question_types,
                                   'rows': rows,
                                   'options': options})
    elif question.type.name == "Multiple Choice":
        options = question.option_set.all().order_by('id')
        return render_to_response('questions/edit.html',
                                  {'question': question,
                                   'question_types': question_types,
                                   'options': options})
    elif question.type.name == "Open question" or question.type.name == "True and False":
        return render_to_response('questions/edit.html',
                                  {'question': question,
                                   'question_types': question_types})
    elif question.type.name == "Range":
        options = question.option_set.filter(active=True).order_by('id')
        first, last = options[0], options.reverse()[0]
        return render_to_response('questions/edit.html',
                                  {'question': question,
                                   'question_types': question_types,
                                   'options': options,
                                   'first': first,
                                   'last': last})

    #If question has an undefined type (weird) return nothing
    return render_to_response('questions/edit.html',
                              {'question': question,
                               'question_types': question_types})

#TODO: Move this to the Question Factory
#TODO: Refactor this, maybe is easier and convenient to actually delete them


def update_matrix(question, data):
    cols = data.cols
    rows = data.rows

    questions = Question.objects.filter(parent_question=question).order_by('id')

    #Set all subquestions to innactive
    Question.objects.filter(parent_question=question).update(active=False)
    #as well as the options for each question
    for q in questions:
        #Set all options for this question as innactive
        q.option_set.all().update(active=False)

    #Assuming the order in data is correct
    for subquestion in rows:
        if hasattr(subquestion, 'id'):
            q = questions.get(pk=subquestion.id)
            q.title = subquestion.label
            q.active = True
            q.save()

            options = q.option_set.all().order_by('id')
            #assuming both objects are in order
            i = 0
            for option in cols:
                try:
                    opt = options[i]
                    if opt:
                        opt.label = option.label
                        opt.active = True
                        opt.save()
                    i += 1
                except IndexError:
                    #It is a new Option
                    new_option = Option(question=q, label=option.label,
                            value = i, order = i)
                    new_option.save()
        else:
            #The subquestion is new
            q = Question(user=Xindex_User.objects.get(pk=1),
                         title=subquestion.label,
                         type=Question_Type.objects.get(pk=question.type.id),
                         parent_question=question)
            q.save()

            #There must be at leat one
            cols = questions[0].option_set.all().order_by('id')
            for option in cols:
                new_option = Option(question=q, label=option.label,
                                    value=option.value, order=option.order)
                new_option.save()

        #At the end, for each question that has been 'removed' (active = False)
        #We should also delete its options
        deleted_questions = Question.objects.filter(parent_question=question,
                                                    active=False)
        for d_question in deleted_questions:
            d_question.option_set.all().update(active=False)


    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")

def update_multiple_choice(question, data):
    options = data.options

    #Set all options to innactive
    Option.objects.filter(question=question).update(active=False)
    current_options = question.option_set.all().order_by('id');

    #Assuming the order in data is correct
    i = 0
    for option in options:
        if hasattr(option, 'id'):
            opt = current_options.get(pk=option.id)
            opt.label = option.label
            opt.active = True
            opt.save()
            i += 1

        else:
            #It is a new Option
            new_option = Option(question=question, label=option.label,
                    value = i, order = i)
            new_option.save()

    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")

def update_open_question(question, data):
    question.title = data.title
    question.save()
    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")

def update_range_question(question, data):
    start_number = int(float(data.options.start_number))
    end_number = int(float(data.options.end_number))

    if start_number < 0 or end_number > 20:
        json_response = json.dumps(
                    {'messagesent': "Error - Limits are not valid for range"}
            )
        return HttpResponse(json_response, content_type="application/json",
                            status=400)

    #Set all options to innactive
    Option.objects.filter(question=question).update(active=False)
    current_options = question.option_set.all().order_by('id')

    #Setting the first value
    first_option = current_options[start_number]
    first_option.label = data.options.start_label
    first_option.value = start_number
    first_option.order = start_number
    first_option.active = True
    first_option.save()

    #Assuming the order in data is correct
    start_number += 1
    for i in range(start_number, end_number):
        try:
            updated_option = current_options[i]
            updated_option.label = ''
            updated_option.value = i
            updated_option.order = i
            updated_option.active = True
            updated_option.save()
        except IndexError:
            #It is a new Option
            new_option = Option(question=question, label="",
                                value=i, order=i)
            new_option.save()

    #Setting the last value
    try:
        #It's already within the limit
        lastOption = current_options[end_number]
        lastOption.label = data.options.end_label
        lastOption.value = end_number
        lastOption.order = end_number
        lastOption.active = True
        lastOption.save()
    except IndexError:
        #Needs to be created
        lastOption = Option(question=question, label=data.options.end_label,
                            value=end_number, order=end_number)
        lastOption.save()


    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")


def update_true_and_false(question, data):
    question.title = data.title
    question.save()
    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")

#TODO: Fix this; DO NOT use in production
@csrf_exempt
def edit_ajax(request, question_id):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )
            q_id = int(question_id)
            question = Question.objects.get(pk=q_id)
            question.title = data.title
            question.save()

            #TODO: Search for types in the table question_type to avoid hardcoding
            if question.type.name == "Matrix":
                return update_matrix(question, data)
            elif question.type.name == "Multiple Choice":
                return update_multiple_choice(question, data)
            elif question.type.name == "Open question":
                return update_open_question(question, data)
            elif question.type.name == "Range":
                return update_range_question(question, data)
            elif question.type.name == "True and False":
                return update_true_and_false(question, data)

            #If the type of question is not defined, throw an error
            json_response = json.dumps(
                    {'messagesent': "Error - Not a valid type of question"}
            )
            return HttpResponse(json_response, content_type="application/json",
                                status=400)
        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response, content_type="application/json",
                                status=400)
    else:
        raise Http404