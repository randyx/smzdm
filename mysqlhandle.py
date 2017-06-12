#!/usr/bin/env python

# encoding: utf-8

'''

@author: xqi

@contact: xiao93qi@gmail.com

@software: PyCharm Community Edition

@file: mysqlhandle.py

@time: 2017/6/12 22:29

@desc:

'''

import pymysql
class MysqlHandle(object):
    def __init__(self):
        self.config={
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'xq1993',
            'db': 'promotioninfo',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }
    def delete_mysql_table(self, tablename):
        connection = pymysql.connect(**self.config)
        cursor = connection.cursor()
        sql = 'DELETE FROM (%s)'
        try:
            cursor.execute(sql, tablename)
            connection.commit()
        except Exception as e:
            print(e.args)
            print(type(e))
            connection.rollback()
            print('delete error')
        connection.close()
    def search_keyword(self, table, keyword, column):
        connection = pymysql.connect(**self.config)
        cursor = connection.cursor()
        sql = 'SELECT * FROM %s WHERE %s LIKE "%%s"'
        try:
            cursor.execute(sql, table, keyword, column)
            result = cursor.fetchall()
            print(result)
        except:
            print("can't find %s" % keyword)
        connection.close()
    def store_mysql_table(self, values):
        connection = pymysql.connect(**self.config)
        cursor = connection.cursor()
        sql = 'INSERT INTO promotion_info (product_name, product_price, isselfnomination, tags, zhi, buzhi) VALUES (%s, %s, %s, %s, %s, %s)'
        try:
            cursor.executemany(sql, values)
            connection.commit()
        except:
            connection.rollback()
            print("store error")
        connection.close()