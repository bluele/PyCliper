#-*- coding:utf-8 -*-
# PyCliper
# Copyright 2011-2012 Jun Kimura
# LICENSE MIT

from tkCommonDialog import Dialog
from os.path import dirname, abspath

class Chooser(Dialog):

    command = "tk_chooseDirectory"

    def _fixresult(self, widget, result):
        if result:
            # keep directory until next time
            self.options["initialdir"] = result
        self.directory = result # compatibility
        return result
#
# convenience stuff

def askdirectory(**options):
    "Ask for a directory name"
    if options.has_key('initialdir'):
        options["initialdir"] = dirname(abspath(__file__))
        print dirname(abspath(__file__))
    return apply(Chooser, (), options).show()
