import sqlite3

class Preferences():
    
    def __init__(self):
        
        self.con = sqlite3.connect("browser.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='preferences'")

        if res.fetchone() is None:
            print('whoop')
            self.cur.execute("CREATE TABLE preferences(name,status)")
            self.cur.execute("INSERT INTO preferences VALUES (?,?)", ('theme','plain'))   
        self.con.commit() 
    
    def update_preferences(self,name,status):
        print(status)
        self.cur.execute("UPDATE preferences SET status = ? WHERE name = ?", (status,name))
        self.cur.execute("SELECT status FROM preferences WHERE name = ?", (name,))
        self.con.commit()
        
    def get_preferences(self,name):
        self.cur.execute("SELECT status FROM preferences WHERE name = ?", (name,))
        status = self.cur.fetchone()
        print(status)
        return status[0]

