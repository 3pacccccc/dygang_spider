# -*- coding: utf-8 -*-
import scrapy

from dygang.items import dygangitem
from scrapy.http import Request
from urllib import parse


class GydangSpider(scrapy.Spider):
    name = 'gydang'
    allowed_domains = ['http://www.dygang.net/']
    start_urls = ['http://www.dygang.net/ys/']    #爬取最新电影


    def parse(self, response):
        post_urls = response.css('.border1 a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail, dont_filter=True)

        #http://www.dygang.net/ys/index_2.htm

        for i in range(2, 100):
            next_page_url = 'http://www.dygang.net/ys/index_{}.htm'.format(i)
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)




    def parse_detail(self, response):
        title = response.css('.title a::text').extract()[0]  #获取电影的标题
        image_urls =  response.css('#dede_content img::attr(src)').extract()   #获取电影的相关图片


        #将相关数据载入到item中去
        item = dygangitem()
        item['title'] = title
        item['image_urls'] = image_urls
        return item

