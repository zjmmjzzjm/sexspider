#! /usr/bin/python

import os
import sys
import socket
import urllib2
import datetime
import httplib
#from urlgrabber.keepalive import HTTPHandler

_DEBUG=False
#_DEBUG=True

def process_item(download_urls):
	#keepalive_handler = HTTPHandler()
	#opener = urllib2.build_opener(keepalive_handler)
	#urllib2.install_opener(opener)
	socket.setdefaulttimeout(60)
	if _DEBUG == True: 
		import pdb 
		pdb.set_trace() 
	for download_url in download_urls:
		try:
			torrent_response = None
			headers = {
			#GET /bbs/attachment.php?aid=2468324 HTTP/1.1
			'Host': '67.220.90.15',
			'Connection': 'close',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
			'Referer': 'http://67.220.90.15/bbs/thread-5749854-1-1.html',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'en-US,en;q=0.8',
			#'Cookie': 'cdb3_sid=dXBxPQ; cdb3_cookietime=2592000; cdb3_auth=aZ90%2BRlwBizNeGmnfhynFDdEYJLToMRQZp%2BiXN77cxih3PzfJFdHAK4irKTxByE5EsY; __utma=1.777934821.1400293657.1400506163.1400541553.8; __utmc=1; __utmz=1.1400293657.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
			'Cookie': 'cdb3_sid=dXBxPQ; cdb3_cookietime=2592000; cdb3_auth=aZ90%2BRlwBizNeGmnfhynFDdEYJLToMRQZp%2BiXN77cxih3PzfJFdHAK4irKTxByE5EsY;'
	
			}
			torrent_request = urllib2.Request(download_url, headers = headers)
			torrent_response = urllib2.urlopen(torrent_request)
			torrent_data = torrent_response.read()
			open('hah.torrent', 'wb').write(torrent_data)
			#torrent_conn = httplib.HTTPConnection('67.220.90.15')
			#torrent_conn.request("GET", "/bbs/attachment.php?aid=2468324", headers = headers)
			#torrent_data = torrent_conn.getresponse()
		except socket.timeout:
			print 'socket.timeout'
		#except Exception as e:
			#print 'other exception: ' + e
		finally:
			if torrent_response:
				torrent_response.close()

if __name__ == '__main__':
	process_item(['http://67.220.90.15/bbs/attachment.php?aid=2468324'])
	#process_item(['http://67.220.90.15/bbs/attachment.php?aid=2468324'])

'''
			'Host': '67.220.90.15',
			'Connection': 'keep-alive',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36',
			'Referer': 'http://67.220.90.15/bbs/thread-5749854-1-1.html',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'en-US,en;q=0.8',
			#'Cookie': 'cdb3_sid=dXBxPQ; cdb3_cookietime=2592000; cdb3_auth=aZ90%2BRlwBizNeGmnfhynFDdEYJLToMRQZp%2BiXN77cxih3PzfJFdHAK4irKTxByE5EsY; __utma=1.777934821.1400293657.1400506163.1400541553.8;__utmc=1; __utmz=1.1400293657.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
			'Cookie': 'cdb3_sid=8cG9Xa; cdb3_oldtopics=D5749854D; __utma=1.1066961665.1400586454.1400586454.1400589733.2; __utmz=1.1400586454.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cdb3_cookietime=315360000; cdb3_auth=Rkdya%2BKsOjFMnDhdAXaUIhSCeSUdcAGqqUnUfZIvDuhhEz9e5zX18Ojnh%2BNZJEurvIY; cdb3_fid318=1400243888; __utmc=1; __utmb=1.2.10.1400589733'
'''