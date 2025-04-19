import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3
import time
from Homepage import Homepage
from Settings import Settings


class SignalEmitter(QObject):
    # Define a custom signal with a value
    loaded_icon = pyqtSignal(QIcon)
    loaded_title = pyqtSignal(str)
    theme_changed = pyqtSignal(str)

class Window(QMainWindow):
    
    def __init__(self,cursor,connection,profile,themes,preferences):
        super(Window, self).__init__()
        self.cur = cursor
        self.con = connection
        self.themes = themes
        self.page = QWebEnginePage(profile)
        self.preferences = preferences
        
        homepage = self.homepage()
        
        
        self.signal_emitter = SignalEmitter()
        self.loaded_icon = self.signal_emitter.loaded_icon
        self.loaded_title = self.signal_emitter.loaded_title
        self.theme_changed = self.signal_emitter.theme_changed
        
        #self.setCentralWidget(self.browser)
        self.setCentralWidget(homepage)
        self.showMaximized()
        
        self.toolbar()
        
        
        
    def browser(self):
        browser = QWebEngineView()    
        browser.setPage(self.page)
        browser.iconChanged.connect(self.updateIcon)
        browser.titleChanged.connect(self.updateTitle)
        browser.urlChanged.connect(self.updateUrl)
        
        self.PrevBtn.triggered.connect(browser.back)
        self.nextBtn.triggered.connect(browser.forward)
        self.refreshBtn.triggered.connect(browser.reload)
        
        return browser
    
    def homepage(self):
        homepage = Homepage()
        homepage.line.returnPressed.connect(self.loadUrl)
        homepage.line.textEdited.connect(self.setQuery)
        homepage.qss(self.themes.home_style)
        return homepage
        
    def menu(self):
        settings = Settings()
        settings.qss(self.themes.settings_style)
        start_theme = self.preferences.get_preferences('theme')
        settings.theme_select.setCurrentText(start_theme)
        settings.theme_select.currentTextChanged.connect(self.update_theme)
        return settings
        
    def toolbar(self):
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)
        
        self.PrevBtn = QAction('<', self)
        self.navbar.addAction(self.PrevBtn)

        self.nextBtn = QAction('>', self)
        self.navbar.addAction(self.nextBtn)

        self.refreshBtn = QAction('↩', self)
        self.navbar.addAction(self.refreshBtn)
        
        self.homeBtn = QAction('home', self)
        self.homeBtn.triggered.connect(self.home)
        self.navbar.addAction(self.homeBtn)
        
        self.settingsBtn = QAction('settings',self)
        self.settingsBtn.triggered.connect(self.settings)
        self.navbar.addAction(self.settingsBtn)
        
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText('Search or enter an address')
        #self.searchBar.textChanged.connect(self.predict)
        self.searchBar.returnPressed.connect(self.loadUrl)
        self.searchBar.textEdited.connect(self.setQuery)
        self.navbar.addWidget(self.searchBar)
        
        
    def updateUrl(self, url):
        url_text = url.toString()  
        self.searchBar.setText(url_text)
        
    def predict(self,text):
        self.cur.execute('SELECT * FROM recent ORDER BY timestamp DESC limit 500')
        recents = self.cur.fetchall()
        if re.match(r'https?:\/\/.',text) is not None:
            for i in range(len(recents)):
                #print(recents[i])
                pass
    
    def setQuery(self,text):
        self.url = text
        
    def loadUrl(self):
        if self.centralWidget().inherits("QWebEngineView") is not True:
            self.setCentralWidget(self.browser())
            
        search_url = f'https://kagi.com/search?q={self.url}'
        if re.match(r'https?:\/\/.',self.url) is not None:
            
            self.centralWidget().setUrl(QUrl(self.url))
            #self.cur.execute("INSERT INTO recent VALUES (?,?,?)", (url,time.time(),True))
            #self.con.commit()
        else:
            self.centralWidget().setUrl(QUrl(search_url))
            #self.cur.execute("INSERT INTO recent VALUES (?,?,?)", (url,time.time(),False))
            #self.con.commit()
        
    
    def home(self):
        self.setCentralWidget(self.homepage())
    
    def settings(self):
        menu = self.menu()
        self.setCentralWidget(menu)
    
    def updateIcon(self):
        self.loaded_icon.emit(self.centralWidget().icon())
        
    def updateTitle(self):
        self.loaded_title.emit(self.centralWidget().title())
     
    def update_theme(self,theme):
        self.themes.update(theme)
        self.theme_changed.emit(self.themes.main_style)
        self.preferences.update_preferences('theme',theme)
        
    def load_theme(self):
        #print('whee')
        
        if type(self.centralWidget()).__name__ == 'Homepage':
            self.centralWidget().qss(self.themes.home_style)
            
        elif type(self.centralWidget()).__name__ == 'Settings':
            #print('yup')
            
            self.centralWidget().qss(self.themes.settings_style)
    
    
