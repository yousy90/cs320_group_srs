from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Exception when creating a User
# whose username is already taken
from django.db import IntegrityError

# Exception when attempting to SELECT
# an entry that doesn't exist
from django.core.exceptions import ObjectDoesNotExist


# Our set of models 
from .models import User
from .models import Game


# standard python library I need
from datetime import timedelta
from datetime import datetime


#def get_stale_game(username):
    #now = datetime.now()
    #expiration_cutoff = now - timedelta(hours=0, minutes=5)

    # Checking for games where current user is player 1
    #stale_game = Game.objects.filter(user1=current_user, last_timestamp__lte(expiration_cutoff))
    #if stale_game:
    #    return stale_game


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


    # Testing if user has already logged in
    already_logged = request.session.get('username', None)
    if already_logged:
        return HttpResponseRedirect(reverse('tictac:homepage'))

    # Getting here means the user has not logged in
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

    # Checking if the user has already logged in
    already_logged = request.session.get('username', None)
    if already_logged:
        return HttpResponseRedirect(reverse('tictac:homepage'))
    
    # GET handler
    if request.method == 'GET':
        return render(request, 'tictac/login.html', {'method': 'GET'})

    # POST handler
    elif request.method == 'POST':
        alleged_username = request.POST['uname']
        alleged_password = request.POST['pword']

        try:
            user = User.objects.get(username=alleged_username, password=alleged_password)
            request.session['username'] = user.username
            request.session['wins'] = user.wins
            request.session['losses'] = user.losses
            return HttpResponseRedirect(reverse('tictac:homepage'))
        except ObjectDoesNotExist:
            return render(request, 'tictac/login.html', {'method': 'POST'})

    

def homepage(request):

    # Redirecting to login page if necessary
    already_logged = request.session.get('username', None)
    if not already_logged:
        return HttpResponseRedirect(reverse('tictac:login'))


    username = request.session.get('username')
    wins = request.session.get('wins')
    losses = request.session.get('losses')

    return render(request, 'tictac/homepage.html', {'username': username, 'wins': wins, 'losses': losses})




def entergame(request):

    player_name = request.session.get('username', None)
    # Returning error if visitor isn't logged in
    if player_name == None:
        return render(request, 'tictac/error.html', {'error_message': 'You must login before joining a game'})

    # Checking if user has open/in progress games  
    # Need to check for games where user1 or user2 is username and timestamp > 5 mins old to accomplish cleanup.
    # notes original had me checking the gameid of the session, but that doesn't seem robust.
    current_user = User.objects.get(username=player_name)

    # Check if the player has  stale queues or games that timed out
    now = datetime.now()
    cutoff = now - timedelta(hours=0, minutes=1) 
    if  Game.objects.filter(user1=current_user, user2=None, last_timestamp__lte=cutoff).first():
        Game.objects.filter(user1=current_user, user2=None, last_timestamp__lte=cutoff).delete()
        return HttpResponse('You had a stale queue entry. We deleted it :)')
    


    # Throw error if the player is already queuing 
    if  Game.objects.filter(user1=current_user, user2=None).first():
        queued_game = Game.objects.get(user1=current_user, user2=None)
        return HttpResponse(f'you are already queued for a game ({queued_game.game_id})')
        


        
    # first check if waiting game   
    now = datetime.now()
    cutoff = now - timedelta(hours=0, minutes=5) 
    queued_game = Game.objects.filter(user2='none', last_timestamp__gt=cutoff)

    if queued_game:
        return HttpResponse('Queued game is waiting!')
    else:
       # No game waiting. Creating new game 
        new_game = Game.objects.create(user1=current_user)
        request.session['game_id'] = new_game.game_id
        return HttpResponse(f'Created a new game with the id of {new_game.game_id}')
   

    






