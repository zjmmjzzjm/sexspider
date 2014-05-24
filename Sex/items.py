# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SexItem(Item):
    # define the fields for your item here like:
    # name = Field()
    # pass
    refer = Field()
    cookie = Field()
    title = Field()
    torrent_hash = Field()
    no_torrent_hash = Field()
    all_info = Field()
    image_right_srcs = Field()
    download_urls = Field()
