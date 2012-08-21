#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-18

@author: haosdent
'''
import gevent
from gevent import monkey
from gevent.pool import Pool
import pool.httpclientpool as httpclientpool
from pool.httpclientpool import HttpClientPool
import db.queue as queue

monkey.patch_all()

""" Counter variable """
count = 0

""" Running snatch flag variable """
running = False

""" Create the thead pool which size is 1000 """
thread_pool = Pool(10)

"""
In spider cluster, 
node_serial_number is the serial number of this node while
node_total_number is the size of spider cluster. 
"""
node_serial_number = 0
node_total_number = 1

def add_task(order, force = False):
    if order != None:
        order = queue.insert_one(order, force)
        if order["status"] != "completed":
            snatch()
        return order
        

def snatch():
    global running
    """ If this node is running, pass """
    if running == True:
        return

    """ Create the httpclient pool which default size is 10 """
    httpclient_pool = HttpClientPool()
    
    """
    Allocate a task to this spider node,
    skip is the task's start point in queue,
    and limit is the number of data which will be snatched in this spider node.
    """
    queue_size = queue.count()
    limit = queue_size / node_total_number 
    skip = limit * node_serial_number
    if node_total_number - 1 == node_serial_number:
        limit += queue_size % node_total_number
        
    print "skip = ", skip, ", limit = ", limit
    
    with gevent.Timeout(None, False):        
        print "This spider is start."
        running = True
        
        orders = queue.find(skip, limit)
        #while orders.count() > 0:
        for order in orders:
            thread_pool.spawn(httpclient_pool.request, order)
            thread_pool.join()
            
        print "Start =", httpclientpool.start,", End =", httpclientpool.end,", Error =", httpclientpool.error
        httpclientpool.start = 0
        httpclientpool.end = 0
        httpclientpool.error = 0
            
        orders = queue.find(skip, limit)

        running = False
        print "This spider is finished."

def test():
    queue.init_db()
    snatch()

if __name__ == '__main__':
    test()
