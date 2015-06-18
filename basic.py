# -*- coding=utf-8 -*-
# Created Time: 2015年06月18日 星期四 15时56分13秒
# File Name: basic.py

from __future__ import print_function, unicode_literals

from wechat_sdk import WechatBasic


class WechatExtend(WechatBasic):
    '''
    继承官方文档
    添加其他接口
    '''
    def __init__(self, *args, **kwargs):
        super(WechatExtend, self).__init__(*args, **kwargs)
