# -*- coding=utf-8 -*-
# Created Time: 2015年06月18日 星期四 15时56分13秒
# File Name: basic.py

from __future__ import print_function, unicode_literals

import requests

from wechat_sdk import WechatBasic


class WechatExtend(WechatBasic):
    '''
    继承官方文档
    添加其他接口
    '''
    def __init__(self, *args, **kwargs):
        super(WechatExtend, self).__init__(*args, **kwargs)

    def get_material_list(self, media_type, offset=0, count=20):
        '''
        获取(永久)素材列表
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/batchget_material',
            data={
                'type': media_type,
                'offset': offset,
                'count': count
            }
        )

    def add_permanent_news(self, articles):
        '''
        新增图文素材
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

    def add_permanent_material(self, media_type, media_file):
        '''
        新增永久其他类型素材
        '''
        self._check_appid_appsecret()

        if isinstance(media_file, file):
            extension = media_file.name.split('.')[-1]
        ext = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'amr': 'audio/amr',
            'mp3': 'audio/mpeg',
            'mp4': 'video/mp4',
        }
        filename = media_file.name.split('/')[-1]

        return requests.post(
            url='https://api.weixin.qq.com/cgi-bin/material/add_material',
            params={
                'access_token': self.access_token,
            },
            data={
                'type': media_type,
            },
            files={
                'media': (filename, media_file, ext[extension])
            }
        )
