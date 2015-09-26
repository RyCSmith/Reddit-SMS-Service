from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /signup
    url(r'^signup/$', views.signup, name='signup'),
    # ex: /my_account
    url(r'^my_account/$', views.my_account, name='my_account'),
    # POST to create subscription
    url(r'^create_subscription/$', views.create_subscription, name='create_subscription'),
    # POST to delete subscription
    url(r'^delete_subscription/$', views.delete_subscription, name='delete_subscription'),
    # POST for getting a subreddit post sent via SMS
    url(r'^get_subreddit_post/$', views.get_subreddit_post, name='get_subreddit_post'),
    # POST for authentication
    url(r'^authenticate/$', views.authentication, name='authentication'),
    # POST for logout
    url(r'^logout/$', views.request_logout, name='request_logout'),
]