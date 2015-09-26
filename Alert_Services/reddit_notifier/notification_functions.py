from django.contrib.auth.models import User
from .models import Subscription
import requests, json
from datetime import datetime
from django.utils import timezone
from twilio.rest import TwilioRestClient
from .models import Subscription, CachedItem

"""Fetches message text for a specified subreddit. First checks the CachedItems
	to see if item has been fetched. If not found, makes a request to Reddit. 
	Verifies to check valid response and returns message text if so. Returns 
	False is unsuccessful."""
def fetch_subreddit(subreddit):
	try:
		potential_record = CachedItem.objects.filter(subreddit = subreddit)
		if potential_record:
			return potential_record[0].text + " " + potential_record[0].url
		url = 'https://www.reddit.com/r/' + subreddit + '/new.json?limit=1'
		headers = {'User-Agent': 'reddit_notifier 1.0','From': 'rycsmith@gmail.com'}
		req = requests.get(url, headers=headers)
		response_json = json.loads(req.text)
		#response format will tell if request was diverted to search query (bad subreddit name)
		subreddits_list = response_json['data']['children']
		if ((len(subreddits_list) > 1) or (len(subreddits_list) == 0)):
			return False
		else:
			text = response_json['data']['children'][0]['data']['title']
			url = response_json['data']['children'][0]['data']['url']
			new_cache_item = CachedItem(subreddit = subreddit, text = text, url = url, last_updated = timezone.now())
			new_cache_item.save()
			return text + " " + url
	except Exception as e:
		return False

"""Fetches message text for a subreddit without checking the CachedItems. This is used for 
	updated the CachedItems. Creates and returns CachedItem on success, False otherwise."""
def fetch_subreddit_no_cache(subreddit):
	try:
		url = 'https://www.reddit.com/r/' + subreddit + '/new.json?limit=1'
		headers = {'User-Agent': 'reddit_notifier 1.0','From': 'rycsmith@gmail.com'}
		req = requests.get(url, headers=headers)
		response_json = json.loads(req.text)
		#response format will tell if request was diverted to search query (bad subreddit name)
		subreddits_list = response_json['data']['children']
		if ((len(subreddits_list) > 1) or (len(subreddits_list) == 0)):
			return False
		else:
			text = response_json['data']['children'][0]['data']['title']
			url = response_json['data']['children'][0]['data']['url']
			new_cache_item = CachedItem(subreddit = subreddit, text = text, url = url, last_updated = timezone.now())
			return new_cache_item
	except Exception as e:
		return False

"""Sends a message containing the provided text to the provided phone number using Twilio.
	Returns True is message receives an sid, False otherwise, indicating error."""
def send_message(message_text, phone_number):
	try:
		phone_number = "+1" + phone_number
		client = TwilioRestClient('AC68b58ad68b2149e952897e80c14a3d56', 'cf8bc59d80aad1c74f4cba3d92edb137')	 
		message = client.messages.create(
			body = message_text,
			to = phone_number,  
			from_ = '+12153372440')
		if message.sid:
			return True
		return False
	except twilio.TwilioRestException as e:
		return False

