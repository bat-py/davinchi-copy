import pymysql 
from pymysql.cursors import DictCursor 




class SqlRequests:
    def __init__(self):
        con = pymysql.connect(
            host='84.252.74.115',
            user='crow',
            password='crow999',
            db='telegrambot',
            cursorclass=DictCursor
            )
            
        self.cur = con.cursor()


