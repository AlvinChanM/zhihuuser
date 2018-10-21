# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    url_token = Field()
    follower_count = Field()
    avatar_url = Field()
    headline = Field()
    gender = Field()
    answer_count = Field()
    article_count = Field()
    user_type = Field()
