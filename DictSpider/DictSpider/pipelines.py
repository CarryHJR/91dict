# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pq

class DictspiderPipeline(object):
    def __init__(self):
        self.conn = pq.connect(host='localhost', user='root',
                passwd='123456', db='renrendict', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        word = item['word']
        sentence = item['sentence']
        files = item['files']
        image = files[0]['path']
        audio = files[1]['path']
        sql = "insert into dict(image, word, sentence, audio) VALUES (%s, %s, %s, %s)"
        self.cur.execute(sql, (image, word, sentence, audio))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
