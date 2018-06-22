# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymysql
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from db_access import *



class ClassicPipeline(object):
    def open_spider(self, spider):
        self.fp = open('book.txt', 'w', encoding='utf8')

    def process_item(self, item, spider):
        obj = dict(item)
        string = json.dumps(obj, ensure_ascii=False)
        self.fp.write(string + '\n')
        print('&' * 30)
        return item

    def close_spider(self, spider):
        self.fp.close()


# class DushuMongoPipeline(object):
#     def open_spider(self, spider):
#         self.conn = MongoClient(host='127.0.0.1', port=27017)
#         db = self.conn.dushu
#         self.mysheet = db.book
#         print('写入MongoDB**********************')
#
#     def close_spider(self, spider):
#         self.conn.close()
#
#     def process_item(self, item, spider):
#         self.mysheet.insert(dict(item))


class ClassicMysqlPipeline(object):
    def process_item(self, item, spider):
        info = {
            "title": item['title'],
            "url": item['url'],
            "img_url": item['image_url']
        }
        result = create_imagUrl(**info)
        return item
