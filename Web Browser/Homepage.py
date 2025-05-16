import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re
import sqlite3
import time
from BookWidget import BookWidget

class SignalEmitter(QObject):
    click = pyqtSignal(str)
    
class Homepage(QWidget):
    def __init__(self,bookmarks):
        super(Homepage, self).__init__()
        
        self.bookmarks = bookmarks
        self.emitter = SignalEmitter()
        self.click = self.emitter.click
        
        self.container = QWidget()
        self.layout = QVBoxLayout()
        bar = QHBoxLayout()
        logo = QHBoxLayout()
        self.line = QLineEdit()
        title = QLabel('The Browser™')
        title.setObjectName('title')
        
        title.setMaximumHeight(100)
        
        self.line.setMinimumSize(0,50)
        self.line.setPlaceholderText('Search or enter an address')
        
        logo.addStretch(10)
        logo.addWidget(title)
        logo.addStretch(10)
        
        bar.addStretch(5)
        bar.addWidget(self.line,10)
        bar.addStretch(5)
        
        self.layout.addStretch(10)
        self.layout.addItem(logo)
        self.layout.addStretch(2)
        self.layout.addItem(bar)
        self.layout.addStretch(2)
        self.set_bookmarks()
        self.layout.addStretch(10)
        
        
        
        self.container.setLayout(self.layout)
        temp = QHBoxLayout()
        temp.addWidget(self.container)
        self.container.setObjectName('homepage')
        self.setLayout(temp)
        
    def qss(self,qss):
        self.setStyleSheet(qss)
    
    def url(self):
        return 'home'
    
    def set_bookmarks(self):
        book_lay = BookWidget(self.bookmarks.get_bookmarks())
        book_lay.bookmark_clicked.connect(lambda url: self.click.emit(url))
        bookmarks = QWidget()
        bookmarks.setLayout(book_lay)
        bookmarks.setObjectName('BookWidget')
        self.layout.addWidget(bookmarks)
        
#MyApp = QApplication(sys.argv)
#test = Homepage()
#test.show()

#MyApp.exec()
        