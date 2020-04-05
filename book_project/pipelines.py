'''
@Author: your name
@Date: 2020-03-28 12:22:56
@LastEditTime: 2020-04-03 16:53:10
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\pipelines.py
'''
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo
import re
import sys
import os
sys.path.append(os.getcwd() + "\\book_project")
from items import dangdang_spiderItem, douban_spiderItem, suning_spiderItem


class BookProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class suning_spiderPipeline(object):
    """
    对豆瓣爬虫进行数据处理
    """
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            host=spider.settings.get('MONGO_HOST'),
            port=spider.settings.get('MONGO_PORT'),
        )
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(
        #     settings['MINGO_USER'], 
        #     settings['MONGO_PSW']
        #     )
        self.db = self.client[spider.settings.get('MONGO_DB')]  # 获得数据库的句柄
        self.coll = self.db['suning_spider_book']  # 获得collection的句柄

    def process_item(self, item, spider):
        """
        进行判断，如果进来的item是豆瓣的数据就进行数据处理存储，
        不然就跳过数据
        """
        if spider.name == 'suning_spider' and isinstance(item, suning_spiderItem):
            # 把进来的item数据进行清洗处理
            book = {}
            book['title'] = item['catentdesc']
            book['author'] = item['author']
            book['price'] = item['price']
            book['type'] = item['tag_type']
            self.coll.insert(book)  # 向数据库插入一条记录,要插入字典
            # print(item)
        return item


class douban_spiderPipeline(object):
    """
    对豆瓣爬虫进行数据处理
    """
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            host=spider.settings.get('MONGO_HOST'),
            port=spider.settings.get('MONGO_PORT'),
        )
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(
        #     settings['MINGO_USER'], 
        #     settings['MONGO_PSW']
        #     )
        self.db = self.client[spider.settings.get('MONGO_DB')]  # 获得数据库的句柄
        # 获得collection的句柄
        # self.coll = self.db[spider.settings.get('MONGO_COLL')]  
        self.coll = self.db['douban_spider_book']

    def process_item(self, item, spider):
        """
        进行判断，如果进来的item是豆瓣的数据就进行数据处理存储，
        不然就跳过数据
        """
        if spider.name == 'douban_spider' and isinstance(item, douban_spiderItem):
            # 把进来的item数据进行清洗处理
            book = {}
            book['title'] = item['title'].split()[0]
            # 这个地方还要做一下处理
            pattern = re.compile(r'（.）|\[.\]|\(.\)')
            author_price = [x.split() for x in item['author_price'].split("/")]
            author = author_price[0]
            if len(author) > 0:
                if len(pattern.findall(author[0])) > 0:
                    if author[0] == pattern.findall(author[0])[0]:
                        author = author[0] + author[1]
                else:
                    author = author[0]
            else:
                author = ''
            book['author'] = author
            book['price'] = author_price[-1][0]
            book['tag'] = item['book_tag'].split(":")[1]
            self.coll.insert(book)  # 向数据库插入一条记录,要插入字典
            # print(item)
        return item


class dangdnag_spiderPipeline(object):
    """
    对当当爬虫进行数据处理
    """
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn = pymysql.connect(
            host=host,
            port=port,
            db=db,
            user=user,
            passwd=passwd,
            charset='utf8',
            )
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库

    def process_item(self, item, spider):
        # 对spider，item进行判断
        if spider.name == 'dangdang_spider' and isinstance(item, dangdang_spiderItem):
            self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        values = (
            item['title'],
            item['authorpenname'],
            item['price'],
            item['categorys'],
        )
        sql = 'INSERT INTO dangdang_books(title,authorpenname,price,categorys) VALUES(%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
