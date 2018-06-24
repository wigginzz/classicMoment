#!/usr/bin/env python
#-*-coding:utf-8-*-
import time
#import logging


from twisted.internet import reactor  
from scrapy.crawler import CrawlerRunner  
from scrapy.settings import Settings  

from classicMonments.spider.spiders.ClassicSpider import ClassicSpider


def run(keyword):
    try:
        res = {"success": False, "msg": ""}
        settings = Settings({
    	#Spiders can still be referenced by their name if SPIDER_MODULES is set with the modules where Scrapy should look for spiders.  
	    #Otherwise, passing the spider class as first argument in the CrawlerRunner.  
	    'SPIDER_MODULES':['classicMonments.spider.spiders.ClassicSpider'],    
	    'ROBOTSTXT_OBEY':False,
	    #设置包头  
	    'DEFAULT_REQUEST_HEADERS':{    
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'},  
	    #启用pipelines组件  
	    'ITEM_PIPELINES':{  
	    'classicMonments.spider.pipelines.ClassicPipeline': 300,
		'classicMonments.spider.pipelines.ClassicMysqlPipeline': 302,},      
	    })
        runner=CrawlerRunner(settings)  
        d=runner.crawl(ClassicSpider,keywords=keyword)  
        d.addBoth(lambda _: reactor.stop()) 
        reactor.run() 

        res["success"] = True
        return res
    except Exception as e:
        res["msg"] = "创建出错"
        return res


if __name__ == "__main__":
    run(['日本'])
