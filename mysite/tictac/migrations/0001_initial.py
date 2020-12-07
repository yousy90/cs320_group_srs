# Generated by Django 3.1.3 on 2020-12-01 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='username')),
                ('password', models.CharField(max_length=150, verbose_name='password')),
                ('wins', models.PositiveIntegerField(default=0, verbose_name='wins')),
                ('losses', models.PositiveIntegerField(default=0, verbose_name='losses')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameid', models.AutoField(primary_key=True, serialize=False)),
                ('current_player', models.PositiveSmallIntegerField(verbose_name='current_player')),
                ('grid_squares', models.CharField(max_length=29, verbose_name='grid_state')),
                ('last_timestamp', models.DateTimeField(auto_now=True, verbose_name='last_updated')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='tictac.user')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='tictac.user')),
            ],
        ),
    ]