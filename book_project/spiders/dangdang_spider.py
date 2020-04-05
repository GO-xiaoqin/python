'''
@Author: your name
@Date: 2020-03-28 16:39:48
@LastEditTime: 2020-04-03 16:43:45
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\spiders\dangdang_spider.py
'''
# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import os
sys.path.append(os.getcwd() + "\\book_project")
from items import dangdang_spiderItem


class DangdangSpiderSpider(scrapy.Spider):
    name = 'dangdang_spider'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://e.dangdang.com/list-DZS-dd_sale-0-1.html']
    url = 'http://e.dangdang.com/media/api.go?action=mediaCategoryLeaf&start={}&end={}&category={}&dimension=dd_sale'

    def parse(self, response):
        # 对返回的response进行数据提取
        item_list = response.xpath("//ul/a/li")
        for i in item_list:
            item = {}
            item['data_type'] = i.xpath('./@data-type').get()
            item['dd_name'] = i.xpath('./@dd_name').get()
            url = self.url.format(0, 20, item['data_type'])
            # 先请求前20个数据
            yield scrapy.Request(url, callback=self.parse_item)
            # 要爬取全站图书就把break注释掉
            break

    def parse_item(self, response):
        # 提取数据
        dangdnag_spideritem = dangdang_spiderItem()
        responses = json.loads(response.text)
        # total = responses['data']['total'] 该行为获取每个小分类图书的总量
        saleList = responses['data']['saleList']
        for book in saleList:
            # 遍历每一本书提取信息
            dangdnag_spideritem['title'] = book['mediaList'][0]['title']
            dangdnag_spideritem['authorpenname'] = book['mediaList'][0]['authorPenname']
            dangdnag_spideritem['price'] = book['mediaList'][0]['price'] * 0.01
            dangdnag_spideritem['categorys'] = book['mediaList'][0]['categorys']
            yield dangdnag_spideritem
        if responses['status']['code'] == 0:
            # 处理下一页数据
            for i in range(21, responses['data']['total'], 20):
                url = self.url.format(i, i+19, responses['data']['code'])
                yield scrapy.Request(url, callback=self.parse_item)
        else:
            pass
