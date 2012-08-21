#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-7-17

@author: haosdent
TODO List:
'''

from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core.context_processors import csrf
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from geventhttpclient import HTTPClient
import pool.threadpool as threadpool

@cache_page(60 * 15)
@csrf_protect
def lesson_table(request):
    if request.method == 'GET':
        print 'GET'

        return HttpResponse(get_token(request), mimetype='text/html')
    elif request.method == 'POST':
        print 'POST'
        order = {"student_id" : request["student_id"], "password" : request["password"], "status" : "never"}
        order_force = False
        threadpool.add_task(order, order_force)
        return HttpResponse(lesson_table, mimetype='text/html')

def test(request):
    threadpool.test()
