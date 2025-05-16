import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from string import Template

class Themes:
    def __init__(self,theme,font,dir):
        
        self.dir = dir
        print(self.dir)
        
        self.bl_main = dict( C1='black',C2='black',C3='red', C4='black',C5='red',C6='black',C7='red',C8='red',C9='red',C10='black')
        self.bl_home = dict(IM1=f'url({self.dir}/qss-bl/background)',C1='black',C2='red',C3='#DD0000')
        self.bl_set = dict(IM1=f'url({self.dir}/qss-bl/settings-background)',C1='black',C2='black',C3='red',C4='red',C5='black')
        
        self.ac_main = dict(C1='black',C2='#800080',C3='black',C4='black',C5='#A3A3A3',C6='white',C7='black',C8='black',C9='#800080',C10='black')
        self.ac_home = dict(IM1=f'url({self.dir}/qss-ac/background.jpg)',C1='#A3A3A3',C2='black',C3='#800080')
        self.ac_set = dict(IM1=f'url({self.dir}/qss-ac/settings-background)',C1='#853085',C2='black',C3='black',C4='black',C5='#A3A3A3')
        
        self.ar_main = dict(C1='black',C2='#800080',C3='black',C4='black',C5='#A3A3A3',C6='white',C7='black',C8='black',C9='#800080',C10='black')
        self.ar_home = dict(IM1=f'url({self.dir}/qss-ac/background.jpg)',C1='#A3A3A3',C2='black',C3='#800080')
        self.ar_set = dict(IM1=f'url({self.dir}/qss-ac/settings-background)',C1='#853085',C2='black',C3='black',C4='black',C5='#A3A3A3')
        
        self.aa_main = dict(C1='#ef9007',C2='#eccd00',C3='black',C4='#1e3f54',C5='#62aedc',C6='#62aedc',C7='black',C8='black',C9='#eccd00',C10='black')
        self.aa_home = dict(IM1=f'url({self.dir}/qss-aa/background.jpg)',C1='#eccd00',C2='black',C3='#62aedc')
        self.aa_set = dict(IM1=f'url({self.dir}/qss-aa/settings-background)',C1='#1e3f54',C2='#ef9007',C3='black',C4='black',C5='#f6d317')
        
        self.nb_main = dict(C1='#FCF434',C2='white',C3='black',C4='black',C5='#9C59D1',C6='black',C7='white',C8='#9C59D1',C9='#9C59D1',C10='black')
        self.nb_home = dict(IM1=f'url({self.dir}/qss-nb/background.svg)',C1='#9C59D1',C2='black',C3='#FCF434')
        self.nb_set = dict(IM1=f'url({self.dir}/qss-nb/settings-background)',C1='black',C2='#9C59D1',C3='white',C4='#9C59D1',C5='blacks')
        
        self.gq_main = dict(C1='#4A8123',C2='#B57EDC',C3='white',C4='#4A8123',C5='white',C6='white',C7='#B57EDC',C8='#B57EDC',C9='#B57EDC',C10='white')
        self.gq_home = dict(IM1=f'url({self.dir}/qss-gq/background)',C1='white',C2='#B57EDC',C3='#4A8123')
        self.gq_set = dict(IM1=f'url({self.dir}/qss-gq/settings-background)',C1='#4A8123',C2='#B57EDC',C3='#B57EDC',C4='#B57EDC',C5='white')
        
        self.style_main = {'plain': self.bl_main, 'ace': self.ac_main, 'aroace': self.aa_main, 'enby': self.nb_main, 'gender queer' : self.gq_main, 'aro': self.ar_main}
        self.style_home = {'plain': self.bl_home, 'ace': self.ac_home, 'aroace': self.aa_home, 'enby': self.nb_home, 'gender queer' : self.gq_home, 'aro': self.ar_home}
        self.style_set = {'plain': self.bl_set, 'ace': self.ac_set, 'aroace': self.aa_set, 'enby': self.nb_set, 'gender queer' : self.gq_set, 'aro': self.ar_set}
                
        self.theme = theme
        self.font = font
        with open(f'{self.dir}/template/browser-style.qss') as raw:
            self.main_template = Template(raw.read())
        with open(f'{self.dir}/template/home-style.qss') as raw:
            self.home_template = Template(raw.read())
        with open(f'{self.dir}/template/settings-style.qss') as raw:
            self.settings_template = Template(raw.read())
            
        self.main_style = self.main_template.safe_substitute(self.style_main[self.theme] | dict(F1=self.font))
        self.home_style = self.home_template.safe_substitute(self.style_home[self.theme])
        self.set_style = self.settings_template.safe_substitute(self.style_set[self.theme])
        
        
    def update(self,theme=None,font=None):
        if theme:
            self.theme = theme
        if font:
            self.font = font
        self.main_style = self.main_template.safe_substitute(self.style_main[self.theme] | dict(F1=self.font))
        self.home_style = self.home_template.safe_substitute(self.style_home[self.theme])
        self.set_style = self.settings_template.safe_substitute(self.style_set[self.theme])


#theme = Themes()