from adblockparser import AdblockRules
import PyQt6
from PyQt6.QtWebEngineCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import urllib3
from gunicorn.config import CACerts
import certifi
import time

class IntRun(QRunnable):
    def __init__(self,emitter):
        super(IntRun,self).__init__()
        self.emitter = emitter
        
    def run(self):
        rules_assembler = RulesAssembler()
        print('interceptor created at ' + str( time.time() ))
        self.emitter.assembly_completed(rules_assembler)
        print('signal emitted at ' + str( time.time() ))

class RulesAssembler:
    def __init__(self):
        super(RulesAssembler,self).__init__()
        print('rules assembler initalized at ' + str( time.time() ))
        con = urllib3.connection_from_url('https://easylist.to', ca_certs= certifi.where() , cert_reqs='REQUIRED')
        print('connection established at ' + str( time.time() ))
        
        resp = con.request("GET", 'https://easylist.to/easylist/easylist.txt')
        print('easylist requested at ' + str( time.time() ))
        
        raw_rules = resp.data.decode('utf-8').splitlines()
        print('easylist decoded at ' + str( time.time() ))
        
        self.rules = AdblockRules(raw_rules)
        print('rules initalized at ' + str( time.time() ))
        
        pr_resp = con.request("GET", 'https://easylist.to/easylist/easyprivacy.txt')
        print('easyprivacy requested at ' + str( time.time() ))
        
        pr_raw_rules = pr_resp.data.decode('utf-8').splitlines()
        print('easyprivacy decoded at ' + str( time.time() ))
        
        self.pr_rules = AdblockRules(pr_raw_rules)
        print('privacy rules initalized at ' + str( time.time() ))

class RulesAssemblerEmitter(QObject):
    rules_assembled = pyqtSignal(RulesAssembler)
    def __init__(self,parent=None):
        super().__init__(parent)
    
    # assembly_progress( self, nameOfSubTask, percentageDone )
    
    def assembly_completed(self,rules_assembler):
        self.rules_assembled.emit(rules_assembler)

class Interceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, rules, pr_rules, parent =None):
        super(Interceptor,self).__init__( parent )
        self.rules = rules
        self.pr_rules = pr_rules

    def interceptRequest(self, info:QWebEngineUrlRequestInfo )->None:
        request = info.requestUrl().toString()
        if self.rules.should_block(request) or self.pr_rules.should_block(request):
            info.block(True)
            print('blocked this url: ' + request)