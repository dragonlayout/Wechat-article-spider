#!/usr/bin/python
# coding=utf-8

import json
import requests
import os
import validators
from bs4 import BeautifulSoup


if __name__ == '__main__':
    offset = 0
    # 遍历公众号历史消息
    # 文章数
    article_count = 1
    total_article_list = []
    while True:
        # 定期需要更换的 2 个字段
        cookie = 'pgv_pvid=7501395272; eas_sid=x155D464U6C1e9X0V7v9a944Q1; pgv_pvi=6138832896; ptui_loginuin=824291784; pt2gguin=o0824291784; RK=LYAIP3TRG/; ptcz=d02014e52903e0fca2b5e05cc679af278a79985c18d7419ab20739e0027b332d; LW_sid=21y5z414E8g6b3u0j8e3O8e1t9; LW_uid=H1s5S4e4p8g6f3Z0Y8p3J8q2N0; ua_id=SMbNc6ZLseKSpvrdAAAAAAJ8r82ADMpi5Yd9seEeYlc=; mm_lang=zh_CN; noticeLoginFlag=1; xid=10ae075b37d81325821fc02bf5317aa2; openid2ticket_o5MrZt-cn0X90BKW7o2Dq5HJij4A=S2/YnQEOk/T0gIM0YkNlGY3ep3TmEYcc71WVkE/YlZ4=; pgv_info=ssid=s5136980807; o_cookie=824291784; pgv_si=s8189424640; wxuin=1946513024; devicetype=Windows10; version=6206061c; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=3uAjh/2Apok7tZs7pDatwwoeDsaKNRUNEwfbuKbJJCqT63lf/zp5HcMNvZH1U3HK; wap_sid2=CIDdlaAHElxPNmduQ0wtMUY2aDZGd3VDekNoOUItZ0NxZ25KQ1JuVDV2U0IyZHN0QTlXZk41d1VsbVBxSUwtWm5xbWtoYVZvMU9QS0FYX1dfbndqUllsQnVuQWp2OTBEQUFBfjDIzpbhBTgNQJVO'
        appmsg_token = '989_ByFOIFkrqYwdfBY1pus5H5yATAeP1OWmg1UJSg~~'
        key = 'c86331612ef0946a199ca2d4c2c2245b297c52d9141cdc9e4192454793543fc0420a836ce46c9f92dfa7ee0668c117522912b66c836bb6c892080146a4fba79a4d4e23f63f8a3dd15a6aed9ddd7d783a'
        pass_ticket = '3uAjh/2Apok7tZs7pDatwwoeDsaKNRUNEwfbuKbJJCqT63lf/zp5HcMNvZH1U3HK'
        biz = 'MzAwMDAxNzk2OA=='
        payload = {'action': 'getmsg',
                   '__biz': biz,
                   'f': 'json',
                   'offset': str(offset),
                   'count': '10',
                   'is_ok': '1',
                   'scene': '124',
                   'uin': 'MTk0NjUxMzAyNA==',
                   'key': key,
                   'pass_ticket': pass_ticket,
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
                article_dict = {'msg_id': article_id,
                                'msg_datetime': article_datetime,
                                'msg_title': app_msg_ext_info.get('title'),
                                'msg_digest': app_msg_ext_info.get('digest'),
                                'msg_content_url': app_msg_ext_info.get('content_url'),
                                'msg_cover_url': app_msg_ext_info.get('cover')}
                article_list.append(article_dict)
                # 两种类型，单个文章，多个文章
                multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                sub_article_count = 1
                for multi_app_msg in multi_app_msg_item_list:
                    article_dict = {'msg_id': article_id + '_' + str(sub_article_count),
                                    'msg_datetime': article_datetime,
                                    'msg_title': multi_app_msg.get('title'),
                                    'msg_digest': multi_app_msg.get('digest'),
                                    'msg_content_url': multi_app_msg.get('content_url'),
                                    'msg_cover_url': multi_app_msg.get('cover')}
                    article_list.append(article_dict)
                    sub_article_count += 1
                total_article_list.append(article_list)
                # 保存文章内容和图片
                # 新建文件夹
                folder_count = 1
                for article in article_list:
                    article_folder_path = '../resources/db/' + article['msg_id']
                    os.mkdir(article_folder_path)
                    # 下载 html
                    with open(article_folder_path + '/index.html', 'w', encoding='utf-8') as html_file:
                        resp_html_str = requests.get(article['msg_content_url']).text
                        # 下载图片
                        soup = BeautifulSoup(resp_html_str, features='html.parser')
                        os.mkdir(article_folder_path + '/images')
                        image_count = 1
                        for img_tag in soup.find_all(name='img'):
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
                                if validators.url(img_url):
                                    image_resp = requests.get(img_url)
                                    if image_resp.status_code == 200:
                                        open(article_folder_path + '/images/' + str(image_count) + '.jpg', 'wb').write(
                                            image_resp.content)
                                        image_count += 1
                                        # 替换 html中的 src
                                        img_tag[tag_type] = article_folder_path + '/images/' + str(image_count) + '.jpg'
                                else:
                                    continue
                        html_str = soup.prettify(encoding='utf-8')
                        html_file.write(html_str.decode('utf-8'))
            with open('../resources/result.json', 'w+') as result_file:
                json.dump(final_article_list, result_file, ensure_ascii=False)
            offset += 10
        except Exception as e:
            print('finish')
            print(response_dict)
            print(e)
            break
        # 先遍历 offset 下载 json, 解析出 文章地址, 下载文章html 和 图片