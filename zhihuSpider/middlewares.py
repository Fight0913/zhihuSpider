# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests


class ZhihuspiderSpiderMiddleware(object):
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

        # Should return either None or an iterable of Response, dict
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


class ProxiesSpiderMiddleware(object):

    def __init__(self, proxies_url):
        self.proxies_url = proxies_url

    def getProxy(self):
        response = requests.get(self.proxies_url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxies_url=crawler.settings.get('PROXIES_URL')
        )


    def process_request(self,request, spider):
        print('处理请求')

    def process_response(self, request, response, spider):
        print('代理中间件')
        print(response.status)
        if response.status == 403:
            IP = self.getProxy()
            print('代理ip: %s' % IP)
            request.meta['proxy'] = IP
            return request
        else:
            return response
