"""

    TODO: Modify the Game model to include a 'concluded' bool and 'outcome' e.g. 'timeout', 'completed'.
          This way things aren't deleting - lessen ambiguity - but its possible to filter out
          deviant Game entries that have already been addressed.


"""

QUEUE_TIMEOUT_MINUTES = 1
MOVE_TIMEOUT_SECONDS = 30


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


def clean_expired_queue(user):
    """
        Returns: true if an expired queue entry was found and resolved. Else false
    """
    now = datetime.now()
    expiration_cutoff = now - timedelta(hours=0, minutes=QUEUE_TIMEOUT_MINUTES)
    stale_gameset = Game.objects.filter(user1=user, user2=None, completion_status=0, last_timestamp__lte=expiration_cutoff)
    if stale_gameset:
        for game in stale_gameset:
            game.completion_status = 1
            game.outcome = 'QUEUE_TIMEOUT'
            game.save()
            return True

    return False

def clean_timeout_game(user):   
    """
        Returns: true if an unfinished game entry with an expired timestamp is found
    """

    def closeout_game(game):
         
        user1 = game.user1
        user2 = game.user2
        loser = game.current_player

        if loser == user1:
            # Updating player stats
            user1.losses += 1 
            user1.save()
            user2.wins += 1
            user2.save()
            # UPdating game record
            game.outcome='USER2_WINS'
        else:   # loser == user2
            # Updating player stats
            user2.losses +=1 
            user2.save()
            user1.wins += 1
            user1.save() 
            # Updating game record
            game.outcome='USER1_WINS'
            
        # Finalzing game record
        game.completion_status = 1
        game.save()


    # Logic begins 

    # Establishing cutoff datetime
    now = datetime.now()
    expiration_cutoff = now - timedelta(hours=0, minutes=0, seconds=MOVE_TIMEOUT_SECONDS)

    # Retrieving potential Game entry
    # First trying where user is in the player 1  slot
    timeouts_user1 = Game.objects.filter(user1=user, user2__isnull=False, completion_status=0, last_timestamp__lte=expiration_cutoff)
    if timeouts_user1.count() > 0:
        for game in timeouts_user1:
            closeout_game(game) 
            return True

    # Now checking where user is in the player2 slot
    timeouts_user2 = Game.objects.filter(user1__isnull=False, user2=user, completion_status=0, last_timestamp__lte=expiration_cutoff)
    if timeouts_user2.count() > 0:
        for game in timeouts_user2:
            closeout_game(game)
            return True

    return False 


def already_queued(user):
    
    now = datetime.now()
    expiration_cutoff = now - timedelta(hours=0, minutes=QUEUE_TIMEOUT_MINUTES)

    queued_game_exists = Game.objects.filter(user1=user, user2=None, completion_status=0, last_timestamp__gte=expiration_cutoff).exists()
    
    if queued_game_exists:
        return True
    return False



def already_in_game(user):
    
    # Checking for games where user is in the first player slot
    game_already_exists = Game.objects.filter(user1=user, user2__isnull=False, completion_status=0).exists()
    if game_already_exists:
        return True

    # Checking for games where  user is in the second player slot
    game_already_exists = Game.objects.filter(user1__isnull=False, user2=user, completion_status=0).exists()
    if game_already_exists:
        return True

    return False


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


    # Checking for stale queue entry
    if clean_expired_queue(current_user):   
        return HttpResponse('You had a stale queue entry. We deleted it :)')

    # Checking for in-progress games that have timed out and thus 
    # need outcome and score processing to occur.
    if clean_timeout_game(current_user):
        request.session['wins'] = current_user.wins
        request.session['losses'] = current_user.losses
        return HttpResponse('You had a game with a score pending..Your record has now been updated :)')


    # Checking if the player is already queued 
    if already_queued(current_user):
        return HttpResponse('You are already queued!') 


    # Checking if the player is already in a game
    if already_in_game(current_user):
        return HttpResponse('You are already in a game!')



    # At this point the player should be matched with anyone already waiting(if such a thing exists)
    # or placed into the queue waiting for someone else
        
    # first check if waiting game   
    now = datetime.now()
    cutoff = now - timedelta(hours=0, minutes=5) 
    queued_game = Game.objects.filter(user2=None, completion_status=0, last_timestamp__gt=cutoff).first()

    if queued_game:
        queued_game.user2 = current_user
        queued_game.outcome = 'IN_PROGRESS'                                                                                                                          
        queued_game.save()
        return HttpResponse(f'You\'ve matched against {queued_game.user1}!')

    else:
       # No game waiting. Creating new game 
        new_game = Game.objects.create(user1=current_user, user2=None, current_player=current_user, completion_status=0, outcome='N/A')
        request.session['game_id'] = new_game.game_id
        return HttpResponse(f'Created a new game with the id of {new_game.game_id}')
   

    






