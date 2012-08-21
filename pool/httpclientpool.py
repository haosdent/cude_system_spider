#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-18

@author: haosdent
'''
import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
import spider.spider as spider
import db.queue as queue

"""monkey.patch_all()"""

""" Counter variable """
start = 0
end = 0
error = 0

""" define the httpclient pool """
httpclient_pool = HTTPClient("202.116.160.170", concurrency=10)

class HttpClientPool(object):
    
    def request(self, order):
        global start, end, error
        order["status"] = "using"
        queue.change_status(order)
        
        try:
            start += 1
            order = spider.snatch_lesson(httpclient_pool, order)
        except:
            error += 1
            order["status"] = "uncompleted"
            queue.change_status(order)
            raise
        else:
            """ Add response headers and body to database if request successfully """
            end += 1
            order["status"] = "completed"
            queue.update_response(order)
        finally:
            pass
