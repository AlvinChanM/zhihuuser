# -*- coding: utf-8 -*-
import json

import requests
from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuSpider(Spider):
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.4,

        # 需要登录后的cookie验证
        'DEFAULT_REQUEST_HEADERS': {
            'Cookie': '_xsrf=graj0i331sGh36vXQou2YDYkkcAevSNS; __utmz=155987696.1539658841.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _zap=e97ed595-cd66-43d3-ab3e-d191ba7c6464; d_c0="AOAnh6zJXg6PTkgzTq6h6Sa_iHQEC6zuUUU=|1539659269"; q_c1=44e5b8fc6f3f43168f39d13a05d4c793|1539659287000|1539659287000; __gads=ID=e72bc63dbcec9064:T=1539659292:S=ALNI_MZ7-iZN5q0pNJtX9oHv-BYxYcnOhw; __utma=155987696.89352572.1539658841.1539679811.1539866818.3; __utmc=155987696; anc_cap_id=86f6a849707b4e1b9d752663cb44b6d7; tgw_l7_route=bc9380c810e0cf40598c1a7b1459f027; capsion_ticket="2|1:0|10:1539992467|14:capsion_ticket|44:ZThkMDYwMjVlMGRmNGQyNjgzMmIyNzRjMjgwOTc3MzY=|2ec4df31b06df17f8b6f0583c8b8d8f98ad2dfe1bc451338dcb4c4d4461c60d2"; z_c0="2|1:0|10:1539992479|4:z_c0|92:Mi4xVi1pTEF3QUFBQUFBNENlSHJNbGVEaVlBQUFCZ0FsVk5uN20zWEFBbkpFSHVZV3U3TS12V1ZiYnRBeU9mQVRLVEtn|522fda2098edd5db2a2ec5e68386982dadd6d2739f73c6b0e17662f97830b23f"',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/64.0.3282.140 Safari/537.36',
        }
    }
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'
    # 用户详情页
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 关注列表
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_spiders(self):
        # 初始人的个人详情
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)

        # 初始人的关注列表
        yield Request(self.followees_url.format(user = self.start_user, include=self.followees_query, offset=0, limit=20), callback=self.parse_followees)

        # 初始人的粉丝列表
        yield Request(self.followers_url.format(user=self.start_user, include = self.follower_query, offset=0, limit=20), callback=self.parse_followers)

    def parse_user(self, response):
        # 解析个人详情
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        # 请求个人的关注列表
        yield Request(self.followees_url.format(user =result.get('url_token'), include=self.followees_query, offset=0, limit=20 ), callback=self.parse_followees)

        # 请求个人粉丝列表
        yield Request(self.followers_url.format(user =result.get('url_token'), include=self.follower_query, offset=0, limit=20 ), callback=self.parse_followers)


    def parse_followees(self, response):
        # 请求关注人的用户详情
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        # 请求下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield  Request(next_page, callback=self.parse_followees)


    def parse_followers(self, response):
        # 请求粉丝列表
        # 请求关注人的用户详情
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              callback=self.parse_user)

        # 请求下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, callback=self.parse_followers)



    def start_requests(self):
        return [Request(url='https://www.zhihu.com/', callback=self.check_login)]

    def check_login(self, response):
        # 验证是否登录成功
        if response.url == 'https://www.zhihu.com/' and response.status == 200:
            return self.start_spiders()


        else:
            print('先登录')