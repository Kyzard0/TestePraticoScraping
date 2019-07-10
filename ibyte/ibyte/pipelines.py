# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class IbytePipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        msg = 'Produtos adicionados ao MongoDB!'

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Produto Inválido {0}!".format(data))
        if valid:

            if item.get('codigo') in self.collection.distinct('codigo') and item.get('url', '') \
                    in self.collection.distinct('url'):
                raise DropItem("Produto Duplicado {0}".format(item['codigo']))

            elif(item.get('codigo') is None):
                raise DropItem("Produto Inválido {0}!".format(item['codigo']))

            elif not item.get('codigo') in self.collection.distinct('codigo'):
                log.msg(msg, level=log.DEBUG, spider=spider)
                self.collection.insert(dict(item))

        return item
