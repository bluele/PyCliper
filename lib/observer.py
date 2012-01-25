# -*- coding: utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT

from Tkinter import NORMAL, DISABLED, END, TclError
from lib.util import logger, SelectedHandler
from lib.errors import NoHandlerError
from os.path import join, basename
import imp
_clipboard_set = None
_clipboard_get = None
try:
    import lib.clipboard
    _clipboard_set = lib.clipboard.clipboard_set
    _clipboard_get = lib.clipboard.clipboard_get
except Exception, err:
    pass
    
class clipobserver():
    
    def __init__(self, parent=None):
        self.last_text = ""
        self.last_handler = SelectedHandler()
        self.parent = parent
        self.app = parent.listBox
        self.setUpClipboard()
        
    def setUpClipboard(self):
        '''
        @summary: 
            クリップボートのアクセサの初期化を行います
        '''
        if _clipboard_set is None or _clipboard_get is None:
            self.clipboard_set = self._tkClipboardSet
            self.clipboard_get = self.app.clipboard_get
        else:
            self.clipboard_set = _clipboard_set
            self.clipboard_get = _clipboard_get
            
    def _tkClipboardSet(self, text):
        '''
        @summary: 
            Tkinterのクリップボートのセッターです
        '''
        self.app.clipboard_clear()
        self.app.clipboard_append(text)
        
    def run(self):
        '''
        @summary: 
            ハンドラ処理の実行メソッドです
        '''
        try:
            text = self.clipboard_get()
            mod_path = self.getPluginPath()
            if self.last_text != text or self.last_handler.path != mod_path:
                self._run(text, mod_path)
        except TclError, err:
            logger.error(err)
        except NoHandlerError:
            self.defaultHandle(text)
        self.app.after(500, self.run)
        
    def _run(self, text, path):
        '''
        @summary: 
            テキストに対してハンドラ処理を行い、
            結果をクリップボートにセットします
        @param text: クリップボートの中身
        @param path: ハンドラモジュールのパス
        '''
        result = None
        try:
            self.setClipBefore(text)
            mod = self.loadModule(path)
            self.last_handler.set_handler(mod.handler, path)
            try:
                result = mod.handler(text)
            except Exception, err:
                self.errorHandler(text, err)
        except AttributeError:
            logger.error("Perhaps don't have your selected handler 'handler' method ?")
        if result is not None:
            try:
                self.last_text = result
                self.clipboard_set(result)
                self.setClipAfter(result)
            except Exception, err:
                logger.error(err)
                
    def loadModule(self, path):
        '''
        @summary: 
            指定されたパスのモジュールをロードします
        '''
        return imp.load_source(basename(path).rstrip('py'), path)
    
    def errorHandler(self, text, err=None):
        '''
        @summary: 
            ハンドラがエラー発生時の処理を行います
        '''
        self.last_text = text
        logger.error(err)
    
    def defaultHandle(self, text):
        '''
        @summary: 
            ハンドラが設定されていないときのデフォルトの動作を指定します
        '''
        if self.last_text != text:
            self.last_text = text
            self.setClipBefore(text)
            self.setClipAfter(text)
                
    def setClipBefore(self, text):
        '''
        @summary: 
            クリップボートに変換前のテキストをセットします
        '''
        self.parent.clip_before.config(state=NORMAL)
        self.parent.clip_before.delete(0.0, END)
        self.parent.clip_before.insert(0.0, text)
        self.parent.clip_before.config(state=DISABLED)
        
    def setClipAfter(self, text):
        '''
        @summary: 
            クリップボートに変換後のテキストをセットします
        '''
        self.parent.clip_after.config(state=NORMAL)
        self.parent.clip_after.delete(0.0, END)
        self.parent.clip_after.insert(0.0, text)
        self.parent.clip_after.config(state=DISABLED)
    
    def getPluginPath(self):
        '''
        @summary: 
            現在選択されているプラグインモジュールのパスを取得します
            なにも選択されていないときはNoneを返します
        '''
        mod_name = self._getModuleName()
        if mod_name is None:
            raise NoHandlerError
        return join(self.parent.plugin_path, mod_name)
        
    def _getModuleName(self):
        '''
        @summary: 
            アプリケーション側で保持されている現在のハンドラ名を取得します
        '''
        return self.parent.current_handler
        