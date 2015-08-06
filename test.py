# -*- coding=utf-8 -*-
# Created Time: 2015年08月06日 星期四 11时00分54秒
# File Name: test.py

from __future__ import print_function

from basic import WechatExtend
from const import appid, appsecret

w = WechatExtend(appid=appid, appsecret=appsecret)
a = 'OezXcEiiBSKSxW0eoylIeAShrSj-id9MvGkWFJWQpgRj4--FhXTDfRhcOKKCJDNEfo4QnEwi_m4kq2IkMqg96HGaXXRh5pRbCaxeYfV-zs8ODNegHFn5Fek61eLIGhYpnV6dE224L0PLD_Xy62krow'
o = 'oXp1ys3Xq5mBu0Yk8V3VGfAJkZY0'

r = w.get_oauth_user_info(a,o)
print(r)
