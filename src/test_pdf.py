#!/usr/bin/python
# coding=utf-8
import pdfkit

if __name__ == '__main__':
    # pdfkit.from_url('https://mp.weixin.qq.com/s?__biz=MzAwMDAxNzk2OA==&amp;mid=2651771016&amp;idx=1&amp;sn=95e444cc8f0c87a22b7812d0708ae019&amp;chksm=811523d7b662aac10682fddea5c50e49870387b0dea315e292d931a5532d289dc8cdb918bca4&amp;scene=27#wechat_redirect', 'out1.pdf')
    pdfkit.from_file('1.html', 'out2.pdf')