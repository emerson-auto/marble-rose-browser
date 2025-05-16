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
from BookWidget import BookWidget

class SignalEmitter(QObject):
    # Define a custom signal with a value
    loaded_tab = pyqtSignal(tuple)
    theme_changed = pyqtSignal(str)

class Window(QMainWindow):
    
    def __init__(self,profile,themes,preferences,bookmarks,intercepting,dir):
        super(Window, self).__init__()
        self.themes = themes
        self.page = QWebEnginePage(profile)
        self.preferences = preferences
        self.bookmarks = bookmarks
        self.dir = dir
        self.intercepting = intercepting
        
        self.signal_emitter = SignalEmitter()
        self.loaded_tab = self.signal_emitter.loaded_tab
        self.theme_changed = self.signal_emitter.theme_changed
        
        #self.setCentralWidget(self.browser)
        self.home()
        self.showMaximized()
        
        self.toolbar()
        #self.setFont(QFont('Party LET'))
        
        
        
    def browser(self):
        browser = QWebEngineView()    
        browser.setPage(self.page)
        browser.loadFinished.connect(self.updateTab)
        browser.urlChanged.connect(self.updateUrl)
        
        self.PrevBtn.triggered.connect(browser.back)
        self.nextBtn.triggered.connect(browser.forward)
        self.refreshBtn.triggered.connect(browser.reload)
        return browser
    
    def homepage(self):
        homepage = Homepage(self.bookmarks)
        homepage.line.returnPressed.connect(self.loadUrl)
        homepage.line.textEdited.connect(self.setQuery)
        homepage.qss(self.themes.home_style)
        homepage.click.connect(self.load_link)
        return homepage
        
    def menu(self):
        settings = Settings(self.dir)
        settings.qss(self.themes.set_style)
        settings.theme_select.setCurrentText(self.preferences.get_preferences('theme'))
        settings.theme_select.currentTextChanged.connect(self.update_theme)
        settings.font_select.setCurrentText(self.preferences.get_preferences('font'))
        settings.font_select.currentTextChanged.connect(self.update_font)
        settings.engine_select.setCurrentText(self.preferences.get_preferences('engine'))
        settings.engine_select.currentTextChanged.connect(lambda engine: self.preferences.update_preferences('engine',engine))
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
        
        self.bookmarkBtn = QAction('bookmark',self)
        self.bookmarkBtn.triggered.connect(self.bookmark)
        self.navbar.addAction(self.bookmarkBtn)
        
        self.searchBar = QLineEdit()
        self.searchBar.setObjectName('fonted')
        self.searchBar.setPlaceholderText('Search or enter an address')
        
        self.drop_down = QCompleter(['pyqt6','example search','fake query'])
        self.searchBar.setCompleter(self.drop_down)
        
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
                pass
    
    def setQuery(self,text):
        if type(text) is str:
            self.url = text
        elif type(text) is QUrl:
            self.url = text.toString()
        
    def loadUrl(self):
        if self.intercepting.functional is not True:
            func = lambda: self.loadUrl()
            self.intercepting.add_task(func)
        else:
            if self.centralWidget().inherits("QWebEngineView") is not True:
                self.setCentralWidget(self.browser())
            if (engine := self.preferences.get_preferences('engine')) == 'Kagi':   
                search_url = f'https://kagi.com/search?q={self.url}'
            elif engine == 'Google':   
                search_url = f'https://www.google.com/search?q={self.url}'
            elif (engine := self.preferences.get_preferences('engine')) == 'DuckDuckGo':   
                search_url = f'https://duckduckgo.com/?q={self.url}'
            
            if re.match(r'https?:\/\/.',self.url) is not None:
                
                self.centralWidget().setUrl(QUrl(self.url))
                #self.cur.execute("INSERT INTO recent VALUES (?,?,?)", (url,time.time(),True))
                #self.con.commit()
            else:
                self.centralWidget().setUrl(QUrl(search_url))
                #self.cur.execute("INSERT INTO recent VALUES (?,?,?)", (url,time.time(),False))
                #self.con.commit()
    
    def load_link(self,link):
        self.setQuery(link)   
        self.loadUrl() 
    
    def home(self):
        self.loaded_tab.emit( ('New Tab',None) )
        self.setCentralWidget(self.homepage())
    
    def settings(self):
        menu = self.menu()
        self.loaded_tab.emit( ('Settings',None) )
        self.setCentralWidget(menu)
    
    
    def bookmark(self):
        if self.centralWidget().inherits("QWebEngineView") and self.bookmarks.check_bookmark(self.centralWidget().url().toString()):
            
            array = QByteArray()
            buff = QBuffer(array)
            buff.open(QIODevice.OpenModeFlag.WriteOnly)
            icon = self.centralWidget().icon()
            pix = icon.pixmap(QSize(20,20))
            pix.save(buff,'PNG')
            buff.close()
            bytes = array.data()
            
            self.bookmarks.bookmark(self.centralWidget().url().toString(),self.centralWidget().title(),bytes)
            if type( self.centralWidget() ) is Homepage:  self.centralWidget().set_bookmarks()
        
    def updateTab(self):    
        self.loaded_tab.emit( ( self.centralWidget().title() , self.centralWidget().icon() ) )
     
    def update_theme(self,theme):
        self.themes.update(theme)
        self.theme_changed.emit(self.themes.main_style)
        self.preferences.update_preferences('theme',theme)
    def update_font(self,font):
        self.themes.update(None,font)
        self.theme_changed.emit(self.themes.main_style)
        self.preferences.update_preferences('font',font)
        
    def load_theme(self):
        if type(self.centralWidget()).__name__ == 'Homepage':
            self.centralWidget().qss(self.themes.home_style)
            
        elif type(self.centralWidget()).__name__ == 'Settings':
            
            self.centralWidget().qss(self.themes.set_style)
    
