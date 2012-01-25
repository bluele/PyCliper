#-*- coding:utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT
import Tkinter as Tk
import os
from os.path import basename, join, exists, dirname
import shutil
import re
from tkforms import askdirectory
import tkFileDialog as filedialog
from util import logger

class TkHandler():
    '''
    @summary: 
        ウィジェットからのインタフェースメソッド
    '''
    
    def refreshList(self):
        '''
        @summary: 
            Tk.aferから呼ばれるイベントメソッド
            ハンドラのリスト一覧を更新します
        '''
        self.listBox.delete(0, Tk.END)
        self.handlers.clear()
        self._loadHandlerList()
        for hname in self.handlers:
            self.listBox.insert(Tk.END, hname)
        
    def _loadHandlerList(self):
        '''
        @summary: 
            ハンドラ一覧を取得します
        '''
        # 取得ファイルパターンの構築
        repat = re.compile(u"|".join(self.mod_pat))
        try:
            for file in os.walk(self.plugin_path).next()[2]:#ファイルのみ抽出
                if repat.search(file) != None:
                    self.handlers[file] = join(self.plugin_path, file)
        except StopIteration:
            pass
        
    def selectHandler(self, *ignore):
        '''
        @summary: 
            変換ハンドラの選択メソッド
            listboxのカーソルのあったインデックスを取得（タプル） 
        @todo: 
            ハンドラセット前にモジュールの存在確認を行った方がよさそう
        '''    
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        name = self.listBox.get(index)
        handler = self.handlers.get(name)
        if handler is None:
            return
        self.current_handler = name
        self.setStatusBar(u"現在のハンドラ : %s" % str(name))
        
    def setStatusBar(self, text, timeout=None):
        '''
        @summary: 
            ステータスバーに文字列を表示します
        @param timeout: float: None以外を指定することで、指定時間後にクリアされます
        '''
        self.statusbar["text"] = text
        if timeout:
            self.statusbar.after(timeout, self.clearStatusBar)

    def clearStatusBar(self):
        '''
        @summary: 
            ステータスバーの文字列を非表示にします
        '''
        self.statusbar["text"] = ""

    def loadPlugin(self):
        '''
        @summary:
            Plugin Moduleをロードします
        @todo: 
            仕様を考える　選択したモジュールをディレクトリにコピーするのか、モジュールパスを追加するのか　前者がシンプル
        '''
        filename = filedialog.askopenfilename(filetypes = [('Python Script', ('.py', '.pyc')),],
                                              initialdir = dirname(__file__))
        if filename != "":
            dist_path = join(self.plugin_path, basename(filename))
            if exists(dist_path):
                # ここで上書き確認
                logger.error("Already exists %s" % dist_path)
                return False
            shutil.copyfile(filename, dist_path)
            self.refreshList()
            
    def changePluginPath(self):
        '''
        @summary: 
            プラグインの格納パスを変更します
        '''
        #self.plugin_pat
        dir_path = askdirectory()
        if dir_path == '':
            return False
        self.plugin_path = dir_path
        self.refreshList()
            
    def fileQuit(self, event=None):
        '''
        @summary: 
            終了処理を行います
        '''
        if self.okayToContinue():
            self.app.destroy()

    def okayToContinue(self):
        '''
        @summary: 
            終了処理を行います
        @return: bool: Trueを返すとアプリケーションが終了します
        '''
        return True
