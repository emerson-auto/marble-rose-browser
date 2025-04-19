import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3

class Settings(QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()
        
        #QFontDatabase.addApplicationFont("./Unnamed.ttf")
        self.setFont(QFont('Courier'))
        
        container = QWidget()
        
        container.setObjectName('container')
        background = QWidget()
        background.setObjectName('background')
        menu = QWidget()
        menu.setObjectName('menu')
        
        
        theme_title = QLabel('Themes')
        theme_title.setObjectName('title')
        theme_title.setMaximumHeight(30)
        theme_title.setMaximumWidth(200)
        theme_title.setFont(QFont('Times New Roman'))
        
        title_lay = QHBoxLayout()
        title_lay.addStretch(50)
        title_lay.addWidget(theme_title)
        title_lay.addStretch(50)
        
        title = QWidget()
        title.setLayout(title_lay)
        title.setMaximumWidth(300)
        
        self.theme_select = QComboBox()
        self.theme_select.addItems(['plain','ace','aroace','enby'])
        self.theme_select.setObjectName('options')
        self.theme_select.setMaximumWidth(300)
        #self.theme_select.setFont(QFont('Unnamed'))
        
        
        
        menu_lay = QGridLayout()
        menu_lay.setRowMinimumHeight(0, 20)
        menu_lay.setRowMinimumHeight(4,500)
        menu_lay.setRowMinimumHeight(1,10)
        menu_lay.setRowMinimumHeight(2,20)
        menu_lay.setColumnMinimumWidth(0,200)
        menu_lay.setColumnMinimumWidth(1,300)
        menu_lay.setColumnMinimumWidth(2,200)
        
        
        menu_lay.addWidget(title,0,1)
        menu_lay.addWidget(self.theme_select,1,1)
        
        menu.setLayout(menu_lay)
        menu.setMaximumWidth(700)
        
        
        self.page = QHBoxLayout()
        self.page.addWidget(menu)
        self.page.addWidget(background)
        
        container.setLayout(self.page)
        self.setCentralWidget(container)
        self.showMaximized()
        
    def qss(self,qss):
        #print('yippee')
        self.setStyleSheet(qss)


#MyApp = QApplication(sys.argv)
#test = Settings()
#test.show()
#MyApp.setStyle('Mac')
#MyApp.exec()