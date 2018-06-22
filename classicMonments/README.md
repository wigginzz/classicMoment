### crawl spider

- 是一个类，继承自Spider，Spider是scrapy里面爬虫的一个基类，CrawlSpider是scrapy封装的另外一个爬虫类，由于CrawlSpider是Spider的子类，所以功能要比Spider要多
- 多了一个功能：提取链接的功能，根据一定的规则直接在该网页中提取符合这个规则的所有链接
- LinkExtractor ：链接提取器

	```scrapy.linkextractors.LinkExtractor(
	    allow = (),            # 正则表达式
	    allow_domains = (),    # 允许的域名（了解）
	    deny_domains = (),     # 不允许的域名（了解）
	    restrict_xpaths = (),  # 根据xpath提取链接
	    retrict_css = ()       # 根据选择器提取链接
	)```

- 通过scrapy shell演示链接的提取
	- 正则提取

			```'list_23_\d.html'
			from scrapy.linkextractors import LinkExtractor
			link = LinkExtractor(allow=r'list_23_\d+\.html')
			打印提取
			link.extract_links(response)```
	- xpath提取
			link = LinkExtractor(restrict_xpaths='//div[@class="x"]')
			【注】xpath路径，不用精确到a，精确到上一级，自动会去div中查找所有的a
	- css提取
			link = LinkExtractor(restict_css='.x')
			不用精确到a，查找的是所有class是x下面的a链接

	- 通过规则，只要提取链接成功，scrapy就会自动的发送这些请求，我们不用管这个，我们只需要关注提取指定规则的链接即可
	实例：
		添加参数，生成CrawlSpider的模板
		```scrapy genspider -t crawl du "www.dushu.com"```
