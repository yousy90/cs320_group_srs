from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField('username', primary_key=True, max_length=150)
    password = models.CharField('password', max_length=150) 
    wins = models.PositiveIntegerField('wins', default=0)
    losses = models.PositiveIntegerField('losses', default=0)
    

    def __str__(self):
        return self.username


class Queue(models.Model):

    waiting_user = models.ForeignKey(User, on_delete=models.CASCADE)
    entered_time = models.DateTimeField('time_entered', auto_now_add=True)


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE, null=True, blank=True)
    current_player = models.ForeignKey(User, related_name="current_player", on_delete=models.CASCADE, null=True, blank=True)
    # 0 = incomplete, 1 = complete
    completion_status = models.PositiveSmallIntegerField('completion_status', default=0)
    outcome = models.CharField('outcome', max_length=30, default='N/A')

    # 1 = user1
    # 2 = user2

    # [1][2][3]
    # [4][5][6]
    # [7][8][9]

    # n = none
    # x = player x occupied
    # o = player o occupied

    #[n][n][n]-[n][n][n]-[n][n][n]

    grid_squares = models.CharField('grid_state', max_length=29, null=True, blank=True)
    last_timestamp = models.DateTimeField('last_updated', auto_now=True)




