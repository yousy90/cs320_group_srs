from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from .models import User


from django.db import IntegrityError

from django.http import Http404

from django.template import loader

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Writing more views
def detail(request, question_id):
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    #return render(request, 'polls/detail.html', {'question': question})

    # Rewritten using idioms
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


#def results(request, question_id):
#    response = "You're looking at the results of a question %s."
#    return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data.  This prevents data from being posted twice if
        # a user hits the back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def testground(request):
    return render(request, 'polls/testground.html')

def register(request):
    if request.method == 'GET':
        # serve up the initial username/password/register stuff
        atr = False
        if 'attempted_registry' in request.session:
            atr = True
            

        return render(request, 'polls/register.html', {'verz': 'GET', 'ar': atr})

    elif request.method == 'POST':
   
        # Need to sanitize input here to protect against stuff (just in case django doesn't) 
        ##
        ##
        ##
        # Checking to see if the user already exists
        

        # Attempting to create new user
        username = request.POST['uname']
        password = request.POST['pword']
        succeeded = False
        try:
            new_user = User.objects.create(username=username, password=password)
            succeeded = True
            request.session['username'] = username
        except IntegrityError:
            succeeded = False

        request.session['attempted_registry'] = True
        return render(request, 'polls/register.html', {'verz': 'POST', 'succeeded': succeeded, 'username': username, 'password': password})


def login(request):

    if request.method == 'GET':
        username = request.session.get('username')
        if username:
            return HttpResponseRedirect(reverse('polls:homepage'))
        return render(request, 'polls/login.html')

    elif request.method == 'POST':
        username = request.session.get('username')
        password = request.session.get('password')

        user = User.objects.get(username=username, password=password)

        ## redirect to homepage
        return HttpResponseRedirect(reverse('polls:homepage'))


def homepage(request):
    username = request.session.get('username')
    return render(request, 'polls/homepage.html', {'username': username})
