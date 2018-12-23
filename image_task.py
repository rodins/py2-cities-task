# -*- coding: UTF-8 -*-

import gtk
import gobject

import threading
import urllib2

class ImageTask(threading.Thread):
    def __init__(self,  gui, link):
        self.gui = gui
        self.link = link
        self.pixbuf_loader = gtk.gdk.PixbufLoader()
        self.pixbuf_loader.connect("area-prepared", self.pixbuf_loader_prepared)
        threading.Thread.__init__(self)
        
    def pixbuf_loader_prepared(self, pixbufloader):
        pixbuf = pixbufloader.get_pixbuf()
        self.gui.set_info_image(pixbuf)
        
    def write_to_loader(self, buf):
        self.pixbuf_loader.write(buf)
        
    def on_post_execute(self):
        if self.pixbuf_loader.close():
            pixbuf = self.pixbuf_loader.get_pixbuf()
            self.gui.set_info_image(pixbuf)
        else:
            print "pixbuf error"
        
    def run(self):
        try:
            response = urllib2.urlopen(self.link)
            for buf in response:
                gobject.idle_add(self.write_to_loader, buf)
        except Exception as ex:
            print ex
        gobject.idle_add(self.on_post_execute)
