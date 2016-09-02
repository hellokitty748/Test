import requests
import sys, os
from bs4 import BeautifulSoup
import getpass
import time
import random
import re
import urllib.parse
import traceback


class CsdnCommenter():
	sess = None
	"""
	csdn oprtor
	"""
	def __init__(self):
		self.sess = requests.session()

	def login(self):
		"""
		login and keep session
		"""
		username = input('username: ')
		password = getpass.getpass('password: ')
		url = 'https://passport.csdn.net/account/login'
		html = self.getUrlContent(self.sess, url)
		if html is None:
			return False
		soup = BeautifulSoup(html, 'html.parser')
		# with open('test.text', 'w', encoding='utf-8') as f:
		# 	f.write(soup.prettify)
		# print(soup.prettify)
		# sys.exit()

		lt = self.getElementValue(soup, 'name', 'lt')
		execution = self.getElementValue(soup, 'name', 'execution')
		_eventId = self.getElementValue(soup, 'name', '_eventId')

		data = {
				'username' : username,
				'password' : password,
				'lt' : lt,
				'execution' : execution,
				'_eventId' : _eventId
			}
		response = None
		try:
			response = self.sess.post(url, data)
		except:
			traceback.print_exc()
			pass

		return self.isLoginSuccess(response)




	def autoComment(self):
		"""
			main handler
		"""	
		if self.getSourceIds() is False:
			print("No source can commnet!")
			return
		print("Total %d source(s) wait for comment." % len(self.sourceids))

		nhandled = 0
		for sourceid in self.sourceids:
			left = len(self.sourceids) - nhandled
			sec = random.randrange(61, 71)
			print('Wait %d seconds for start. %s source(s) left.' % (sec, left))
			time.sleep(sec)

			self.comment(sourceid)
			nhandled += 1

		print("Finished!")

	def getSourceIds(self):
		"""
			get source ids wait for comment
		"""	
		self.sourceids = set()
		pagecount = self.getPageCount()
		if pagecount == 0:
			return False

		print('Pagecount is %d.' % pagecount)

		pattern = re.compile(r'.+/(\d+)#comment')

		for n in range(1, pagecount + 1):
			url = 'http://download.csdn.net/my/downloads/%d' % n
			html = self.getUrlContent(self.sess, url)
			if html is None:
				continue
			soup = BeautifulSoup(html, 'html.parser')
			sourcelist = soup.findAll('a', attrs={'class' : 'btn-comment'})
			if sourcelist is None:
				continue
			for source in sourcelist:
				href = source.get('href', None)
				if href is not None:
					rematch = pattern.match(href)
					print(rematch)
					if rematch is not None:
						self.sourceids.add(rematch.group(1))

		return len(self.sourceids) > 0					


	def getPageCount(self):
		"""
			get downloaded resources page count
		"""
		url = 'http://download.csdn.net/my/downloads'
		html = self.getUrlContent(self.sess, url)


		if html is None:
			print('Get pagecount failed')
			return 0
		soup = BeautifulSoup(html, 'html.parser')
		
		pagelist = soup.findAll('a', attrs={'class' : 'pageliststy'})
		if pagelist is None:
			return 0

		lasthref = pagelist[len(pagelist) - 1].get('href', None)
		# print(lasthref)
		if lasthref is None:
			return 0
		# return int(filter(str.isdigit, str(lasthref)))
		return int(re.findall(r"\d+\.?\d*", lasthref)[0])

	def comment(self, sourceid):
		"""
			comment per source
		"""	
		print('sourceid %s commenting...' % sourceid)
		comments = [
				'It just soso, but thank you all the same.',
				'Neither good nor bad.',
				'It is a nice resource, thanks for share.',
				'It is userful for me, thanks.',
				'I have looking this for long, thanks.'
		]
		rating = random.randrange(1, 6)
		content = comments[rating - 1]
		t = '%d' % (time.time() * 1000)

		paramsmap = {
				'sourceid' : sourceid,
				'content' : content,
				'rating' : rating,
				't' : t,
				'txt_validcode' : 'undefined'
		}

		params = urllib.parse.urlencode(paramsmap)
		url = 'http://download.csdn.net/index.php/comment/post_comment?%s' % params
		html = self.getUrlContent(self.sess, url)
		if html is None or html.find('({"succ":1})') == -1:
			print('sourceid %s comment failed! response is %s.' % (sourceid, html))
		else:
			print('sourceid %s comment succeed!' % sourceid)

	@staticmethod		
	def getElementValue(soup, element_name, element_value):
		element = soup.find(attrs={element_name : element_value})		
		if element is None:
			return None
		return element.get('value', None)

	@staticmethod	
	def isLoginSuccess(response):
		if response is None or response.status_code != 200:
			return False
		return -1 != response.text.find('lastLoginIP')

	@staticmethod	
	def getUrlContent(session, url):	
		html = None
		try:
			response = session.get(url)
			if response is not None:
				html = response.text
		except requests.exceptions.ConnectionError as e:
			traceback.print_exc()
			pass

		return html


def main():
	# help(requests.models.Response)
	csdn = CsdnCommenter()
	while csdn.login() is False:
		print('Login failed! Please try again.')
	print('Login succeed!')
	csdn.autoComment()

if __name__ == '__main__':
	main()