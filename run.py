'''
@Author: your name
@Date: 2020-03-29 13:37:31
@LastEditTime: 2020-03-29 14:12:54
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \python\book_project\book_project\run.py
'''

from scrapy import cmdline

cmd = 'scrapy crawl dangdang_spider'
cmdline.execute(cmd.split())
