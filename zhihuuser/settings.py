# -*- coding: utf-8 -*-

# Scrapy settings for zhihuuser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuuser'

SPIDER_MODULES = ['zhihuuser.spiders']
NEWSPIDER_MODULE = 'zhihuuser.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuuser (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.5

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Cookie': '_xsrf=graj0i331sGh36vXQou2YDYkkcAevSNS; __utmz=155987696.1539658841.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _zap=e97ed595-cd66-43d3-ab3e-d191ba7c6464; d_c0="AOAnh6zJXg6PTkgzTq6h6Sa_iHQEC6zuUUU=|1539659269"; q_c1=44e5b8fc6f3f43168f39d13a05d4c793|1539659287000|1539659287000; __gads=ID=e72bc63dbcec9064:T=1539659292:S=ALNI_MZ7-iZN5q0pNJtX9oHv-BYxYcnOhw; __utma=155987696.89352572.1539658841.1539679811.1539866818.3; __utmc=155987696; anc_cap_id=86f6a849707b4e1b9d752663cb44b6d7; tgw_l7_route=bc9380c810e0cf40598c1a7b1459f027; capsion_ticket="2|1:0|10:1539992467|14:capsion_ticket|44:ZThkMDYwMjVlMGRmNGQyNjgzMmIyNzRjMjgwOTc3MzY=|2ec4df31b06df17f8b6f0583c8b8d8f98ad2dfe1bc451338dcb4c4d4461c60d2"; z_c0="2|1:0|10:1539992479|4:z_c0|92:Mi4xVi1pTEF3QUFBQUFBNENlSHJNbGVEaVlBQUFCZ0FsVk5uN20zWEFBbkpFSHVZV3U3TS12V1ZiYnRBeU9mQVRLVEtn|522fda2098edd5db2a2ec5e68386982dadd6d2739f73c6b0e17662f97830b23f"',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuuser.middlewares.ZhihuuserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'zhihuuser.middlewares.ProxyMiddleware': 543,
   'zhihuuser.middlewares.RandomUserAgentMiddleware': 544,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'zhihuuser.pipelines.ExamplePipeline': 1,

    # Store scraped item in redis for post-processing.
    # 'scrapy_redis.pipelines.RedisPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = '172.16.7.1'
MYSQL_DBNAME = 'spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'Alvin_M1a0'
MYSQL_PORT = 3306
MYSQL_TABLE = 'zhihuuser'

MONGO_URI = 'localhost'
MONGO_DATABASE = 'zhihu'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True

REDIS_URL = 'redis://172.16.7.1:6379'

PROXY_POOL_URL = 'http://172.16.7.1:5555/random'