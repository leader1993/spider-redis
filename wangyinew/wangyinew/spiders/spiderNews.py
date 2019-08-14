# -*- coding: utf-8 -*-
import scrapy
#导入分布式工具包
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from wangyinew.wangyinew.items import WangyinewItem
class SpidernewsSpider(RedisSpider):
    name = 'spiderNews'
    #allowed_domains = ['http://news.163.com/']
    #start_urls = ['http://news.163.com/']
    redis_key = 'wangyi'

    def __init__(self):
    #实例化无界面浏览器
        self.brower = webdriver(executable_path='C:\\soft\\phantomjss\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

    def close(self, spider):
        #爬虫结束
        print('爬虫运行结束')
        self.brower.quit()
    #获取板块链接
    def parse(self, response):
        lis = response.xpath('')
        indexs = [3,4,6,7]
        li_list = []
        for index in indexs:
            li_list.append(lis[index])
        #获取板块的链接和文字标题
        for li in li_list:
            url = li.xpath('').extract()
            title = li.xpath('').extract()
            print(url+'::'+title)

            #对每一个板块对应url请求，获取页面
            yield scrapy.Request(url=url,callback=self.parseData,meta={'title':title})

    def parseData(self,response):
        div_list = response.xpath("//div[@class='data_row news_article clearfix']")
        # print(len(div_list))
        for div in div_list:
            head = div.xpath('.//div[@class="news_title"]/h3/a/text()').extract_first()
            url = div.xpath('.//div[@class="news_title"]/h3/a/@href').extract_first()
            imgUrl = div.xpath('./a/img/@src').extract_first()
            tag = div.xpath('.//div[@class="news_tag"]//text()').extract()
            tags = []
            for t in tag:
                t = t.strip(' \n \t')
                tags.append(t)
            tag = "".join(tags)

            # 获取meta传递过来的数据值title
            title = response.meta['title']

            # 实例化item对象，将解析到的数据值存储到item对象中
            item = WangyinewItem()
            item['head'] = head
            item['url'] = url
            item['imgUrl'] = imgUrl
            item['tag'] = tag
            item['title'] = title

            # 对url发起请求，获取对应页面中存储的新闻内容数据
            yield scrapy.Request(url=url, callback=self.getContent, meta={'item': item})

    def getContent(self, response):
        # 获取传递过来的item
        item = response.meta['item']

        # 解析当前页面中存储的新闻数据
        content_list = response.xpath('//div[@class="post_text"]/p/text()').extract()
        content = "".join(content_list)
        item['content'] = content

        yield item