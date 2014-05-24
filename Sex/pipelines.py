# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import socket
import urllib2
import datetime

import scrapy
from scrapy.exceptions import DropItem

_DEBUG=False
#_DEBUG=True

class InfoPipeline(object):
	def process_item(self, item, spider):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		if 'torrent_hash' in item:
			open('Info/With_Torrent_Page_Info/' + item['torrent_hash'] + '.txt', 'wb').write(item['all_info'])
		else:
			open('Info/No_Torrent_Pages_Info/' + item['no_torrent_hash'] + '.txt', 'wb').write(item['all_info'])
		#if _DEBUG == True: 
		#	import pdb 
		#	pdb.set_trace() 
		return item

class HashPipeline(object):
	def process_item(self, item, spider):
		if 'torrent_hash' in item:
			open('Hash/Hash.txt', 'ab').write(item['torrent_hash'] + '\n')
		return item

class TorrentDonwloadPipeline(object):
	def process_item(self, item, spider):
		#print "TorrentDonwloadPipeline"
		if 'download_urls' in item:
			socket.setdefaulttimeout(80)
			#if _DEBUG == True: 
			#	import pdb 
			#	pdb.set_trace() 
			for download_url in item['download_urls']:
				try:
					torrent_response = None
					headers = {
						'Host': '67.220.90.15',
						'Connection': 'close',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
						'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
						'Referer': item['refer'],
						'Accept-Encoding': 'gzip,deflate,sdch',
						'Accept-Language': 'en-US,en;q=0.8',
						#'Cookie': 'cdb3_sid=dXBxPQ; cdb3_cookietime=2592000; cdb3_auth=aZ90%2BRlwBizNeGmnfhynFDdEYJLToMRQZp%2BiXN77cxih3PzfJFdHAK4irKTxByE5EsY; __utma=1.777934821.1400293657.1400506163.1400541553.8;__utmc=1; __utmz=1.1400293657.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
						'Cookie': item['cookie']
					}
					torrent_request = urllib2.Request(download_url, headers = headers)
					torrent_response = urllib2.urlopen(torrent_request)
					torrent_data = torrent_response.read()
					if 'torrent_hash' in item:
						if os.path.exists('Torrent/' + item['torrent_hash'] + '.torrent'):
							open('Torrent/' + item['torrent_hash'] + "_" + str(datetime.datetime.now().microsecond) + '.torrent', 'wb').write(torrent_data)
						else:
							open('Torrent/' + item['torrent_hash'] + '.torrent', 'wb').write(torrent_data)
					else:
						if os.path.exists('Torrent/' + item['no_torrent_hash'] + '.torrent'):
							open('Torrent/' + item['no_torrent_hash'] + "_" + str(datetime.datetime.now().microsecond) + '.torrent', 'wb').write(torrent_data)
						else:
							open('Torrent/' + item['no_torrent_hash'] + '.torrent', 'wb').write(torrent_data)
				except socket.timeout:
					open('Log/Error_Download_Timeout_Torrents.log', 'ab').write(download_url + '\n')
				except Exception, e:
					open('Log/Error_Download_UnKownReason_Torrents.log', 'ab').write(e)
				else:
					open('Log/DownloadedTorrent.log', 'ab').write(download_url + '\n')
				finally:
					if torrent_response:
						torrent_response.close()

				if _DEBUG == True: 
					import pdb 
					pdb.set_trace() 
		return item

class ImageDownloadPipeline(object):
	def process_item(self, item, spider):
		if 'image_right_srcs' in item:
			if 'torrent_hash' in item:
					open('Image/Img_Src/' + item['torrent_hash'] + '.txt', 'wb').write(item['image_right_srcs'])
			else:
					open('Image/Img_Src/' + item['no_torrent_hash'] + '.txt', 'wb').write(item['image_right_srcs'])
		return item