# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from classicMonments.spider.items import ClassicItem

class ClassicSpider(CrawlSpider):
    name = 'ClassicSpider'
    allowed_domains = ['www.gov.cn','sousuo.gov.cn']
    start_urls = ['http://www.gov.cn/premier/index.htm']
    # 规则是一个元组，可以写多个规则，每一个对着就是Rule对象，
    # 参数1：LinkExtractor(allow=r'Items/')链接提取器
    # 参数2：回调，处理链接提取器提取的url的响应结果，
    # callback=方法名，和Spider不同
    # 参数3：跟进，是否要接着按照这个规则进行提取链接
    #//*[@id="public_chckmore"]/a
    rules = (
        Rule(LinkExtractor(allow='/premier/*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='http://sousuo.gov.cn/column/.*'), follow=True),
    )

    def parse_item(self, response):
        content = response.xpath('//div[@class="article oneColumn pub_border"]')
        item = ClassicItem()
        item['url'] = response.url
        item['title'] = content.xpath('h1/text()').extract_first()
        item['image_url'] = content.xpath('div[@class="pages_content"]/p/img/@src').extract_first()
        if item['image_url']:        
            item['image_url'] = re.sub(r'[^\/]+$','',response.url) + item['image_url']
            return item;
        else:
            return
        


    def parse_info(self,response):
        item = response.meta['item']
        #获取其他信息
        item['book_price'] = response.xpath('//div[@class="book-details"]//span/text()').extract_first()
        #简介
        item['book_info'] = response.xpath('//div[@class="book-summary"]/div/div/text()').extract_first()
        item['book_publish'] = response.xpath('//div[@class="book-details"]//table//tr[2]/td[2]/a/text()').extract_first()
        yield item


