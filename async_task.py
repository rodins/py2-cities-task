# -*- coding: UTF-8 -*-
import threading

class AsyncTask(threading.Thread):
    def __init__(self, loader):
         self.loader = loader
         threading.Thread.__init__(self)

    def run(self):
        self.loader.load()
