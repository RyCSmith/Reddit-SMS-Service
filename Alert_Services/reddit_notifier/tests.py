from django.test import TestCase
from tasks import *
from notification_functions import *
from .models import Subscription, CachedItem
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from datetime import datetime
from django.utils import timezone


class Reddit_Notifier_View_Tests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(first_name = 'test', last_name = 'user', username = '123456789', password = "testpass")
		self.user.save()

	def test_index(self):
		response = self.client.get(reverse('reddit_notifier:index'))
		self.assertEqual(response.status_code, 200)
	
	def test_signup(self):
		url = reverse('reddit_notifier:signup')
		data = {'phone_number':'22334455','first_name':'John','last_name':'Snow','user_password':'Ghost'}
		users = User.objects.filter(username='22334455')
		self.assertFalse(users)
		self.client.post(url, data, format='json')
		users = User.objects.filter(username='22334455')
		self.assertEquals(1, len(users))
		#test case for username that already exists

	def test_my_account(self):
		#not logged in
		response = self.client.get(reverse('reddit_notifier:my_account'))
		self.assertEqual(response.status_code, 302)
		#verify no subscriptions listed
		self.client.login(username = "123456789", password = "testpass")
		response = self.client.get(reverse('reddit_notifier:my_account'))
		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context['subscriptions_list'])
		user = User.objects.filter(username = '123456789')[0]
		new_sub = Subscription(user=user, subreddit='opensource', frequency='2')
		new_sub.save()
		#verify new subscription now shown
		response = self.client.get(reverse('reddit_notifier:my_account'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(1, len(response.context['subscriptions_list']))
	
	def test_create_subscription(self):
		#verify sub does not exist
		user = User.objects.filter(username = '123456789')
		user_subs = Subscription.objects.filter(user = user)
		self.assertFalse(user_subs)
		#login and create sub
		self.client.login(username = "123456789", password = "testpass")
		url = reverse('reddit_notifier:create_subscription')
		data = {'subreddit_name':'opensource','frequency':'2'}
		self.client.post(url, data, format='json')
		user = User.objects.filter(username = '123456789')
		user_subs = Subscription.objects.filter(user = user)
		self.assertEqual(1, len(user_subs))
		#test case for sub that is invalid

	def test_delete_subscription(self):
		#create and verify subscription
		user = User.objects.filter(username = '123456789')[0]
		new_sub = Subscription(user=user, subreddit='opensource', frequency='2')
		new_sub.save()
		user_subs = Subscription.objects.filter(user = user, subreddit='opensource')
		self.assertEqual(1, len(user_subs))
		#login and test delete subscription
		self.client.login(username = "123456789", password = "testpass")
		url = reverse('reddit_notifier:delete_subscription')
		data = {'subscription_id':str(user_subs[0].id)}
		self.client.post(url, data, format='json')
		user_subs = Subscription.objects.filter(user = user, subreddit = 'opensource')
		self.assertFalse(user_subs)


class Celery_Tasks_Tests(TestCase):
	def setUp(self):
		time = datetime(2000, 4, 1, 16, 3, 8)
		item = CachedItem(subreddit="opensource", text="nonsense", url="nonsense", last_updated=time)
		item.save()
	
	def test_update_cached_listings(self):
		item = CachedItem.objects.all()[0]
		self.assertEqual(item.subreddit, "opensource")
		self.assertEqual(item.text, "nonsense")
		update_cached_listings()
		item = CachedItem.objects.all()[0]
		self.assertEqual(item.subreddit, "opensource")
		self.assertNotEqual(item.text, "nonsense")


class Notification_Function_Tests(TestCase):
	def setUp(self):
		item = CachedItem(subreddit = "opensourcesss", text = "nonsense", url = "nonsense", last_updated = timezone.now())
		item.save()
		item = CachedItem(subreddit = "opensource", text = "nonsense", url = "nonsense", last_updated = timezone.now())
		item.save()

	def test_fetch_subreddit(self):
		#verify a subreddit that is already cached
		self.assertEqual("nonsense nonsense", fetch_subreddit('opensourcesss'))
		#verify a subreddit that exists but is not cached
		self.assertIsNotNone(fetch_subreddit('gaming'))
		#verify that subreddit does not exist
		self.assertFalse(fetch_subreddit('opensdxcofnfdsf'))

	def test_fetch_subreddit_no_cache(self):
		#check a valid subreddit that is already cached with nonsense and verify it changes
		new_cache_item = fetch_subreddit_no_cache("opensource")
		self.assertNotEqual(new_cache_item.text, "nonsense")
		self.assertNotEqual(new_cache_item.url, "nonsense")
		#check that an invalid subreddit returns false regardless of caching
		new_cache_item = fetch_subreddit_no_cache("opensourcesss")
		self.assertFalse(new_cache_item)
	
	def test_send_message(self):
		pass
		#this test cannot verfiy logic since it relys entirely on Twilio - this is just used to indicate is service is down or malfunctioning
		self.assertTrue(send_message("test_message", "5202627130"))
