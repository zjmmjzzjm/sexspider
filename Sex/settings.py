# Scrapy settings for Sex project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Sex'

SPIDER_MODULES = ['Sex.spiders']
NEWSPIDER_MODULE = 'Sex.spiders'
ITEM_PIPELINES = {
	'Sex.pipelines.InfoPipeline': 100,
	'Sex.pipelines.HashPipeline': 200,
	'Sex.pipelines.TorrentDonwloadPipeline': 300,
	'Sex.pipelines.ImageDownloadPipeline': 400,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Sex (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'
COOKIES_ENABLED = True
COOKIES_DEBUG = True
