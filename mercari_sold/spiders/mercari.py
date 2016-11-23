# -*- coding: utf-8 -*-
import scrapy

from ..items import MercariSoldItem

class MercariSpider(scrapy.Spider):
    name = "mercari"
    allowed_domains = ["www.mercari.com", 'item.mercari.com']
    domain = "https://www.mercari.com"
    start_urls = (
        # レディース
        'https://www.mercari.com/jp/category/1/',
        # メンズ
        'https://www.mercari.com/jp/category/2/',
        # ベビー・キッズ
        'https://www.mercari.com/jp/category/3/',
        # インテリア小物
        'https://www.mercari.com/jp/category/4/',
        # エンタメ
        'https://www.mercari.com/jp/category/5/',
        # コスメ
        'https://www.mercari.com/jp/category/6/',
        # 家電
        'https://www.mercari.com/jp/category/7/',
        # スポーツ
        'https://www.mercari.com/jp/category/8/',
        # ハンドメイド
        'https://www.mercari.com/jp/category/9/',
        # チケット
        'https://www.mercari.com/jp/category/1027/',
        # 自転車
        'https://www.mercari.com/jp/category/1318/',
        # その他
        'https://www.mercari.com/jp/category/10/',
    )

    def parse_detail(self, response):
        item = response.meta['item']
        item['title'] = response.css("h2.item-name::text").extract_first()
        item['categories'] = response.css("table.item-detail-table tr:nth-child(2) a div::text").extract()
        item['price'] = response.css("span.item-price::text").extract_first().__str__().strip("¥ ")
        item['shipping_fee'] = response.css("span.item-shipping-fee::text").extract_first()
        item['description'] = ''.join([x.strip() for x in response.css("div.item-description::text").extract()])

        if not item['title']:
            yield
        else:
            yield item

    def parse(self, response):
        items = []

        for el in response.css('section.items-box'):
            # sold item check
            if el.css("figure.items-box-photo > figcaption > div.item-sold-out-badge"):
                item = MercariSoldItem()
                item['url'] = detail_url = el.css("a::attr(href)").extract_first()

                request = scrapy.Request(detail_url, callback=self.parse_detail)
                request.meta['item'] = item
                yield request

        # should be next pager link
        path = response.css("li.pager-cell.active + li > a::attr(href)").extract_first()
        if path:
            url = ''.join([self.domain, path])
            yield scrapy.Request(url, callback=self.parse)
