'''
@Author: your name
@Date: 2020-03-28 16:42:45
@LastEditTime: 2020-04-03 17:56:03
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\spiders\suning_spider.py
'''
# -*- coding: utf-8 -*-
import scrapy
import re
import json
import sys
import os
sys.path.append(os.getcwd() + "\\book_project")
from items import suning_spiderItem


class SuningSpiderSpider(scrapy.Spider):
    name = 'suning_spider'
    allowed_domains = ['suning.com']
    start_urls = ['http://lib.suning.com/api/jsonp/cb/KfQ-cmsJsonpApi.jsonp']
    url = 'https://search.suning.com/emall/mobile/wap/clientSearch.jsonp?keyword={}&channel=99999972&cp={}&ps=10&set=5&ct=-1&v=99999999'
    tag_name = ''

    def parse(self, response):
        # 对类别名称进行提取
        pattern = re.compile(r'\(.*\)')
        response_item = pattern.findall(response.body_as_unicode())
        # 使用正则提取网页中的数据，对数据进行预处理
        response_eval = eval(response_item[0])
        # 处理后的数据为list
        # 获取分类信息的字典
        for d in response_eval:
            if d.__contains__('fl8p_bt'):
                response_dict_list = d['fl8p_bt']['nodes'][0]['tag']
                for url_dict in response_dict_list:
                    url_name = url_dict['linkUrl']
                    pattern = re.compile(r'https://m\.suning\.com/search/(.*?)/&')
                    global tag_name
                    self.tag_name = pattern.findall(url_name)[0]
                    # 已经获取到URL的类别名称，开始构造URL
                    # 构造一个一页十个的URL
                    stat_url = self.url.format(self.tag_name, 0)
                    # 返回到下一页函数进行数据提取
                    yield scrapy.Request(stat_url, callback=self.parse_item)
                    # 要爬取全站图书就把break注释掉
                    break

    def parse_item(self, response):
        response_json = json.loads(response.text)
        # 进行判断是否有返回数据
        if len(response_json['errorCode']) == 0:
            # 进行数据提取及下一页请求
            suning_spideritem = suning_spiderItem()
            book_list = response_json['goods']
            for book in book_list:
                # 对每本书的数据进行提取
                suning_spideritem['catentdesc'] = book['catentdesc']
                suning_spideritem['author'] = book['author'] if len(book['author']) > 0 else None
                suning_spideritem['price'] = book['price']
                suning_spideritem['tag_type'] = self.tag_name
                yield suning_spideritem
            '''
            构造下一页URL，构造一个生成器,
            这的601是根据分析页面获得的结果，这里可以随便设定，
            尽量大一点要比六百大，因为苏宁这个网站最多返回六千个数据
            '''
            for x in range(1, 601):
                next_url = self.url.format(self.tag_name, x)
                yield scrapy.Request(next_url, callback=self.parse_item)
        else:
            pass
