import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3

class Settings(QWidget):
    def __init__(self,dir):
        super(Settings, self).__init__()
        self.dir = dir
        QFontDatabase.addApplicationFont(f"{dir}/Unnamed.ttf")
        
        self.setObjectName('container')
        background = QWidget()
        background.setObjectName('background')
        menu = QWidget()
        menu.setObjectName('menu')
        
        themes = ['plain','ace','aroace','enby','gender queer']
        theme_title,self.theme_select = self.make_pref('Themes', themes)
        
        fonts = ['Times New Roman','Courier New','Unnamed','Chalkduster','Party LET']
        font_title,self.font_select = self.make_pref('Fonts', fonts)
        
        engines = ['Google','Kagi','DuckDuckGo']
        engine_title,self.engine_select = self.make_pref('Engines',engines)
        
        menu_lay = QGridLayout()
        menu_lay.setRowMinimumHeight(0,100)
        menu_lay.setRowMinimumHeight(1,30)
        menu_lay.setRowMinimumHeight(3,30)
        menu_lay.setRowMinimumHeight(4,30)
        menu_lay.setRowMinimumHeight(6,200)
        menu_lay.setColumnMinimumWidth(0,200)
        menu_lay.setColumnMinimumWidth(1,300)
        menu_lay.setColumnMinimumWidth(2,200)
        
        
        menu_lay.addWidget(theme_title,0,1)
        menu_lay.addWidget(self.theme_select,1,1)
        menu_lay.addWidget(font_title,2,1)
        menu_lay.addWidget(self.font_select,3,1)
        menu_lay.addWidget(engine_title,4,1)
        menu_lay.addWidget(self.engine_select,5,1)
        
        menu.setLayout(menu_lay)
        menu.setMaximumWidth(700)
        
        
        self.page = QHBoxLayout()
        self.page.addWidget(menu)
        self.page.addWidget(background)
        
        self.setLayout(self.page)
        self.showMaximized()
        
    def make_pref(self,pref,options):
        title = QLabel(pref)
        title.setMaximumHeight(30)
        title.setMaximumWidth(200)
        title.setObjectName('title')
        
        lay = QHBoxLayout()
        lay.addStretch(50)
        lay.addWidget(title)
        lay.addStretch(50)
        
        group = QWidget()
        group.setLayout(lay)
        group.setMaximumWidth(300)
        
        select = QComboBox()
        select.addItems(options)
        select.setMaximumWidth(300)
        select.setObjectName('options')
        return group,select
        
    def qss(self,qss):
        #print('yippee')
        self.setStyleSheet(qss)
        
    def url(self):
        return 'settings'
    

#MyApp = QApplication(sys.argv)
#test = Settings()
#test.show()
#MyApp.setStyle('Mac')
#MyApp.exec()