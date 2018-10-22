# -*- coding: utf-8 -*-
import json

import requests
from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuSpider(Spider):
    # custom_settings = {
    #     "COOKIES_ENABLED": False,
    #     "DOWNLOAD_DELAY": 0.4,
    # }
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
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user,dont_filter=True)

        # 初始人的关注列表
        yield Request(self.followees_url.format(user = self.start_user, include=self.followees_query, offset=0, limit=20), callback=self.parse_followees, dont_filter=True)

        # 初始人的粉丝列表
        yield Request(self.followers_url.format(user=self.start_user, include = self.follower_query, offset=0, limit=20), callback=self.parse_followers, dont_filter=True)

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
        return [Request(url='https://www.zhihu.com/', callback=self.check_login, dont_filter=True)]

    def check_login(self, response):
        # 验证是否登录成功
        if response.url == 'https://www.zhihu.com/' and response.status == 200:
            return self.start_spiders()


        else:
            print('先登录')