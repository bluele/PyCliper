#-*- coding:utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT

from os.path import join, dirname, abspath
import Tkinter as Tk
from tkhandlers import TkHandler
from ScrolledText import ScrolledText
from lib.observer import clipobserver
from lib.util import logger

class TkBaseWindow:
        
    def setUp(self):
        '''
        @summary: 
            widget類の配置を行います
        '''
        self.setUpMenuBar()
        
        main_frame = Tk.PanedWindow(self.app)
        main_frame.pack(expand = True, fill = Tk.BOTH)
        tool_frame = Tk.PanedWindow(main_frame, orient = 'vertical')
        clip_frame = Tk.PanedWindow(tool_frame, orient = 'vertical')
        
        self.listBox = self.setUpListBox(main_frame)
        self.statusbar = self.setUpStatusBar(tool_frame)
        
        main_frame.add(self.listBox)
        main_frame.add(tool_frame)
        
        tool_frame.add(self.setUpToolBar(tool_frame))
        tool_frame.add(self.statusbar)
        #tool_frame.add(self.setUpAutoChangeBox())
        tool_frame.add(clip_frame)
        
        self.clip_before = self.setUpClipArea(clip_frame) 
        self.clip_after = self.setUpClipArea(clip_frame)
        
        clip_frame.add(self.setBeforeLabel(clip_frame))
        clip_frame.add(self.clip_before)
        clip_frame.add(self.setAfterLabel(clip_frame))
        clip_frame.add(self.clip_after)
        
        self.setUpWindow()
        
    def setUpWindow(self):
        '''
        @summary: 
            windowの配置を行います
        '''
        window = self.app.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        #ウインドウの生成位置を指定
        self.app.geometry("{0}x{1}+{2}+{3}".format(500, 500,
                                                    0, 50))
        self.app.title("PyCliper")
        
    def setUpAutoChangeBox(self):
        '''
        @summary: 
            自動変換の真偽のチェックボックスを生成します
        '''
        self.is_auto = Tk.BooleanVar()
        self.is_auto.set(False)
        return Tk.Checkbutton(text = u'自動変換', variable = self.is_auto, justify = Tk.LEFT)
        
    def setUpClipArea(self, frame):
        '''
        @summary: 
            クリップボートの表示エリアを作成します
        '''
        xscrollbar = Tk.Scrollbar(frame, orient=Tk.HORIZONTAL)
        st = ScrolledText(frame, bg="GRAY", xscrollcommand=xscrollbar.set, height=10)
        st.config(state=Tk.DISABLED)
        return st
    
    def setBeforeLabel(self, frame):
        '''
        @summary: 
            ハンドラの変換前のラベルを作成します
        '''
        label = Tk.Label(frame, text=u"変換前のクリップボート",
                             anchor=Tk.W, bg="cyan")
        return label
        
    def setAfterLabel(self, frame):
        '''
        @summary: 
            ハンドラの変換後のラベルを作成します
        '''
        label = Tk.Label(frame, text=u"変換後のクリップボート",
                             anchor=Tk.W, bg="red")
        return label
        
    def setUpMenuBar(self):
        '''
        @summary: 
            メニューバーを作成します
        '''
        menubar = Tk.Menu(self.app)
        self.app["menu"] = menubar
        # create filemenu
        fileMenu = Tk.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                                                    ("Add New Plugin", self.loadPlugin, "Ctrl+N", "<Control-n>"),
                                                    ("Change Plugin Directory", self.changePluginPath, "Ctrl+P", "<Control-p>"),
                                                    (None, None, None, None),
                                                    ):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label, underline=0,
                                     command=command, accelerator=shortcut_text)
                self.app.bind(shortcut, command)
        menubar.add_cascade(label="File", menu=fileMenu, underline=0)
        
    def setUpToolBar(self, frame):
        '''
        @summary: 
            ツールバーを作成します
        '''
        toolbar = Tk.Frame(frame)
        for image, command in (
                           ("images/gif/Refresh.gif", self.refreshList),    # handlerリストの更新 
                           ("images/gif/Red Mark.gif", self.selectHandler), # ハンドラの選択
                           ("images/gif/Add.gif", self.loadPlugin),  # プラグインのインポート
                           ("images/gif/Folder.gif", self.changePluginPath) # プラグインディレクトリの変更を行います
                           ):
            image = join(dirname(dirname(__file__)), image)
            try:
                image = Tk.PhotoImage(file=image)
                self.toolbar_images.append(image)
                button = Tk.Button(toolbar, image=image,
                                   command=command)
                button.grid(row=0, column=len(self.toolbar_images) -1)
            except Tk.TclError, err:
                logger.error(err)
        return toolbar
    
    def setUpListBox(self, frame):
        '''
        @summary: 
            リストボックスを作成します
        '''
        listBox = Tk.Listbox(frame)
        sbv = Tk.Scrollbar(frame, orient = 'v', command = listBox.yview)
        sbh = Tk.Scrollbar(frame, orient = 'h', command = listBox.xview)

        listBox.configure(yscrollcommand = sbv.set)
        listBox.configure(xscrollcommand = sbh.set)
        listBox.bind('<Double-1>', self.selectHandler)
        listBox.focus_set()
        return listBox
        
    def setUpStatusBar(self, frame):
        '''
        @summary: 
            ステータスバーを作成します
        '''
        statusbar = Tk.Label(frame, text=u"初期化中...",
                             anchor=Tk.W, )
        return statusbar
    
    def bootEvent(self):
        '''
        @summary: 
            イベントの開始メソッド
        '''
        clip = clipobserver(self)
        self.listBox.after(2000, clip.run)
        self.app.after(1000, self.refreshList)
        self.statusbar.after(3000, lambda:self.setStatusBar(u"ハンドラを選択してください"))


class TkWindow(TkBaseWindow, TkHandler):
    
    def __init__(self, app):
        self.app = app
        self.toolbar_images = []
        self.handlers = {}
        self.plugin_path = join(dirname(dirname(abspath(__file__))), u"plugins")
        self.mod_pat = [u".py$"]  # モジュールとして読み込むパターンリスト(正規表現)
        self.current_handler = None
        self.setUp()
        
