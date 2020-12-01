from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Exception when creating a User
# whose username is already taken
from django.db import IntegrityError




# Our set of models 
from .models import User

# Create your views here.
def index(request):

    # need login button
    # need register button
    #return HttpResponse("Hello, world. You're at tic tac toe index!")

    return render(request, 'tictac/index.html')



def register(request):

    """

        Successful registration updates the user's session data with
        their username
    """

    # GET handler
    if request.method == 'GET':
        return render(request, 'tictac/register.html', {'method': 'GET'})
   
    # POST handler
    elif request.method == 'POST':   # user submitted desired credentials

        desired_username = request.POST['uname']
        desired_password = request.POST['pword']
        successfully_registered = False     # 

        try:    # Attempting to create entry in the User table
            new_user = User.objects.create(username=desired_username, 
                                           password=desired_password)
            successfully_registered = True
            request.session['username'] = desired_username
        except IntegrityError:
            successfully_registered = False

        data = {'successfully_registered': successfully_registered,
                'method': 'POST',
                'username': desired_username}

        return render(request, 'tictac/register.html', data)

def login(request):

    # GET handler
    if request.method == 'GET':
        return render(request, 'tictac/login.html', {'method': 'GET'})

    # POST handler
    elif request.method == 'POST':
        alleged_username = request.POST['uname']
        alleged_password = request.POST['pword']

        try:
            user = User.objects.get(username=alleged_username, password=alleged_password)
        except ObjectDoesNotExist:
            return render(request, 'tictac/login.html', {'method': 'POST'})

        return HttpResponseRedirect(reverse('tictac:homepage'))
    

def homepage(request):

    return render(request, 'tictac/homepage.html')
