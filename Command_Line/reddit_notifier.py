import argparse, requests, json
from datetime import datetime
from twilio.rest import TwilioRestClient
import twilio

"""If option -O is selected, loops allowing the user to continue making
	requests until entering 'quit'. If subreddit and phone number are 
	provided via the command line, attempts the request and exits.
	If ValueError is caught (thrown by parse_args()) CLI -help is printed."""
def main():
	try:
		args = parse_args()
		if args.open:
			proceed = True
			while proceed:
				print "Use 'quit' to exit at any time."
				subreddit = raw_input('\tEnter name of subreddit:  ').strip()
				if subreddit != 'quit':
					phone_number = raw_input('\tEnter phone number:  ').strip()
					if phone_number != 'quit':
						attempt_request(subreddit, phone_number)
					else:
						proceed = False
				else:
					proceed = False
		else:
			attempt_request(args.subreddit, args.phone_number)

	except ValueError as e:
		print(e)

"""Calls methods to interact with Reddit and Twilio services and informs
	user of the result."""
def attempt_request(subreddit, phone_number):
	message = fetch_subreddit(subreddit)
	if not message:
		print "\tAn error occurred while fetching that subreddit. Please check your input."
	else:
		result = send_message(message, phone_number)
		if result:
			print "\tMessage Sent!"
		else:
			print "\tAn error occurred while sending via Twilio. Please try again."

"""Uses argparse to parse command line arguments and make sure a valid option has
	been selected. Returns arguments object if valid. Raises an exception if not."""
def parse_args():
	parser = argparse.ArgumentParser(description='PromptWorks Reddit Machine!')
	parser.add_argument('-S', '--subreddit', metavar='subreddit', type=unicode,
        help='Name of subreddit.', required=False)
	parser.add_argument('-N', '--phone_number', metavar='##########', type=int,
    	help='Phone number to send SMS to.', required=False)
	parser.add_argument('-O', '--open', help='Opens a loop for repeated requests.', 
		action='store_true', required=False)
	args = parser.parse_args()
	if not (args.open or (args.subreddit and args.phone_number)):
		raise ValueError(parser.format_help())
	return args

"""Fetches message text for a specified subreddit. Makes a request to Reddit. 
	Verifies to check valid response and returns message text if so. Returns 
	False is unsuccessful."""
def fetch_subreddit(subreddit):
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
			return text + " " + url
	except Exception as e:
		return False

"""Sends a message containing the provided text to the provided phone number using Twilio.
	Returns True if message receives an sid, False otherwise, indicating error."""
def send_message(message_text, phone_number):
	try:
		phone_number = "+1" + str(phone_number)
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

if __name__ == '__main__':
    main()