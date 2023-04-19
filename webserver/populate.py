import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'dogsorcats.settings')
django.setup()
from voteapp.models import *  # noqa: E402
from django.contrib.auth.models import User  # noqa: E402
from datetime import datetime, timedelta

def count():
	print("Total de votos a gatos: " + str(Vote.objects.filter(voteType=VoteType.CATS).count()))
	print("Total de votos a perros: " + str(Vote.objects.filter(voteType=VoteType.DOGS).count()))
	print("Total de votos a empate: " + str(Vote.objects.filter(voteType=VoteType.TIE).count()))

def populate():

	dict_user = {'user': 'manuel', 'password': 'prueba123', 'nVotes': 10}
	Vote.objects.all().delete()
	count()
	try:
		usuario = User.objects.get(username=dict_user['user'])
	except User.DoesNotExist:
		usuario = User.objects.create_user(username=dict_user['user'], password=dict_user['password'])
	print("Creamos votos aleatorios para el usuario " + dict_user['user'])
	
	for i in range(dict_user['nVotes']):
		random_vote = random.choice(list(VoteType))
		Vote.objects.create(user=usuario, voteType=random_vote)
	count()

if __name__ == '__main__':
	populate()