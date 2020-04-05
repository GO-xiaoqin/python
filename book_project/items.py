'''
@Author: your name
@Date: 2020-03-28 12:22:56
@LastEditTime: 2020-04-03 15:54:26
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\items.py
'''
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class dangdang_spiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authorpenname = scrapy.Field()
    price = scrapy.Field()
    categorys = scrapy.Field()


class douban_spiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author_price = scrapy.Field()
    book_tag = scrapy.Field()


class suning_spiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    catentdesc = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    tag_type = scrapy.Field()
