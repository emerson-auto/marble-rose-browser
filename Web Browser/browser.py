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
import os
from Window import Window
from Settings import Settings
from ThemesTemp import Themes
from Preferences import Preferences
from Tabs import Tabs
from Bookmarks import Bookmarks
from Interceptor import Interceptor, RulesAssembler, IntRun, RulesAssemblerEmitter

class Intercepting():
    def __init__(self):
        self.functional = False
        self.tasklist = []
    def add_task(self,func):
        self.tasklist.append(func)
    def run_tasks(self):
        self.functional = True
        while len(self.tasklist) != 0:
            func = self.tasklist.pop()
            func()
    
class Browser(QWidget):
    def __init__(self, app):
        super(Browser, self).__init__()
        print('browser initalized at ' + str( time.time() ))
        self.app = app
        con = sqlite3.connect("browser.db")
        cur = con.cursor()
        self.preferences = Preferences(con,cur)
        self.tab_storage = Tabs(con,cur)
        self.bookmarks = Bookmarks(cur,con)
        
        self.dir = os.path.dirname(__file__)
        
        QFontDatabase.addApplicationFont("./Unnamed.ttf")
        
        self.themes = Themes(self.preferences.get_preferences('theme'),self.preferences.get_preferences('font'),self.dir)
        self.object_list = []
        
        self.profile = QWebEngineProfile('main_profile')
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        
        rules_assembler_emitter = RulesAssemblerEmitter(self) 
        rules_assembler_emitter.rules_assembled.connect(self.add_interceptor)
        
        self.intrun = IntRun(rules_assembler_emitter)
        self.pool = QThreadPool()
        self.pool.start(self.intrun)
        
        self.intercepting = Intercepting()
        
        self.tabs = QTabWidget()
        
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        
        prev = self.tab_storage.get_tabs()
        for index,url in enumerate(prev):
            self.add_tab(url, index)
        if self.tabs.count() == 0:
            self.add_tab()
        
        self.i = self.tabs.tabCloseRequested
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        index = self.tabs.tabBar().addTab('')
        self.button = QPushButton('+')
        self.button.setMaximumWidth(40)
        self.button.setMaximumHeight(20)
        self.button.clicked.connect(self.add_tab)
        self.tabs.tabBar().setTabButton(index,QTabBar.ButtonPosition.RightSide,self.button)
        self.tabs.tabBar().setObjectName('fonted')
        self.tabs.showMaximized()
        self.app.aboutToQuit.connect(self.save)
    
    def add_interceptor(self,rules_assembler):
        self.interceptor = Interceptor( rules_assembler.rules, rules_assembler.pr_rules, self )
        self.profile.setUrlRequestInterceptor(self.interceptor)
        self.intercepting.run_tasks()
        
        
    def add_tab(self,url=None,index=None): 
        tab = Window(self.profile,self.themes,self.preferences,self.bookmarks,self.intercepting,self.dir)
        
        name = 'New Tab'
        
        if url:
            if url == 'home':
                name = 'New Tab'
                tab.home()
            elif url == 'settings':
                name = 'Settings'
                tab.settings()
            else:
                tab.setQuery(url)
                tab.loadUrl() 
        if not index:
            tabdex = self.tabs.addTab(tab,QIcon(),'')
        else:
            self.tabs.insertTab(index,tab,QIcon(),'')
            tabdex = index
        
        self.tabs.tabBar().setTabButton(tabdex , QTabBar.ButtonPosition.LeftSide,self.left_label( (name,None) ) )
        widge = self.tabs.widget(tabdex)
        
        tab.page.newWindowRequested.connect(lambda request: self.add_tab( request.requestedUrl(), self.tabs.indexOf(widge) + 1 ) )
        update_tab = lambda tuple: self.update_tab(self.tabs.indexOf(widge),tuple)
        
        tab.loaded_tab.connect(update_tab)
        tab.theme_changed.connect(self.app.setStyleSheet)
        tab.theme_changed.connect(tab.load_theme)
    
        
    def update_tab(self,tabdex,tuple):
        self.tabs.tabBar().setTabButton(tabdex,QTabBar.ButtonPosition.LeftSide,self.left_label(tuple))
    
    def close_tab(self, index):
        
        self.tabs.removeTab(index)
    
    def save(self):
        tablist = [self.tabs.widget(index).centralWidget().url() for index in range(self.tabs.count()) if self.tabs.widget(index)]
        self.tab_storage.save_tabs(tablist)    

    def left_label(self,tuple):
        label = QLabel(tuple[0],alignment=Qt.AlignmentFlag.AlignLeft)
        label.setObjectName('tabtext')
        lay = QHBoxLayout()
        if tuple[1]:
            icon = QLabel()
            icon.setPixmap(tuple[1].pixmap(QSize(16,16)))
            lay.addWidget(icon)
        lay.addWidget(label)
        contain = QWidget()
        contain.setLayout(lay)
        
        
        return contain

print('program started at ' + str( time.time() ) + ' in ' + os.path.dirname(__file__) )
print('Executables will be searched for at ' + QLibraryInfo.path(QLibraryInfo.LibraryPath.LibraryExecutablesPath))
MyApp = QApplication(sys.argv)
MyApp.setApplicationName('I have no idea what I am doing')
MyApp.setStyle('Fusion')
browser = Browser(MyApp)

MyApp.setStyleSheet(browser.themes.main_style)
MyApp.exec()