'''
Created on Dec 28, 2014

@author: svatasoiu
'''

import mysql.connector
from threading import Condition

class DBPool(object):

    def __init__(self, dbargs, pool_size=5):
        '''
        Constructor
        '''
        self.active_connections = 0
        self.max_connections = pool_size
        self.dbargs = dbargs
        self.cond_var = Condition()
        
    def get_connection(self):
        self.cond_var.acquire()
        while self.active_connections >= self.max_connections:
            self.cond_var.wait()
        self.active_connections += 1
        connection = mysql.connector.connect(**self.dbargs)
        print connection
        self.cond_var.release()
        return connection 
    
    def close_connection(self, db_conn):
        self.cond_var.acquire()
        db_conn.close()
        self.active_connections -= 1
        self.cond_var.notify()
        self.cond_var.release()