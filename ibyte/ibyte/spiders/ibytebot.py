# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import FormRequest
from ..items import IbyteItem


class IbytebotSpider(scrapy.Spider):
    name = 'ibytebot'
    allowed_domains = ['www.ibyte.com.br']
    start_urls = ['https://www.ibyte.com.br']

    def parse(self, response):
        self.log('Acessando página inicial - URL: %s' % response.url)
        return FormRequest.from_response(response, formid="search_mini_form", formdata={
        "q" : self.pesquisa
        }, callback=self.start_scraping)


    def start_scraping(self, response):

        self.log('Acessando resultado da pesquisa - URL: %s' % response.url)
        links_produtos = response.xpath("//h2[@class='product-name']/a/@href").extract()

        for link in links_produtos:
            yield scrapy.Request(link, self.produto)

        try:
            url_proxima_pagina = response.xpath("//li[@class='next']/a/@href").extract_first()

            self.log('Seguindo para próxima página.')

            yield scrapy.Request(url_proxima_pagina, self.start_scraping)

        except:
            self.log('Não existem mais páginas.')

    def produto(self, response):

        self.log('Acessando página do produto - URL: %s' % response.url)

        item = IbyteItem()
        item['url'] = response.url
        nome = response.xpath("//div[@class='product-name']/h1[@itemprop='name']/text()").extract_first()
        item['nome'] = nome
        codigo = response.xpath("//div[@id='info-secondaria']/span[@class='view-sku']/text()").extract_first()

        if(codigo is not None):
            item['codigo'] = codigo.split(': ')[1]

        preco = response.xpath("//div[@class='price-box']/p[@class='old-price']/span[@class='price']/text()").extract_first()

        if(preco is None):
            preco = response.xpath("//div[@class='price-box']/span[@class='regular-price']/span[@class='price']/text()").extract_first()
            preco_antigo = "0.0"
        else:
            preco_antigo = preco
            preco = response.xpath("//div[@class='price-box']/p[@class='special-price']/span[@class='price']/text()").extract_first()
            preco_antigo = preco_antigo.split('R$ ')[1]
            preco_antigo = preco_antigo.replace('.', '')

        preco = preco.split('R$ ')[1]
        preco = preco.replace('.', '')
        preco = preco.strip(" ")
        preco_antigo = preco_antigo.strip(" ")
        item['preco'] = float(preco.replace(',', '.'))

        if(preco_antigo!="0.0"):
            item['preco_antigo'] = float(preco_antigo.replace(',', '.'))
        else:
            item['preco_antigo'] = float(preco_antigo)

        descricao = response.xpath("//div[@id='descricao']/*[not(self::table) and not(self::img)]/text()").extract() #Remove a tabela e imagens da descrição

        descricao = list(map(str.strip, descricao))# Remove espaços e quebra de páginas
        descricao = list(filter(None, descricao))# Remove strings brancas da lista
        item['descricao'] = descricao

        item['garantia'] = response.xpath("//div[@class='infoEanGarantia']/b/text()").extract()


        caracteristicas = {}
        rows = response.xpath("//div[@id='descricao']/table/tbody/tr")
        for table_row in rows[1:]:
            col1 = table_row.xpath("td[2]/strong//text()").extract_first()
            col2 = table_row.xpath("td[3]//text()").extract_first()

            if(col1 is not None and col2 is not None):
                col1 = re.sub('\,|\?|\.|\!|\/|\;|\:', '', col1)
                caracteristicas[col1] = col2

        item['caracteristicas'] = caracteristicas

        yield item







