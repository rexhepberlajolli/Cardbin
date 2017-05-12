#!/usr/bin/python

import re
import requests
import time
from lxml import html

class Crawler(object):
	def __init__(self, pastebin_url_string):
		self.pastebin_url_string = pastebin_url_string
		self.regex = {"CreditCard": "(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})"}
		self.cc_regex = re.compile(self.regex['CreditCard'], re.IGNORECASE)
		self.get_content()


	def check_for_cc(self):
		if re.match(self.cc_regex, self.content) != None:
			print "\033[92mFound CreditCard on https://pastebin.com/raw%s\033[0m" % self.pastebin_url_string
			print "\033[92m%s\033[0m" % self.content
			with open('cc.txt', 'a+') as filee:
				filee.write("*" * 50 + "\r\n")
				filee.write("Content of: https://pastebin.com/raw%s :\r\n" % self.pastebin_url_string)
				filee.write(self.content+"\r\n")
			filee.close()
		else:
			pass


	def get_content(self):
		print "Checking: https://pastebin.com/raw%s" % self.pastebin_url_string
		self.content = requests.get("https://pastebin.com/raw%s" % self.pastebin_url_string).content
		self.check_for_cc()
		


used_paste = ['/scraping', '/pro']

while True:
	for archive in html.fromstring(requests.get("https://pastebin.com/archive").content).xpath('//@href')[13:21]:
		if archive not in used_paste:
			used_paste.append(archive)
			Crawler(archive)
		else:
			pass
	time.sleep(float(15.5))