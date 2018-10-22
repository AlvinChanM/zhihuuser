# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymsql

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # collection_name = item.__class__.__name__
        # 去重
        self.db['user'].update({'url_token':item['url_token']},{'$set':item}, True)
        return item

class ExamplePipeline(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host = self.settings['MYSQL_HOST'],
            user = self.settings['MYSQL_USER'],
            passwd = self.settings['MYSQL_PASSWD'],
            db = self.settings['MYSQL_DBNAME'],
            port = self.settings['MYSQL_PORT'],
            charset = 'utf8')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = "INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(table=self.settings['MYSQL_TABLE'], keys=keys, values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            if self.cur.execute(sql, tuple(data.values()) * 2):
                print('Save done!')
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
