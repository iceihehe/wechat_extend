# -*- coding=utf-8 -*-
# Created Time: 2015年08月06日 星期四 11时00分54秒
# File Name: test.py

from __future__ import print_function

from basic import WechatExtend
from const import appid, appsecret

w = WechatExtend(appid=appid, appsecret=appsecret)

t = '2015-8-8'

r = w.get_article_total(t, t)
print(r)
