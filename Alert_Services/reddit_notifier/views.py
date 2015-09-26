from .models import Subscription
from django.contrib.auth.models import User
from tasks import *
from notification_functions import *
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

"""Returns the homepage."""
def index(request):
	if request.user.is_authenticated():
		context = {'loggedin':True}
	else:
		context = {'loggedin':False}
	return render(request, 'reddit_notifier/index.html', context)

"""Parses POST request and creates new User. Logs user in if successful. Redirects to homepage."""
def signup(request):
	username = request.POST.get('phone_number', False)
	password = request.POST.get('user_password', False)
	first_name = request.POST.get('first_name', False)
	last_name = request.POST.get('last_name', False)
	new_user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name)
	new_user.save()
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	return HttpResponseRedirect(reverse('reddit_notifier:index'))

"""Responds to user request to have most recent post from a given subreddit
	texted to their phone. Returns a json containing a message concerning the response result."""
def get_subreddit_post(request):
	phone_num = request.POST.get('phone_number', False)
	subreddit = request.POST.get('subreddit_name', False)
	response = fetch_subreddit(subreddit)
	server_response = {}
	if response:
		success = send_message(response, phone_num)
		if success:
			server_response['result'] = 'Message sent successfully!'
		else:
			server_response['result'] = 'An error occurred while contacting Twilio. :('
	else:
		server_response['result'] = 'An error occurred while contacting Reddit. Please check the name of your subreddit. :('
	return HttpResponse(json.dumps(server_response), content_type = "application/json")

"""Delivers the my_account page if the user is logged in."""
@login_required()
def my_account(request):
	subscriptions_list = Subscription.objects.filter(user=request.user)
	context = {'subscriptions_list':subscriptions_list, 'user_name':request.user.first_name}
	return render(request, 'reddit_notifier/my_account.html', context)

"""Creates a Subscription object for given user per request."""
@login_required()
def create_subscription(request):
	subreddit_name = request.POST.get('subreddit_name', False)
	frequency = request.POST.get('frequency', False)
	if not frequency == False:
		frequency = int(frequency)
	new_subscription = Subscription(user = request.user, subreddit = subreddit_name, frequency = frequency)
	new_subscription.save()
	fetch_subreddit(subreddit_name) #this just ensures that the subreddit winds up in CachedItems if it isn't already so that it is present when attempting to fulfill subscription
	return HttpResponseRedirect(reverse('reddit_notifier:my_account'))

"""Removes a Subscription object for a given user per request."""
@login_required()
def delete_subscription(request):
	subscription_id = request.POST.get('subscription_id')
	subscription = Subscription.objects.filter(id = subscription_id)
	if subscription:
		subscription.delete()
	return HttpResponseRedirect(reverse('reddit_notifier:my_account'))

"""Verifies user authentication for sign in."""
def authentication(request):
	phone_num = request.POST.get('phone_number', False)
	password = request.POST.get('user_password', False)
	user = authenticate(username=phone_num, password=password)
	if user is not None:
		login(request, user)
	return HttpResponseRedirect(reverse('reddit_notifier:index'))

"""Logs a user out."""
def request_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('reddit_notifier:index'))



