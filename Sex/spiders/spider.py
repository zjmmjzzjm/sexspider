import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.cookies import CookieJar
from scrapy.selector import Selector
from Sex.items import SexItem

import datetime
import urllib2
import exceptions
#import socket
import string
import datetime
import time
import sys
import re

from killhtmltags import *

_DEBUG=False
#_DEBUG=True

class kaisouSpider(CrawlSpider):
	name = 'sexinsex'
	allowed_domains = ['67.220.90.15']
	start_urls = [
		#'http://67.220.90.15/bbs/thread-5715209-1-1.html',
		#'http://67.220.90.15/bbs/thread-5749352-1-1.html'
	]

	rules = [Rule(SgmlLinkExtractor(allow=['thread.+\.html']), 'get_movie_item')]
	rules = [Rule(SgmlLinkExtractor(allow=['forum.+\.html']), 'get_movie_page')]
	#rules = [Rule(SgmlLinkExtractor(allow=['/tag/.+']), 'get_movie_page')]
	# the rules will be flushed

	def start_requests(self):
		return [scrapy.http.FormRequest("http://67.220.90.15/bbs/logging.php?action=login&loginsubmit=true",
						formdata={'formhash':'6e09b927', 'cookietime':'2592000', 'loginfield':'username', 'username':'999snake999', 'password':'tteesstt9', 'userlogin':'true'},
						callback=self.logged_in
					)
				]

	def get_complete_url(self, url):
		return "http://67.220.90.15/bbs/"+url

	def get_movie_pages(self, response):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		sel = Selector(response)
		tags = sel.xpath('//*[@id="container"]//div[1]/a/@href').extract()
		#if _DEBUG == True: 
		#	import pdb 
		#	pdb.set_trace() 
		for tag in tags:
		#	if _DEBUG == True: 
		#		import pdb 
		#		pdb.set_trace() 
			yield self.make_requests_from_url(self.get_complete_url(tag))

	def get_movie_page(self, response):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		open('Pages/CrawledNextPages.log', 'ab').write(response.url + '\n')
		sel = Selector(response)
		next_pages = sel.xpath('//*[@class="pages"]/a/@href').extract()
		#if _DEBUG == True: 
		#		import pdb 
		#		pdb.set_trace() 
		#print next_pages
		item_pages = sel.xpath('//*[@class="folder"]/a/@href').extract()
		#open('Pages/Subpages.log', 'ab').write('\n'.join(next_pages))
		for next_page in next_pages:
		#	print self.get_complete_url(next_page)
		#	yield scrapy.http.Request(self.get_complete_url(next_page), callback=self.get_movie_page)
		#	if _DEBUG == True: 
		#		import pdb 
		#		pdb.set_trace() 
			open('Pages/NextPages.log', 'ab').write(response.url + '\n')
			yield self.make_requests_from_url(self.get_complete_url(next_page))
		for item_page in item_pages:
			item_page = self.get_complete_url(item_page)
			print item_page
			open('Pages/ItemPages.log', 'ab').write(item_page + '\n')
			yield scrapy.http.Request(item_page, callback=self.get_movie_item)
			#yield self.make_requests_from_url(item_page)
			# here can't use make_requests_from_url, i think cause we can't find href in the page 


	def get_movie_item(self, response):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		self.log("get_movie_item just arrived! %s" % response.url)
		open('Pages/CrwaledSinglePages.log', 'ab').write(response.url + '\n')
		torrent = SexItem()
		print 'get_movie_item: ' + response.url
		sel = Selector(response)
		torrent_urls = sel.xpath('//*[@class="box postattachlist"]//a/@href').extract()
		image_srcs = sel.xpath('//*[@class="t_msgfont"]//img/@src').extract()
		try:
			title = sel.xpath('//*[@class="postmessage defaultpost"]//h2/text()')[0].extract()
		except exceptions.IndexError:
			open('Log/ErrorParsedPages.log', 'ab').write(response.url + '\n')
			return

		torrent['title'] = title
		torrent['refer'] = response.url
		#cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
		#cookieJar.extract_cookies(response, response.request)
		#torrent['cookie'] = cookieJar._cookies
		torrent['cookie'] = response.request.headers['Cookie']
		if _DEBUG == True: 
			import pdb 
			pdb.set_trace() 

		#for cookie in cookieJar:
		#	torrent['cookie'].append(cookie)

		image_right_srcs = ''
		image_item_srcs  = []
		for image_src in image_srcs:
			if image_src.find('.jpg') != -1:
				image_right_srcs += image_src + '\n'
				image_item_srcs.append(image_src)
		torrent['image_right_srcs'] = image_right_srcs
		page_info = ''.join(sel.xpath('//*[@class="t_msgfont"]')[0].extract())
		page_info = ''.join(page_info.split('\t'))
		page_info = filter_tags(page_info)

		if_get_hash = re.search(r'[0-9a-zA-Z]{40}', page_info)
		#if _DEBUG == True: 
		#		import pdb 
		#		pdb.set_trace()
		if if_get_hash:
			torrent_hash = if_get_hash.group(0)
			torrent['torrent_hash'] = torrent_hash
		else:
			torrent_hash = "NoHash_" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())) + "_" + str(datetime.datetime.now().microsecond)
			torrent['no_torrent_hash'] = torrent_hash

		if (torrent_urls.__len__() == 0):
			all_info = '#!Title: ' + title + '\n\n' + '#!Torrent Info: ' + page_info + '\n\n'+ '#!Images: \n' + image_right_srcs + '\n\n!Original URL: ' + response.url
			torrent['all_info'] = all_info
		else:
			download_urls = ''
			download_item_urls = []
			for torrent_url in torrent_urls:
				if torrent_url.find('attachment.php') != -1:
					if torrent_url[-1] in string.digits:
						download_urls +=  self.get_complete_url(torrent_url) + '\n'
						download_item_urls.append(self.get_complete_url(torrent_url))
						#scrapy.http.Request(self.get_complete_url(torrent_url))
			all_info = '#!Title: ' + title + '\n\n'  + '#!Torrent Info: ' + page_info + '\n\n'+ '#!Images: \n' + image_right_srcs + '\n\n' + '#!Download: ' + download_urls + '\n\n#!Original URL: ' + response.url 
			torrent['download_urls'] = download_item_urls
		torrent['all_info'] = all_info

		return torrent

	#def parse_start_url(self, response):
	#def parse(self, response):
	#	self.log("parse_category just arrived! %s" % response.url)
		#if _DEBUG == True: 
		#		import pdb 
		#		pdb.set_trace() 
	#	return self.get_movie_item(response)

	def logged_in(self, response):
		self.log("logged_in just arrived! %s" % response.url)
		yield self.make_requests_from_url("http://67.220.90.15/bbs/forum-318-1.html")
		#yield self.make_requests_from_url("http://67.220.90.15/bbs/thread-5749854-1-1.html", meta={'cookiejar': response.meta['cookiejar']},)