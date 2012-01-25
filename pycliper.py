#!/usr/bin/env python
#-*- coding:utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT

import Tkinter as Tk
from lib import tkwindows

def boot_strap():
    application = Tk.Tk()
    return application

def main():
    application = boot_strap()
    window = tkwindows.TkWindow(application)
    window.bootEvent()
    application.protocol("WM_DELETE_WINDOW", window.fileQuit)
    application.mainloop()
  
if __name__ == '__main__':
    main()

