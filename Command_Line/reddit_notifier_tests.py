import unittest
from reddit_notifier import *

"""This class in entirely dedicated to I/O and as such is difficult to test.
	However, these tests can be used to ensure outside systems are running properly."""
class Reddit_Notifier_Test(unittest.TestCase):

	def test_fetch_subreddit(self):
		# attempt to fetch a subreddit that exists
		result = fetch_subreddit('opensource')
		#make sure string is returned
		self.assertTrue(len(result) > 0)
		# title and url should be split by space in middle
		self.assertTrue(result.find(" ") > 0)
		# make sure that a url follows
		self.assertTrue(result[result.find(" "):].find("http") > 0)
		# subreddit that does not exist should return false
		self.assertFalse(fetch_subreddit('opeadnsasdourasdce'))

	def test_send_message(self):
		#this test cannot verfiy logic since it relys entirely on Twilio - this is just used to indicate is service is down or malfunctioning
		self.assertTrue(send_message("test_message", "5202627130"))

unittest.main()