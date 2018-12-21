# -*- coding: UTF-8 -*-
# py2_cities_task.py
import gtk
import gobject

from gui import Gui

def main():
    gobject.threads_init()
    Gui()
    gtk.main()

if __name__ == "__main__":
    main()

    
    
    
    
