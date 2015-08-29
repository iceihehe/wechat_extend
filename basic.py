# -*- coding=utf-8 -*-
# Created Time: 2015年06月18日 星期四 15时56分13秒
# File Name: basic.py

from __future__ import print_function, unicode_literals

import requests
import urllib
import json

from wechat_sdk import WechatBasic


class WechatExtend(WechatBasic):
    '''
    继承官方文档
    添加其他接口
    '''
    def __init__(self, *args, **kwargs):
        super(WechatExtend, self).__init__(*args, **kwargs)
        # self.__appid = kwargs['appid']
        # self.__appsecret = kwargs['appsecret']

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
        确实不是永久的,只管3天
        post数据实例
        articles是个列表
        thumb_media_id是个临时素材的id
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

    def get_user_summary(self, begin_date, end_date):
        '''
        获取用户增减数据(最大时间跨度7天)
        格式为'2014-12-02'
        end_date的最大值为昨天
        begin和end的最大差值<=6
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/datacube/getusersummary',
            data={
                'begin_date': begin_date,
                'end_date': end_date,
            }
        )

    def get_user_cumulate(self, begin_date, end_date):
        '''
        获取累计用户数据(最大时间跨度7天)
        格式为'2014-12-02'
        end_date的最大值为昨天
        begin和end的最大差值<=6
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/datacube/getusercumulate',
            data={
                'begin_date': begin_date,
                'end_date': end_date,
            }
        )

    def generate_oauth_url(self, redirect_uri, scope='snsapi_base', state=''):
        '''
        生成网页授权的链接
        '''
        url_base = 'https://open.weixin.qq.com/connect/oauth2/authorize?'\
            'appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}'\
            '#wechat_redirect'

        return url_base.format(
            self._WechatBasic__appid, urllib.quote_plus(redirect_uri),
            scope,
            state
        )

    def exchange_code_for_oauth_access_token(self, code):
        '''
        用code换取网页授权的access_token和openid
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/sns/oauth2/access_token',
            params={
                'appid': self._WechatBasic__appid,
                'secret': self._WechatBasic__appsecret,
                'code': code,
                'grant_type': 'authorization_code',
            }
        )

    def refresh_oauth_access_token(self, refresh_token):
        '''
        刷新access_token
        这个参数是从exchange_code_for_oauth_access_token方法获得的
        '''
        self._check_appid_appsecret()

        return self._post(
            url='https://api.weixin.qq.com/sns/oauth2/refresh_token',
            params={
                'appid': self._WechatBasic__appid,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }
        )

    def get_oauth_user_info(self, access_token, openid, lang='zh_CN'):
        '''
        获取用户信息
        '''
        self._check_appid_appsecret()

        return self._get(
            url='https://api.weixin.qq.com/sns/userinfo',
            params={
                'access_token': access_token,
                'openid': openid,
                'lang': lang,
            }
        )

    def validate_oauth_access_token(self, access_token, openid):
        '''
        验证access_token是否有效
        '''

        return self._get(
            url='https://api.weixin.qq.com/sns/auth',
            params={
                'access_token': access_token,
                'openid': openid,
            }
        )

    def add_kfaccount(self, kf_account, nickname, password=''):
        '''
        添加客服账号
        '''
        data = {
            'kf_account': kf_account,
            'nickname': nickname,
        }

        if password:
            data.update({'password': password})

        return self._post(
            url='https://api.weixin.qq.com/customservice/kfaccount/add',
            data=data,
        )

    def get_kflist(self):
        '''
        获取客服账号列表
        '''

        return self._get(
            url='https://api.weixin.qq.com/cgi-bin/customservice/getkflist',
        )

    def send_kfmessage(
            self, openid, msgtype, content=None, media_id=None,
            articles=None, music=None
            ):
        '''
        发送客服消息
        articles是个列表
        music是个字典
        '''

        self._check_appid_appsecret()

        data = {
            'msgtype': msgtype,
            'touser': openid,
        }

        some_types = [
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
        elif msgtype == 'music':
            pass
        elif msgtype == 'news':
            pass

        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
            data=data,
        )
