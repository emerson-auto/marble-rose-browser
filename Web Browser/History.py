import sqlite3
import re
import time

class History:
    def __init__(self,con,cur):
        self.con = con
        self.cur = cur
        site = self.cur.execute("SELECT name FROM sqlite_master WHERE name='site_history'")
        search = self.cur.execute("SELECT name FROM sqlite_master WHERE name='search_history'")
        if site.fetchone() is None:
            self.cur.execute("CREATE TABLE site_history(url,title,time,frequency)") 
            self.con.commit()
        if search.fetchone() is None:
            self.cur.execute("CREATE TABLE search_history(search,time,frequency)") 
            self.con.commit()
        
        