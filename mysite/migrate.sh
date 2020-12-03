#!/bin/bash

i=$(cat mig_count.txt)


# first command
pipenv run python3 manage.py makemigrations tictac

# second command
pipenv run python3 manage.py sqlmigrate tictac 000$i

# third command
pipenv run python3 manage.py migrate


# increment and save the new i value
i=$((i+1))
echo $i > mig_count.txt
