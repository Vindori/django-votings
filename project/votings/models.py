from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from random import choice
from string import ascii_lowercase


def random_token():
	return ''.join([choice(ascii_lowercase) for _ in range(16)])


class Author(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Question(models.Model):
	topic = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	cr_date = models.DateTimeField('creation date', default=datetime.now)
	author = models.ForeignKey('Author', on_delete=models.CASCADE)
	public = models.BooleanField(default=True)
	access_token = models.CharField(
		max_length=16,
		default=random_token,
		primary_key=True,
		unique=True
	)

	def __str__(self):
		return self.topic


class Choice(models.Model):
	label = models.CharField(max_length=30)
	votes = models.IntegerField(default=0)
	question = models.ForeignKey('Question', on_delete=models.CASCADE)

	def __str__(self):
		return self.label
