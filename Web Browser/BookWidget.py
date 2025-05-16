from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class SignalEmitter(QObject):
    bookmark_clicked = pyqtSignal(str)

class BookWidget(QHBoxLayout):
    def __init__(self,bookmarks):
        super(BookWidget, self).__init__()
        self.emitter = SignalEmitter()
        self.bookmark_clicked = self.emitter.bookmark_clicked
        self.book_list = []
        
        self.addStretch(20)
        
        for i in bookmarks:
            bookmark = self.make_bookmark(i)
            self.book_list.append(bookmark)
            self.addWidget(bookmark)
            self.addStretch(1)
        self.addStretch(20)
    
    def make_bookmark(self,bookmark):
        lay = QGridLayout()
        
        #site = QPushButton(bookmark[1])
        site_text = QLabel(bookmark[1])
        site_text.setObjectName('booklabel')
        site_text.setWordWrap(True)
        
        site_lay = QHBoxLayout()
        site_lay.addWidget(site_text)
        #site.setLayout(site_lay)
        
        #site.setObjectName('bookbutton')
        #site.setFlat(True)
        #site.clicked.connect(lambda: self.bookmark_clicked.emit( bookmark[0] ) )
        
        if bool(bookmark[2]):
            ba = QByteArray(bookmark[2])
            pix = QPixmap()
            pix.loadFromData(ba, 'PNG')
        else:
            pix = QPixmap()
        pix_cont = QLabel('')
        pix_cont.setObjectName('bookicon')
        pix_cont.setPixmap(pix)
        
        site_text = QLabel(bookmark[1])
        site_text.setObjectName('booklabel')
        site_text.setWordWrap(True)
        site_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        site_lay = QGridLayout()
        site_lay.addWidget(pix_cont,0,1)
        site_lay.addWidget(site_text,1,0,1,3)
        
        #lay.addWidget(pix_cont,0,1)
        #lay.addWidget(site,1,0,1,3)
        
        container = QPushButton()
        container.setObjectName('bookback')
        container.setLayout(site_lay)
        container.clicked.connect(lambda: self.bookmark_clicked.emit( bookmark[0] ) )
        return container