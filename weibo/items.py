# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Weibo2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_users = scrapy.Field() # 博主信息
    weibo_content = scrapy.Field() # 微博信息

class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_name = scrapy.Field() # 博主
    weibo_url = scrapy.Field() # 博主地址
    weibo_img = scrapy.Field() # 博主头像
    weibo_fsc = scrapy.Field() # 粉丝数

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_id = scrapy.Field() # 微博id
    con_time = scrapy.Field() # 时间

    like_count = scrapy.Field() #赞数量
    forward_count = scrapy.Field() #转发数量
    review_count = scrapy.Field() #评论数量
    review_url = scrapy.Field() #评论链接

    con_type = scrapy.Field() # 转发or原创
    content = scrapy.Field() # 微博内容 {content:"",ori_name:"",ori_text:"", ori_like:"", ori_forword:"", ori_review:""}

class ReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_id = scrapy.Field()  # 微博id
    review_name = scrapy.Field() #评论人
    review_to = scrapy.Field() #评论对象
    review_context = scrapy.Field() #评论内容
    review_like = scrapy.Field() #评论点赞人数
    review_time = scrapy.Field() #评论点赞人数