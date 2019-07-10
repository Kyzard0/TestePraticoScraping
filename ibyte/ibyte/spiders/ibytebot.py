# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from ..items import IbyteItem


class IbytebotSpider(scrapy.Spider):
    name = 'ibytebot'
    allowed_domains = ['www.ibyte.com.br']
    start_urls = ['https://www.ibyte.com.br']

    def parse(self, response):

        return FormRequest.from_response(response, formid="search_mini_form", formdata={
        "q" : self.pesquisa
        }, callback=self.start_scraping)


    def start_scraping(self, response):

        links_produtos = response.xpath("//h2[@class='product-name']/a/@href").extract()

        for link in links_produtos:
            yield scrapy.Request(link, self.produto)

        try:
            url_proxima_pagina = response.xpath("//li[@class='next']/a/@href").extract_first()
            print(url_proxima_pagina)

            yield scrapy.Request(url_proxima_pagina, self.start_scraping)

        except:
            self.log('Não existem mais páginas.')

    def produto(self, response):

        item = IbyteItem()

        item['url'] = response.url
        nome = response.xpath("//div[@class='product-name']/h1[@itemprop='name']/text()").extract_first()
        print(nome)
        item['nome'] = nome
        codigo = response.xpath("//div[@id='info-secondaria']/span[@class='view-sku']/text()").extract_first()

        if(codigo is not None):
            item['codigo'] = codigo.split(': ')[1]

        preco = response.xpath("//div[@class='price-box']/p[@class='old-price']/span[@class='price']/text()").extract_first()

        if(preco is None):
            preco = response.xpath("//div[@class='price-box']/span[@class='regular-price']/span[@class='price']/text()").extract_first()
            preco_antigo = 0.0
        else:
            preco_antigo = preco
            preco = response.xpath("//div[@class='price-box']/p[@class='special-price']/span[@class='price']/text()").extract_first()
            preco_antigo = preco_antigo.split('R$ ')[1]
            preco_antigo = preco_antigo.replace('.', '')

        preco = preco.split('R$ ')[1]
        preco = preco.replace('.', '')
        item['preco'] = float(preco.replace(',', '.'))

        if(float(preco_antigo)>0.0):
            item['preco_antigo'] = float(preco_antigo.replace(',', '.'))
        else:
            item['preco_antigo'] = preco_antigo

        item['descricao'] = response.xpath("//div[@id='descricao']/text()//*[not(child::table)]").extract()

        yield item







