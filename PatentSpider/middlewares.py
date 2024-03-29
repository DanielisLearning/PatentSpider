# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from scrapy import signals
from fake_useragent import UserAgent
from tools.crawl_xici_ip import GetIP


class PatentspiderSpiderMiddleware(object):
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


class PatentspiderDownloaderMiddleware(object):
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
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
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


# # scrapy爬虫设置随机访问时间间隔
# class RandomDelayMiddleware(object):
#     def __init__(self, delay):
#         self.delay = delay
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
#         if not isinstance(delay, int):
#             raise ValueError("RANDOM_DELAY need a int")
#         return cls(delay)
#
#     def process_request(self, request, spider):
#         delay = random.randint(0, self.delay)
#         # logging.debug("### random delay: %s s ###" % delay)
#         time.sleep(delay)




class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
        # request.meta["proxy"] = "http://180.175.0.123:8060"
        # request.meta["proxy"] = "http://115.199.124.93:8060"
        # request.meta["proxy"] = "http://177.137.20.55:80"
        # request.meta["proxy"] = "http://120.52.32.46:80"
        # request.meta["proxy"] = "http://118.123.113.4:80"
        # request.meta["proxy"] = "http://218.85.133.62:80"
        # request.meta["proxy"] = "http://52.67.126.170:3129"
        # request.meta["proxy"] = "http://111.92.227.139:8080"
        # request.meta["proxy"] = "http://192.168.137.200:8080"
        # request.meta["proxy"] = "http://163.204.245.117:9999"


        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()

# class RandomProxyMiddleware(object):
#     #动态设置ip代理
#     def process_request(self, request, spider):
#         get_ip = GetIP()
#         request.meta["proxy"] = get_ip.get_random_ip()