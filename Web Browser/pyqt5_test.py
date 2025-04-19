from PyQt5.QtWidgets import *
import time

item = ['cool','super cool','really cool','incredibly cool']
others = ['uncool','not cool', 'really uncool', 'incredibly uncool']
def buttonclick():
    cool_menu.addItem(box.text())
    print(cool_menu.currentText())
app = QApplication([])
tabs = QTabWidget()
#set up app and layout

window = QWidget()
lay = QVBoxLayout()
#add menu to layout
cool_menu = QComboBox()
for i in item:
    cool_menu.addItem(i)
lay.addWidget(cool_menu)
#add input    
box = QLineEdit()
lay.addWidget(box)
#add button
button = QPushButton('whee')
button.clicked.connect(buttonclick)
lay.addWidget(button)
#apply layout and run
window.setLayout(lay)
#other tab
tab = QWidget()
tab_lay = QHBoxLayout()
uncool_menu = QComboBox()
for i in others:
    uncool_menu.addItem(i)
tab_lay.addWidget(uncool_menu)
tab.setLayout(tab_lay)
tabs.addTab(window, 'cool tab')
tabs.addTab(tab,'cool tab')
tabs.show()
app.exec()
