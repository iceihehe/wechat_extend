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

    def get_material_list(self, type, offset=0, count=20):
        '''
        获取(永久)素材列表
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/batchget_material',
            data={
                'type': type,
                'offset': offset,
                'count': count
            }
        )

    def add_permanent_material(self, articles):
        '''
        新增（永久）素材列表
        articles示例:
        articles = [
            {
                'title': xx,
                'thumb_media_id': xx,
                'author': xx,
                'digest': xx,
                'show_cover_pic': xx,
                'content': xx,
                'content_source_url': xx,
            },
            //如果是多图文，还有...
        ]
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/add_news',
            data={
                'articles': articles
            }
        )
