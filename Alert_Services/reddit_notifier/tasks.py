from .models import Subscription, CachedItem
from django.contrib.auth.models import User
from notification_functions import *
from datetime import datetime
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

#scheduled tasks
"""Runs every 2 minutes. Queries all subreddits in CachedItems, requests most recent post from Reddit
	and replaces the CachedItem if changes have occurred."""
@periodic_task(run_every=(crontab(hour="*", minute="*/2", day_of_week="*")), ignore_result=True)
def update_cached_listings():
	cached_items = CachedItem.objects.all()
	for item in cached_items:
		result_item = fetch_subreddit_no_cache(item.subreddit)
		if result_item is not False:
			if result_item.text != item.text:
				item.delete()
				result_item.save()

"""Runs every 2 minutes. Adds schedule_message() for all 2 minute subscriptions to the async task queue."""
@periodic_task(run_every=(crontab(hour="*", minute="*/2", day_of_week="*")), ignore_result=True)
def fulfill_two_minute_subscriptions():
	two_minute_subs = Subscription.objects.filter(frequency = 2)
	for item in two_minute_subs:
		phone_num = item.user.username
		matching_items = CachedItem.objects.filter(subreddit = item.subreddit)
		message = matching_items[0].text + " " + matching_items[0].url
		if message:
			schedule_message.delay(phone_num, message)

"""Runs every hour. Adds schedule_message() for all hour subscriptions to the async task queue."""
@periodic_task(run_every=(crontab(hour="*", minute="0", day_of_week="*")), ignore_result=True)
def fulfill_hour_subscriptions():
	hour_subs = Subscription.objects.filter(frequency = 60)
	for item in hour_subs:
		phone_num = item.user.username
		matching_items = CachedItem.objects.filter(subreddit = item.subreddit)
		message = matching_items[0].text + " " + matching_items[0].url
		if message:
			schedule_message.delay(phone_num, message)

"""Runs every day. Adds schedule_message() for all day subscriptions to the async task queue."""
@periodic_task(run_every=(crontab(hour="12", minute="0", day_of_week="*")), ignore_result=True)
def fulfill_daily_subscriptions():
	day_subs = Subscription.objects.filter(frequency = 1440)
	for item in day_subs:
		phone_num = item.user.username
		matching_items = CachedItem.objects.filter(subreddit = item.subreddit)
		message = matching_items[0].text + " " + matching_items[0].url
		if message:
			schedule_message.delay(phone_num, message)

#unscheduled tasks
"""Wraps the send_message() function so that it can be added to the async task queue and processed when possible."""
@shared_task()
def schedule_message(phone_num, message):
	send_message(message, phone_num)
