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
        新增永久图文素材
        articles示例:
        {
            articles: [
                {
                    'title': xx,
                
                    'thumb_media_id': xx, //永久mediaID
                    'author': xx,
                    'digest': xx,
                    'show_cover_pic': xx,
                    'content': xx,
                    'content_source_url': xx,
                },
                //如果是多图文，还有...
            ]
        }
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/add_news',
            data=articles
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

    def upload_news(self, articles):
        '''
        上传图文消息素材
        但是能不能用有待测试
        post数据实例
        {
            'articles': [
                {
                    'thumb_media_id': 'xxxxxx',
                    'author': 'xxx',
                    'title': 'xxxx',
                    'content_source_url': 'xxx',
                    'content': 'xxxx',
                    'digest': 'xxxxxx',
                    'show_cover_pic': '1',
                },
                {
                    ....
                    'show_cover_pic': '0',
                }
            ]
        }
        '''

        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/media/uploadnews',
            data=articles
        )

    def preview(self, msgtype, user_id=None, user_name=None, media_id=None, content=None):
        '''
        预览接口
        '''
        self._check_appid_appsecret()

        some_types = [
            'mpnews',
            'voice',
            'mpvideo',
            'image',
        ]

        if user_name:
            data = {'towxname': user_name, 'msgtype': msgtype}
        else:
            data = {'touser': user_id, 'msgtype': msgtype}

        if msgtype in some_types:
            data.update(
                {msgtype: {'media_id': media_id}}
            )
        elif msgtype == 'text':
            data.update(
                {'text': {'content': content}}
            )
        elif msgtype == 'wxcard':
            pass

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/mass/preview',
            data=data
        )
