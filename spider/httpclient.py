#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-7-18

@author: haosdent
TODO List:
'''

import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
from checkcode import parse
from parser import parse_lesson

httpclient = HTTPClient("202.116.160.166", concurrency=10)

def get():
    global httpclient
    return httpclient