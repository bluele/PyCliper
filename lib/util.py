# -*- coding: utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT

import os
import sys
import logging

logger = None
def set_logger():
    global logger
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s (%(threadName)-2s) %(message)s',
                    #filename='/tmp/pycliper.log',
                    #filemode='w'
                    )
    logger = logging.getLogger("server")
    
def setup():
    if logger is None:
        set_logger()
setup()

class PluginPath():
    
    _default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"plugins")
    
    def __init__(self, path=None):
        if path is None:
            path = self._default_path
        self.path = path
        sys.path.append(self.path)
        
    def __str__(self):
        return self.path
    
    def set_path(self, path):
        self.path = path

        
def defaultHandle(text):
    '''
    @summary: 
        デフォルトのハンドラです
    '''
    return text
        
class SelectedHandler():
    '''
    @summary: 
        現在選択中のハンドラの管理クラス
    '''
    __slots__ = ('handle', 'path')
    def __init__(self, handle=defaultHandle, path=None):
        self.handle = handle
        self.path = path
        
    def set_handler(self, handle, path):
        self.handle = handle
        self.path = path
        