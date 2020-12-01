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
    gameid = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE)

    # 1 = user1
    # 2 = user2
    current_player = models.PositiveSmallIntegerField('current_player')

    # [1][2][3]
    # [4][5][6]
    # [7][8][9]

    # n = none
    # x = player x occupied
    # o = player o occupied

    #[n][n][n]-[n][n][n]-[n][n][n]

    grid_squares = models.CharField('grid_state', max_length=29)
    last_timestamp = models.DateTimeField('last_updated', auto_now=True)




