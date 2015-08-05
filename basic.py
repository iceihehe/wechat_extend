# -*- coding=utf-8 -*-
# Created Time: 2015年06月18日 星期四 15时56分13秒
# File Name: basic.py

from __future__ import print_function, unicode_literals

import requests
import json

from wechat_sdk import WechatBasic


class WechatExtend(WechatBasic):
    '''
    继承官方文档
    添加其他接口
    '''
    def __init__(self, *args, **kwargs):
        super(WechatExtend, self).__init__(*args, **kwargs)

    def _request(self, method, url, **kwargs):
        """
        向微信服务器发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.access_token,
            }
        if isinstance(kwargs.get("data", ""), dict) and \
                not kwargs.get('files'):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        try:
            response_json = r.json()
        except ValueError:
            response_json = r

        self._check_official_error(response_json)
        return response_json

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
        articles示例(是个列表):
        [
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
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/add_news',
            data={'articles': articles}
        )

    def add_permanent_material(self, media_type, media_file, extension='jpg'):
        '''
        新增永久其他类型素材
        media_file就是个file object
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

        return self._post(
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

    def get_permanent_material(self, media_id):
        '''
        获取永久素材
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/get_material',
            data={'media_id': media_id}
        )

    def delete_permanent_material(self, media_id):
        '''
        删除永久素材
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/del_material',
            data={'media_id': media_id}
        )

    def update_permanent_material(self, media_id, articles, index=0):
        '''
        修改永久图文素材
        articles是一个字典，因为一次只能改一个
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/material/update_news',
            data={
                'media_id': media_id,
                'index': index,
                'articles': articles,
            }
        )

    def upload_news(self, articles):
        '''
        上传图文消息素材
        但是不是永久的有待测试
        post数据实例
        articles是个列表
        [
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
        '''

        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/media/uploadnews',
            data={'articles': articles}
        )

    def preview(self, msgtype, user_id=None, user_name=None, media_id=None,
                content=None):
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

    def mass_send_by_openid(self, msgtype, user_ids, media_id=None,
                            content=None):
        '''
        根据openid列表群发
        user_ids是个列表
        '''
        self._check_appid_appsecret()

        some_types = [
            'mpnews',
            'voice',
            'mpvideo',
            'image',
        ]

        data = {'touser': user_ids, 'msgtype': msgtype, 'touser': user_ids}

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
            url='https://api.weixin.qq.com/cgi-bin/message/mass/send',
            data=data
        )

    def mass_send_by_group(self, msgtype, is_to_all=False, group_id='0',
                           media_id=None, title=None, content=None):
        '''
        根据组群发
        '''
        self._check_appid_appsecret()

        data = {
            'filter': {'is_to_all': is_to_all, 'group_id': group_id},
            'msgtype': msgtype
        }

        some_types = [
            'mpnews',
            'voice',
            'image',
        ]

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
        elif msgtype == 'video':
            pass

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/mass/sendall',
            data=data
        )

    def get_mass_send_status(self, msg_id):
        '''
        查询群发消息发送状态
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/mass/get',
            data={'msg_id': msg_id}
        )
