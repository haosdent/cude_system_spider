#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-7-17

@author: haosdent
TODO List:
'''

import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
from checkcode import parse

def parse_lesson(resp_body):
    """ Transform the decode of response body to UTF8. """
    encoding = chardet.detect(resp_body)["encoding"]
    if encoding == "GB2312":
        resp_body = resp_body.decode('gbk').encode('utf-8')
    elif encoding == "UTF8":
        resp_body = resp_body.decode('utf-8')

    """ Pick up the lesson table from html """
    resp_body = resp_body[resp_body.find('<table') : resp_body.find('</table>') + 8]
    resp_body = re.sub('&nbsp;', '', resp_body)

    return resp_body