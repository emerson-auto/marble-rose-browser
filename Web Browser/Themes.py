import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Themes:
    def __init__(self,theme):
        self.style_dict = {'plain': 'qss-bl', 'ace': 'qss-ac', 'aroace': 'qss-aa', 'bi': 'qss-bi', 'enby': 'qss-nb'}
        self.theme = theme
        self.path = self.style_dict[theme]
        with open(f'./{self.path}/browser-style.qss') as raw:
            self.main_style = raw.read()
        with open(f'./{self.path}/home-style.qss') as raw:
            self.home_style = raw.read()
        with open(f'./{self.path}/settings-style.qss') as raw:
            self.settings_style = raw.read()
        
    def update(self,theme):
        self.theme = theme
        self.path = self.style_dict[theme]
        with open(f'./{self.path}/browser-style.qss') as raw:
            self.main_style = raw.read()
        with open(f'./{self.path}/home-style.qss') as raw:
            self.home_style = raw.read()
        with open(f'./{self.path}/settings-style.qss') as raw:
            self.settings_style = raw.read()
        #print(self.settings_style)


#theme = Themes()