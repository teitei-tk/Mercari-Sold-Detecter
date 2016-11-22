# -*- coding: utf-8 -*-
import scrapy

from ..items import MercariSoldItem

class MercariSpider(scrapy.Spider):
    name = "mercari"
    allowed_domains = ["www.mercari.com"]
    domain = "http://www.mercari.com"
    start_urls = [
        'http://www.mercari.com/jp/category/11/'
    ]

    def parse(self, response):
        items = []

        for el in response.css('section.items-box'):
            # sold item check
            #if not el.css("div.item-sold-out-badge"):
            #   continue

            item = MercariSoldItem()
            item['url'] = el.css("a::attr(href)").extract_first()
            item['name'] = el.css("h3.items-box-name::text").extract_first()
            yield item

        # should be next pager link
        path = response.css("li.pager-num li:not(.active) > a::attr(href)").extract_first()
        if path:
            url = ''.join([self.domain, path])
            yield scrapy.Request(url, callback=self.parse)
