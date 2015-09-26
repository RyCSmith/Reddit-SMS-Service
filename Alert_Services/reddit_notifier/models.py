from django.db import models
from django.contrib.auth.models import User
import datetime

"""Subscription model used to store User subscription."""
class Subscription(models.Model):
	user = models.ForeignKey(User)
	subreddit = models.CharField(max_length = 200)
	frequency = models.IntegerField(default = 60)

"""Model used to store the results of a request for a given subreddit."""
class CachedItem(models.Model):
	subreddit = models.CharField(max_length = 200)
	text = models.CharField(max_length = 200)
	url = models.CharField(max_length = 200)
	last_updated = models.DateTimeField('last updated')

