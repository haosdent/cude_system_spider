#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-7-15

@author: haosdent
TODO List:
1.Directly save image in a object instead of save it in the file.
'''

import urllib, re
from pytesser import *
from StringIO import StringIO
from geventhttpclient import HTTPClient

def parse(httpclient, session_id = ''):
    result = ''
    headers = { 'Cookie' : 'ASP.NET_SessionId=' + session_id,
                'Referer' : 'http://' + httpclient.host + '/'}

    while not check_result(result):
        resp_body = httpclient.get('http://' + httpclient.host + '/CheckCode.aspx', headers).read()
        im = Image.open(StringIO(resp_body))
        result = image_to_string(im)
        result = re.sub('\s', '', result)
    return result

def check_result(result):
    if len(re.findall('\S', result)) != 5 or len(re.findall('\d', result)) != 5:
        return False
    return True

if __name__ == '__main__':
    pass