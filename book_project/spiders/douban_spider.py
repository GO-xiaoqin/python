'''
@Author: your name
@Date: 2020-03-28 16:43:02
@LastEditTime: 2020-04-03 16:43:25
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\spiders\douban_spider.py
'''
# -*- coding: utf-8 -*-
import scrapy
import sys
import os
sys.path.append(os.getcwd() + "\\book_project")
from items import douban_spiderItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/']

    def parse(self, response):
        # 获取分类链接
        book_tags = response.xpath(
            "//div[@id='content']//b/../a/@href").extract()
        for book in book_tags:
            # print(response.urljoin(book))
            yield scrapy.Request(response.urljoin(book),
                                 callback=self.parse_item)
            # 要爬取全站图书就把break注释掉
            break

    def parse_item(self, response):
        douban_spideritem = douban_spiderItem()
        items = response.xpath('//div[@id="content"]')[0]
        book_tag = items.xpath('.//h1/text()').get()
        li_list = items.xpath('//div[@id="subject_list"]/ul//li')
        for li in li_list:
            # 循环一个页面书籍列表
            douban_spideritem['title'] = li.xpath('.//h2/a/text()').get()
            douban_spideritem['author_price'] = li.xpath('.//div[@class="pub"]/text()').get()
            douban_spideritem['book_tag'] = book_tag
            # 把每本书信息塞到管道进行处理
            yield douban_spideritem
        # 处理下一页链接
        next_href = response.xpath('//span[@class="next"]/a/@href')
        if len(next_href) > 0:
            # 还有下一页
            next_href = next_href.get()
            yield scrapy.Request(response.urljoin(next_href),
                                 callback=self.parse_item)
        else:
            pass
