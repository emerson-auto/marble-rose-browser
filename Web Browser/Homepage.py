import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3
import time


class Homepage(QMainWindow):
    def __init__(self):
        super(Homepage, self).__init__()
        container = QWidget()
        container.setObjectName('background')
        layout = QVBoxLayout()
        bar = QHBoxLayout()
        logo = QHBoxLayout()
        self.line = QLineEdit()
        title = QLabel('The Browser™')
        
        title.setFont(QFont('Times New Roman'))
        title.setMaximumHeight(100)
        
        self.line.setMinimumSize(0,50)
        self.line.setFont(QFont('Times New Roman'))
        self.line.setPlaceholderText('Search or enter an address')
        
        logo.addStretch(10)
        logo.addWidget(title)
        logo.addStretch(10)
        
        bar.addStretch(5)
        bar.addWidget(self.line,10)
        bar.addStretch(5)
        
        layout.addStretch(10)
        layout.addItem(logo)
        layout.addStretch(2)
        layout.addItem(bar)
        layout.addWidget(QWidget(),10)
        #layout.addWidget(QWidget,3,2)
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.showMaximized()
        
    def qss(self,qss):
        self.setStyleSheet(qss)
    
        
#MyApp = QApplication(sys.argv)
#test = Homepage()
#test.show()

#MyApp.exec()
        