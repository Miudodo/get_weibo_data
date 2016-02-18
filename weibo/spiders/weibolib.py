#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import requests
import lxml.html as HTML

class weibo:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
            'Referer':'',
        }
        self.s = requests.Session()

    def get_rand(self, url):
        r = requests.get(url).content
        rand = HTML.fromstring(r).xpath("//form/@action")[0].split("&")[0].split("=")[1]
        passwd = HTML.fromstring(r).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(r).xpath("//input[@name='vk']/@value")[0]
        return rand, passwd, vk

    def login(self):
        #post参数
        backTitle='%E6%89%8B%E6%9C%BA%E6%96%B0%E6%B5%AA%E7%BD%91'
        backURL='http://weibo.cn/'
        ns= '1'
        revalid= '2'
        vt= '4'
        url = 'https://login.weibo.cn/login/?backURL='+ backURL + '&backTitle=' + backTitle + '&vt=' + vt + '&revalid=' + revalid + '&ns=' + ns
        rand, passwd, vk = self.get_rand(url)
        url_login = url + '&rand=' + rand
        login_data = {
            'backTitle':'手机新浪网',
            'backURL':backURL,
            'mobile':self.user,
            passwd:self.pwd,
            'remember':'on',
            'submit':'登录',
            'tryCount':'',
            'vk':vk,
            'encoding': 'utf-8',
        }

        r = self.s.post(url_login, params=login_data, headers=self.headers, allow_redirects=False)

        #gsid_CTandWM =  r.cookies['gsid_CTandWM']
        cookies = r.cookies
        #html = self.s.get('http://weibo.cn/u/3125046087?vt=4',cookies = cookies)
        return cookies