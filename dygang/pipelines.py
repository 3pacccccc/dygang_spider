# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class DygangPipeline(object):
    def process_item(self, item, spider):
        return item



class dygangimagepipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url=image_url, meta={'item': item})



    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
           raise DropItem('item contains no images')

        return item


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']

        image_guid = request.url.split('/')[-1]
        filenames = 'full/%s/%s' %(item['title'], image_guid)

        return filenames