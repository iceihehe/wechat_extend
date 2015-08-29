# -*- coding=utf-8 -*-
# Created Time: 2015年08月06日 星期四 11时00分54秒
# File Name: test.py

from __future__ import print_function

from basic import WechatExtend
from const import appid, appsecret

w = WechatExtend(appid=appid, appsecret=appsecret)

# r = w.add_kfaccount('haha@gh_5301ba9ebc1d', 'haha')
r = w.send_kfmessage('o-LjpsmORiDrUOlpAsN5N739vz48', 'image', media_id='hR32bzXVtc_j3Xv28lnDebL9Ve4603SyZQuqzhr4wQc')
# r = w.get_material_list('image')
print(r)
