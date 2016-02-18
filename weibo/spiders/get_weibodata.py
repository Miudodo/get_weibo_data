#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import scrapy
import weibolib
import requests
import lxml.html
import re


from scrapy.http import Request
from weibo.items import Weibo2Item



class get_weibodata(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = [
        'http://weibo.cn/attgroup/show?cat=user&uid=1936923577&gid=221101270044820644&type=&rl=1&f=&vt=4',
        'http://weibo.cn/attgroup/show?cat=user&currentPage=1&rl=2&next_cursor=10&previous_cursor=0&uid=1936923577&gid=221101270044820644&page=2&vt=4',
        'http://weibo.cn/attgroup/show?cat=user&uid=1936923577&gid=3835240546280704&rl=1&rand=495196&vt=4',
    ]

    user = 'miao880513@126.com'
    pwd = 'MIAODD9420miaoww'

    c = weibolib.weibo(user, pwd)
    c = c.login()
    cookies = {}
    for i in c:
        cookies2 = {i.name : i.value}
        cookies.update(cookies2)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies)

    #爬取名单
    def parse(self, response):
        sites = response.xpath('//table/tr')

        #获取博主信息
        for sel in sites:
            item = Weibo2Item()

            users = {}

            users["weibo_name"] = ''.join(sel.xpath('td[2]/a[1]/text()').extract())
            users["weibo_url"] = ''.join(sel.xpath('td[2]/a[1]/@href').extract())
            users["weibo_img"] = ''.join(sel.xpath('td[1]/a/img/@src').extract())
            users["weibo_fsc"] = ''.join(sel.xpath('td[2]/text()[1]').extract())

            weibo_url = "http://weibo.cn" + ''.join(users["weibo_url"])

            item["weibo_users"] = users
            item["weibo_content"] = get_weibodata.parse_weibo(self, weibo_url)

            yield item


    #获取微博数据
    def parse_weibo(self, weibo_url):
        r = requests.get(weibo_url, cookies=self.cookies)
        response = r.text.encode('utf-8')
        doc = lxml.html.fromstring(response)
        sites = doc.xpath('//div[contains(@id,"M_")]')
        s = doc.xpath('//div[contains(@id,"M_")]')

        item_all = []
        if s <> []:
            for sel in sites:
                item = {}

                #微博时间
                item["con_time"] = ''.join(sel.xpath('div[last()]/span[@class="ct"]/text()'))

                #赞、转发和评论数
                item["like_count"] = ''.join(sel.xpath('div[last()]/a[contains(@href,"attitude")]/text()'))
                item["forward_count"] = ''.join(sel.xpath('div[last()]/a[contains(@href,"repost")]/text()'))
                item["review_count"] = ''.join(sel.xpath('div[last()]/a[contains(@href,"comment")]/text()'))
                item["review_url"] = ''.join(sel.xpath('div[last()]/a[contains(@href,"comment")]/@href'))

                #微博内容
                content_ctt = {"content_ctt" : ''.join(sel.xpath('div[1]/span[@class="ctt"]/text()'))}
                content_cmt = {"content_cmt" : ''.join(sel.xpath('div[last()]/text()[1]'))}
                ori_name = {"ori_name" : ''.join(sel.xpath('div[1]/span[@class="cmt"]/a/text()'))}

                content_ctt.update(content_cmt)
                content_ctt.update(ori_name)
                item["content"] = content_ctt

                #评论
                review_url = ''.join(item["review_url"])
                item["review"] = get_weibodata.parse_review(self, review_url)
                item_all.append(item)
        else:
            pass

        #下一页
        next_page = doc.xpath("id('pagelist')/form/div/a[1]/@href")

        next_page_url = "http://weibo.cn"  + ''.join(next_page)
        next_page_num = ''.join(re.findall(r'page=([0-9]+)', ''.join(next_page)))

        if next_page <> [] and int(next_page_num, 10) <= 100:
           item_n = get_weibodata.parse_weibo(self, next_page_url)
           for items in item_n:
               item_all.append(items)
        else:
            pass

        return item_all

    #获取评论数据
    def parse_review(self, review_url):
        r = requests.get(review_url, cookies=self.cookies)
        response = r.text.encode('utf-8')
        doc = lxml.html.fromstring(response)
        sites = doc.xpath('//div[contains(@id,"C_")]')

        item_all = []
        if sites <> []:
            for sel in sites:
                item = {}

                item["review_name"] = ''.join(sel.xpath('a[1]/text()'))
                item["review_to"] = ''.join(sel.xpath('span[@class="ctt"]/a/text()'))
                item["review_context"] = ''.join(sel.xpath('span[@class="ctt"]/text()'))
                item["review_like"] = ''.join(sel.xpath('span[@class="cc"][1]/a/text()'))
                item["review_time"] = ''.join(sel.xpath('span[@class="ct"]/text()'))
                item_all.append(item)
        else:
            pass

        #下一页
        next_page = doc.xpath("id('pagelist')/form/div/a[text()='\u4e0b\u9875']/@href")
        next_page_url = "http://weibo.cn"  + ''.join(next_page)
        next_page_num = ''.join(re.findall(r'page=([0-9]+)', ''.join(next_page)))

        end_page_num = doc.xpath("id('pagelist')/form/div/input[@type='hidden']/@value")
        end_page_num = ''.join(end_page_num)

        if next_page <> []:
            item_n = get_weibodata.parse_review(self, next_page_url)
            for items in item_n:
                item_all.append(items)

        else:
            pass

        return item_all