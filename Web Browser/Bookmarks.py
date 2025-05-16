import sqlite3
import re
from PyQt6.QtCore import *

class Bookmarks():
    def __init__(self, cur, con):
        self.cur = cur
        self.con = con
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='bookmarks'")
        
        if res.fetchone() is None:
            self.cur.execute("CREATE TABLE bookmarks(url TEXT,title TEXT ,icon BLOB)")
            self.con.commit()
        
    def bookmark(self,url,title,icon):
        self.cur.execute("INSERT INTO bookmarks VALUES (?,?,?)",(url,title,icon))
        self.con.commit()
    
    def get_bookmarks(self):
        res = self.cur.execute("SELECT * FROM bookmarks")
        marks = res.fetchall()
        return marks
    
    def check_bookmark(self,url):
        res = self.cur.execute("SELECT url FROM bookmarks WHERE url=?",(url,))
        if res.fetchone():
            return False
        else:
            return True