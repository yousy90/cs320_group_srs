# Generated by Django 3.1.3 on 2020-11-13 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='username')),
                ('password', models.CharField(max_length=150, verbose_name='password')),
            ],
        ),
    ]