# Reddit-SMS-Service
Django web app to subscribe to subreddit updates via SMS.  

Features:  
-Homepage allows users to request a subreddit post (from 'new' category) be texted to a phone number.  
-Homepage uses ajax to display the result of this request without reloading.  
-Users can create password protected accounts and subscribe to receive subreddit updates via SMS on a chosen interval.  
-Uses a cache system so that the program will never exceed reddit API usage while maintaining data that is at most 2 minutes old. When a user request comes in, the program will first look in the cache. If the subreddit does not exist, the request will be fulfilled then added to the cache and included in subsequent updates.  
-In order to fulfill subscriptions and update the cache without blocking I used Celery and RabbitMQ to implement an asynchronous task queue.   
-The site is connected to a MySQL database hosted in RDS which contains user info and permissions, user subscription details and currently cached items. (Future improvement could be to retain a portion of the cache in local memory).  
-I developed in a Vagrant environment using Ubuntu. I included the Vagrantfile in GitHub which should have everything needed to launch locally except RabbitMQ (I installed manually as pip version wasn't executing).  
-I used sslify to deploy the site behind ssl on Heroku using Heroku's standard ssl certificate.  
-Repo also contains a basic command line tool to send individual subreddit posts via SMS.