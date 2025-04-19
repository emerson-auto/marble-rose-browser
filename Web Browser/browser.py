#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3
import time
from Window import Window
from Settings import Settings
from Themes import Themes
from Preferences import Preferences


class Browser(QWidget):
    def __init__(self, cursor, connection, app):
        super(Browser, self).__init__()
        self.cur = cursor
        self.con = connection
        self.app = app
        self.preferences = Preferences()
        
        QFontDatabase.addApplicationFont("./Unnamed.ttf")
        self.app.setFont(QFont('Times New Roman'))
        
        self.themes = Themes(self.preferences.get_preferences('theme'))
        
        self.profile = QWebEngineProfile('main_profile')
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        
        self.tabs = QTabWidget()
        self.add_tab()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        
        self.i = self.tabs.tabCloseRequested
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        index = self.tabs.tabBar().addTab('')
        self.button = QPushButton('+')
        self.button.setMaximumWidth(40)
        self.button.setMaximumHeight(20)
        self.button.clicked.connect(self.add_tab)
        self.tabs.tabBar().setTabButton(index,QTabBar.ButtonPosition.RightSide,self.button)
        
        self.tabs.showMaximized()
    
        
    def add_tab(self):
        tab = Window(self.cur,self.con,self.profile,self.themes,self.preferences)
        tabdex = self.tabs.addTab(tab,QIcon(),' New Tab ')
        widge = self.tabs.widget(tabdex)
        update_icon_for_tab = lambda icon: self.update_icon(self.tabs.indexOf(widge),icon)
        tab.loaded_icon.connect(update_icon_for_tab)
        update_title_for_tab = lambda title: self.update_title(self.tabs.indexOf(widge),title)
        tab.loaded_title.connect(update_title_for_tab)
        tab.theme_changed.connect(self.app.setStyleSheet)
        tab.theme_changed.connect(tab.load_theme)
        
    def update_icon(self,tabdex,icon):
        print(tabdex,icon)
        self.tabs.tabBar().setTabIcon(tabdex,icon)
        
    def update_title(self,tabdex,title):
        print(tabdex,title)
        self.tabs.tabBar().setTabText(tabdex,title)
    
    def close_tab(self, index):
        print(index)
        self.tabs.removeTab(index)
    


    

con = sqlite3.connect("browser.db")
cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='recent'")

if res.fetchone() is None:
    cur.execute("CREATE TABLE recent(search,timestamp,is_website)")
MyApp = QApplication(sys.argv)
MyApp.setApplicationName('I have no idea what I am doing')
MyApp.setStyle('Fusion')


browser = Browser(cur,con,MyApp)
MyApp.setStyleSheet(browser.themes.main_style)
MyApp.exec()
con.close()