#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-7-16

@author: haosdent
TODO List:
'''

import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser
from geventhttpclient.url import URL
from checkcode import parse
from parser import parse_lesson
from geventhttpclient import HTTPClient

def ___login(httpclient, student_id, passwd):
    """ Firstly, register a SESSION in 202.116.160.166 and then get ASP.NET_SessionId, __VIEWSTATE and checkcode """
    resp = httpclient.get('http://' + httpclient.host + '/default2.aspx')
    """ Get ASP.NET_SessionId """
    session_id = ''
    for header in resp.headers:
        if header[0] == 'set-cookie':
            session_id = re.split(r'ASP.NET_SessionId=(\w+);', header[1])[1]

    """ Get __VIEWSTATE """
    viewstate = ''
    resp_body = resp.read()
    viewstate = re.split(r'name="__VIEWSTATE" value="(\w+)"', resp_body)[1]

    """ Secondly, post the student id and password to cude system for login """
    status_code = 500
    while status_code != 302:
        """ Get checkcode"""
        checkcode = ''
        checkcode = parse(httpclient, session_id)

        headers = { 'Content-Length' : '169',
                    'Content-Type' : 'application/x-www-form-urlencoded',
                    'Cookie' : 'ASP.NET_SessionId=' + session_id,
                    'Referer' : 'http://' + httpclient.host + '/'}
        postdata = [('__VIEWSTATE', viewstate),
                    ('TextBox1', student_id),
                    ('TextBox2', passwd),
                    ('TextBox3', checkcode),
                    ('RadioButtonList1', '%D1%A7%C9%FA'),
                    ('Button1', ''),
                    ('lbLanguage', '')]
        postdata = urllib.urlencode(postdata)
        resp = httpclient.post('http://' + httpclient.host + '/default2.aspx', postdata, headers)

        status_code = resp.status_code
    return session_id

def ___snatch_lesson(httpclient, student_id, session_id):
    """ Snatch the lesson """
    headers = { 'Cookie' : 'ASP.NET_SessionId=' + session_id,
                'Referer' : 'http://' + httpclient.host + '/'}
    resp = httpclient.get('http://' + httpclient.host + '/xskbcx.aspx?xh=' + student_id, headers)

    """ Transform the decode of response body to UTF8. """
    resp_body = resp.read()
    lesson = parse_lesson(resp_body)

    return lesson

def snatch_lesson(httpclient, order):
    session_id = ___login(httpclient, order['student_id'], order['password'])
    order['response'] = ___snatch_lesson(httpclient, order['student_id'], session_id)

    return order

if __name__ == '__main__':
    pass
