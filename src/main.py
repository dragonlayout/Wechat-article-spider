#!/usr/bin/python
# coding=utf-8

import json
import requests
import os
import validators
import time
from bs4 import BeautifulSoup


def get_folder_format_datetime(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H %M", time_local)
    return dt


def get_format_datetime(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M", time_local)
    return dt


def get_img_type(image_url):
    """
    微信图片地址链接判断图片拓展名
    :type image_url: str https://mmbiz.qpic.cn/mmbiz_jpg/kWialSIU35riaOicicHMWibUhCibNSqzYiaffkkErdHIJCbG3PhicKialYs54JvYpskibuSe4k5bsZHUsODxxeU4JjXlYFfg/640?wx_fmt=jpeg
    """
    if image_url.find('jpeg') != -1:
        return 'jpeg'
    elif img_url.find('png') != -1:
        return 'png'
    elif img_url.find('gif') != -1:
        return 'gif'
    else:
        return 'jpeg'


def render_wx_article_html(title, cover_url, post_time, content):
    """

    :type post_time: long
    :param title:
    :param cover_url:
    :param post_time:
    :param content:
    :return:
    """
    # 赋值 title
    wx_article_html_template_soup.title.string = title
    # 赋值 封面图
    wx_article_html_template_soup.find('img', id='js_cover')['src'] = cover_url
    # 赋值 活动名
    wx_article_html_template_soup.find('h2', id='activity-name').string = title
    # 赋值 发布日期
    # 时间戳转化 yyyy-MM-dd
    dt = get_format_datetime(post_time)
    wx_article_html_template_soup.find('em', id='post-date').string = dt
    # 赋值 文章正文
    wx_article_html_template_soup.find('div', id='js_content').replace_with(content)


if __name__ == '__main__':
    offset = 240
    # 遍历公众号历史消息
    # 文章数
    article_count = 1
    total_article_list = []
    # 读取模板 html
    with open('../resources/media/wx-article.html', encoding='utf-8') as wx_article_html_file:
        wx_article_html_template_str = wx_article_html_file.read()
    wx_article_html_template_soup: BeautifulSoup = BeautifulSoup(wx_article_html_template_str, features='html5lib')
    print('开始下载:')
    while True:
        print("offset: " + str(offset))
        # 定期需要更换的 2 个字段
        cookie = 'pgv_pvid=7501395272; eas_sid=x155D464U6C1e9X0V7v9a944Q1; pgv_pvi=6138832896; ptui_loginuin=824291784; pt2gguin=o0824291784; RK=LYAIP3TRG/; ptcz=d02014e52903e0fca2b5e05cc679af278a79985c18d7419ab20739e0027b332d; LW_sid=21y5z414E8g6b3u0j8e3O8e1t9; LW_uid=H1s5S4e4p8g6f3Z0Y8p3J8q2N0; ua_id=SMbNc6ZLseKSpvrdAAAAAAJ8r82ADMpi5Yd9seEeYlc=; mm_lang=zh_CN; noticeLoginFlag=1; xid=10ae075b37d81325821fc02bf5317aa2; openid2ticket_o5MrZt-cn0X90BKW7o2Dq5HJij4A=S2/YnQEOk/T0gIM0YkNlGY3ep3TmEYcc71WVkE/YlZ4=; pgv_info=ssid=s5136980807; o_cookie=824291784; pgv_si=s8189424640; wxuin=1946513024; devicetype=Windows10; version=6206061c; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=5pbZM454l+vkK3dkZaK+j9Rw8Kv0uu96Mr3mxslZb9DBXdUn5I6gUXYh8kz8aK9p; wap_sid2=CIDdlaAHElwxdnMyeHhaWS1DUkJXNVVqak9hRjFSalZZeGgxcnp0RWZtUW1XdkFRTW4wbWJnQzFNTEhkcks2a205R0N1RVNHQ0Z3THB3SGtuaTR0QTdpVXJFS3NROTBEQUFBfjCRspnhBTgNQJVO'
        appmsg_token = '989_4FBMl%2FvJCZ5EIP5%2BTbZJ58tNgNhK5nI5CTox_g~~'
        # key = '5a324f0431f6a795d359d5a975b0286da70ab1b26578e332e04333d9c4c18d1d0e04aa009759e29944943913d4df6c74321371fc893b2b79942769abecd3d125c5a9aaf4298d3209c4d9a82491ff9d5c'
        # pass_ticket = '989_GlqHZ10y24H3tHiJtHMpRKRYacHufg8sYneLOw~~'
        biz = 'MzAwMDAxNzk2OA=='
        payload = {'action': 'getmsg',
                   '__biz': biz,
                   'f': 'json',
                   'offset': str(offset),
                   'count': '10',
                   'is_ok': '1',
                   'scene': '123',
                   'uin': '777',
                   'key': '777',
                   'pass_ticket': '',
                   'wxtoken': '',
                   'appmsg_token': appmsg_token,
                   'x5': '0'}
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'mp.weixin.qq.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }
        r = requests.get('https://mp.weixin.qq.com/mp/profile_ext', params=payload, headers=headers)
        response_dict = json.loads(r.text)
        # 返回了当前页的 10 个页面信息
        final_article_list = []
        try:
            msg_list_str: str = response_dict['general_msg_list']
            msg_list_dict: dict = json.loads(msg_list_str)
            # 文章列表 dict
            msg_list: list = msg_list_dict.get('list')
            msg: dict
            for msg in msg_list:
                # 每次推送一条消息，可能包含多条文章
                article_list = []
                comm_msg_info: dict = msg.get('comm_msg_info')
                article_id = comm_msg_info['id']
                article_datetime = comm_msg_info['datetime']
                article_status = comm_msg_info['status']
                app_msg_ext_info: dict = msg.get('app_msg_ext_info')
                article_dict = {'msg_id': str(article_id),
                                'msg_datetime': article_datetime,
                                'msg_title': app_msg_ext_info.get('title'),
                                'msg_digest': app_msg_ext_info.get('digest'),
                                'msg_content_url': app_msg_ext_info.get('content_url'),
                                'msg_cover_url': app_msg_ext_info.get('cover')}
                if len(article_dict['msg_content_url']) != 0:
                    article_list.append(article_dict)
                # 两种类型，单个文章，多个文章
                multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                sub_article_count = 1
                for multi_app_msg in multi_app_msg_item_list:
                    article_dict = {'msg_id': str(article_id) + '_' + str(sub_article_count),
                                    'msg_datetime': article_datetime,
                                    'msg_title': multi_app_msg.get('title'),
                                    'msg_digest': multi_app_msg.get('digest'),
                                    'msg_content_url': multi_app_msg.get('content_url'),
                                    'msg_cover_url': multi_app_msg.get('cover')}
                    if len(article_dict['msg_content_url']) != 0:
                        article_list.append(article_dict)
                    sub_article_count += 1
                total_article_list.append(article_list)
                # 保存文章内容和图片
                # 新建文件夹
                folder_count = 1
                for article in article_list:
                    article_folder_path = '../resources/db/' + get_folder_format_datetime(article['msg_datetime']) + '(' + article['msg_id'] + ')' + article['msg_title']
                    cover_image_relative_path = ''
                    if not os.path.exists(article_folder_path):
                        print('建立文件夹:' + article_folder_path)
                        try:
                            os.mkdir(article_folder_path)
                        except Exception as e:
                            print("文件夹名字不合法:" + article['msg_title'])
                            article_folder_path = '../resources/db/' + get_folder_format_datetime(article['msg_datetime']) + '(' + article['msg_id'] + ')'
                            if not os.path.exists(article_folder_path):
                                os.mkdir(article_folder_path)
                    else:
                        print('文件夹已存在:' + article_folder_path)
                    # 下载 html
                    with open(article_folder_path + '/index.html', 'w', encoding='utf-8') as html_file:
                        resp_html_str = requests.get(article['msg_content_url']).text
                        # 下载图片
                        source_wx_article_soup = BeautifulSoup(resp_html_str, features='html5lib')
                        # 获取 js_content
                        article_js_content_str = source_wx_article_soup.find('div', id='js_content')
                        if not os.path.exists(article_folder_path + '/images'):
                            print('建立文件夹:' + article_folder_path + '/images')
                            os.mkdir(article_folder_path + '/images')
                        else:
                            print('文件夹已存在:' + article_folder_path + '/images')
                        image_count = 1
                        img_list = [article['msg_cover_url']]
                        for img_tag in article_js_content_str.find_all(name='img'):
                            img_list.append(img_tag)
                        for img_tag in img_list:
                            if type(img_tag) == str:
                                retry_count = 1
                                image_file_name = article['msg_id'] + '_cover.' + get_img_type(img_tag)
                                cover_image_path = article_folder_path + '/images/' + image_file_name
                                cover_image_relative_path = 'images/' + image_file_name
                                if os.path.exists(cover_image_path):
                                    print('封面图已下载: ' + image_file_name)
                                    continue
                                while retry_count <= 3:
                                    print('下载封面图 ' + image_file_name + '(第 ' + str(retry_count) + ' 次):' + img_tag)
                                    image_resp = requests.get(img_tag)
                                    if image_resp.status_code == 200:
                                        print('下载封面图成功' + image_file_name)
                                        with open(cover_image_path, 'wb') as image_file:
                                            image_file.write(image_resp.content)
                                        break
                                    retry_count += 1
                            else:
                                img_attrs: dict = img_tag.attrs
                                data_src_url = img_attrs.get('data-src')
                                data_backsrc_url = img_attrs.get('data-backsrc')
                                src_url = img_attrs.get('src')
                                tag_type = ''
                                if data_src_url is not None:
                                    img_url = data_src_url
                                    tag_type = 'data-src'
                                elif data_backsrc_url is not None:
                                    img_url = data_backsrc_url
                                    tag_type = 'data-backsrc'
                                else:
                                    img_url = src_url
                                    tag_type = 'src'
                                if img_url is not None:
                                    #下载图片
                                    image_file_name = article['msg_id'] + '_' + str(image_count) + '.' + get_img_type(img_url)
                                    image_file_path = article_folder_path + '/images/' + image_file_name
                                    if os.path.exists(article_folder_path + '/images/' + image_file_name):
                                        print('图片图已下载: ' + image_file_name)
                                        img_tag[tag_type] = 'images/' + image_file_name
                                        image_count += 1
                                        continue
                                    if validators.url(img_url):
                                        retry_count = 1
                                        while retry_count <= 3:
                                            print('下载图片 ' + image_file_name + ' (第 ' + str(retry_count) + ' 次):' + img_url)
                                            image_resp = requests.get(img_url)
                                            if image_resp.status_code == 200:
                                                print('下载图片成功:' + image_file_name)
                                                with open(image_file_path, 'wb') as image_file:
                                                    image_file.write(image_resp.content)
                                                # 替换 html img 的 src
                                                img_tag[tag_type] = 'images/' + image_file_name
                                                break
                                    else:
                                        print('图片地址不合法:' + image_file_name)
                                        continue
                                image_count += 1
                        # 赋值给 页面
                        render_wx_article_html(title=article['msg_title'], cover_url=cover_image_relative_path, post_time=article['msg_datetime'], content=article_js_content_str)
                        # print(str(wx_article_html_template_soup))
                        # html_str = wx_article_html_template_soup.prettify(encoding='utf-8', formatter='html5')
                        html_file.write(str(wx_article_html_template_soup))
            offset += 10
        except Exception as e:
            print('finish')
            print(response_dict)
            break
        # 先遍历 offset 下载 json, 解析出 文章地址, 下载文章html 和 图片
        # 2018-09-25 22:46(1000000493_1)【一线风采】新血液，新力量