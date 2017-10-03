#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 17:32:17 2017

@author: toni
-----------------------------------------------------------------------
Script final que realiza una conversion a csv del horario de la UIB
dentro de las fechas que nosotros designemos.
-----------------------------------------------------------------------
"""
import scrapy
import getpass

import pandas as pd
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Join, MapCompose

class AsiItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()

class AsiItem(scrapy.Item):
    Subject = scrapy.Field()
    Start_Date = scrapy.Field()
    Start_Time = scrapy.Field()
    End_Date = scrapy.Field()
    End_Time = scrapy.Field()
    Location = scrapy.Field()
    All_Day_Event = scrapy.Field()

class LoginSpider(scrapy.Spider):

    name = 'calendar'
    start_urls = ['https://uibdigital.uib.es/uibdigital/intern/categoria/inici.html']

    def parse(self, response):

        user_name = raw_input('user name: ')
        pw = getpass.getpass()
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': user_name, 'password': pw},
            formxpath='//*[@id="fm1"]',
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            # self.logger.error("Login failed")
            self.log("Login failed", level=log.ERROR)
            return
        # print response.url
        else:
            yield scrapy.Request(url="https://uibdigital.uib.es/uibdigital/estudis/horaris/informacio.html",callback=self.after_login_page)

    def after_login_page(self, response):
        # continue scraping with authenticated session...
        #print response.text
        lista=[]
        frase_a="/uibdigital/estudis/horaris/cronograma/setmana/"
        frase_b="/consultar.html"
        dates = pd.date_range('09-10-2017', periods=80, freq='W')
        print dates

        for i in dates:
           frase_aux= frase_a+str(i.strftime('%Y%m%d'))+frase_b
           lista.append(frase_aux)
        #para cada uno de las fechas.
        for i in lista:
            new_page_url = response.urljoin(i)
            yield scrapy.Request(url=new_page_url,callback=self.extraer_elemento_semanal)
            
    def extraer_elemento_semanal(self, response):
        #Estamos dentro de una semana.
        #meterse en cada uno de los elementos action
        url_aux= response.css('div.actions >a::attr(href)').extract()
        #para cada uno de los elementos action
        for i in url_aux:
            i= response.urljoin(i)
            yield scrapy.Request(url=i,callback=self.extraer_datos_asignatura)
            
            
    def extraer_datos_asignatura(self, response):
        loader= AsiItemLoader(item=AsiItem(), selector=response)
        #Añadir asignatura
        loader.add_xpath('Subject','//*[@id="information"]/div/h2/text()')
        #Añadir Fecha y hora inicial
        string=response.xpath('//*[@id="information"]/div/fieldset[1]/div/div[1]/div[2]/text()').extract_first()
        lista= string.split()
        loader.add_value('Start_Date',lista[0])
        if 2==len(lista):
            loader.add_value('Start_Time',lista[1])
        string=response.xpath('//*[@id="information"]/div/fieldset[1]/div/div[2]/div[2]/text()').extract_first()
        lista= string.split()
        #Añadir fecha y hora final
        if string == '-':#se trata de un evento que dura todo el día
            loader.add_value('End_Date','')
            loader.add_value('All_Day_Event','True')
        else:
            loader.add_value('End_Date',lista[0])
            loader.add_value('All_Day_Event','False')
        if 2==len(lista):
            loader.add_value('End_Time',lista[1])
        #Añadir lugar
        loader.add_xpath('Location','//*[@id="information"]/div/fieldset[1]/div/div[5]/div[2]/text()')

        #cargar el item
        yield loader.load_item()
        