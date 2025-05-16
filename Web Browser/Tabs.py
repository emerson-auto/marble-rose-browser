import sqlite3
import time

class Tabs():
    def __init__(self,con,cur):
        self.con = con
        self.cur = cur
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='tabs'")
        
        if res.fetchone() is None:
            self.cur.execute("CREATE TABLE tabs(url,loc)")
            self.con.commit()
            
    def save_tabs(self,tablist):
        self.cur.execute("DROP TABLE tabs")
        self.cur.execute("CREATE TABLE tabs(url,loc)")
        for index,url in enumerate(tablist):
            if type(url) is not str:
                url = url.toString()
            self.cur.execute('INSERT INTO tabs VALUES (?,?)',(url,index))
        self.con.commit()
        self.con.close()
        
    def get_tabs(self):
        res = self.cur.execute("SELECT url FROM tabs ORDER BY loc asc")
        tuples = res.fetchall()
        list = [tab[0] for tab in tuples]
        return list