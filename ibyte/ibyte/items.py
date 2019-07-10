# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IbyteItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    nome = scrapy.Field()
    codigo = scrapy.Field()
    preco = scrapy.Field()
    preco_antigo = scrapy.Field()
    descricao = scrapy.Field()
    imagens = scrapy.Field
    caracteristicas = scrapy.Field()
    garantia = scrapy.Field()
