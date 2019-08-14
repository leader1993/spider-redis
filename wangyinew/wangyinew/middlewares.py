# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

import random
#UA池代码的编写（单独给UA池封装一个下载中间件的一个类）
#1，导包UserAgentMiddlware类
class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        #从列表中随机抽选出一个ua值
        user_agent = random.choice(user_agent_list)
        #ua值进行当前拦截到请求的ua的写入操作
        request.headers.setdefault('User-Agent',user_agent)

#批量对拦截到的请求进行ip更换
class Proxy(object):
    def process_request(self, request, spider):
        #对拦截到请求的url进行判断（协议头到底是http还是https）
        #request.url返回值：http://www.xxx.com
        h = request.url.split(':')[0]  #请求的协议头
        if h == 'https':
            ip = random.choice(PROXY_https)
            request.meta['proxy'] = 'https://'+ip
        else:
            ip = random.choice(PROXY_http)
            request.meta['proxy'] = 'http://' + ip

PROXY_http = [
    '153.180.102.104:80',
    '195.208.131.189:56055',
]
PROXY_https = [
    '120.83.49.90:9000',
    '95.189.112.214:35508',
]
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"]


class WangyinewSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WangyinewDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # 响应对象中存储页面数据的篡改
        if request.url in ['http://news.163.com/domestic/', 'http://news.163.com/world/', 'http://news.163.com/air/',
                           'http://war.163.com/']:
            spider.bro.get(url=request.url)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            spider.bro.execute_script(js)
            time.sleep(2)  # 一定要给与浏览器一定的缓冲加载数据的时间
            # 页面数据就是包含了动态加载出来的新闻数据对应的页面数据
            page_text = spider.bro.page_source
            # 篡改响应对象
            return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding='utf-8', request=request)
        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
