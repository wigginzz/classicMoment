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

    def __init__(self, keywords=None,*a, **kw):
        super(ClassicSpider, self).__init__(*a, **kw)
        self.__keywords = keywords

    def parse_item(self, response):
        content = response.xpath('//div[@class="article oneColumn pub_border"]')
        item = ClassicItem()
                
        keywords = self.__keywords;
        pattern =  keywords[0]
        for key in range(1,len(keywords),1):
            pattern = pattern + '|' + keywords[key]
    
        news_conntent = content.xpath('div[@class="pages_content"]/p/text()').extract()
        match = re.findall(pattern,''.join(news_conntent))            
        if len(match):
            imgUrls = content.xpath('div[@class="pages_content"]/p/img/@src').extract()
            for imgurl in imgUrls:
                item['url'] = response.url
                item['title'] = content.xpath('h1/text()').extract_first()
                
                item['image_url'] = re.sub(r'[^\/]+$','',response.url) + imgurl
                yield item;
        


