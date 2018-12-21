# -*- coding: UTF-8 -*-
# Gui
import pygtk
pygtk.require('2.0')
import gtk

import os
import sys

from async_task import AsyncTask
from db_loader import DbLoader

class Gui(gtk.Window):
    def __init__(self):
        super(Gui, self).__init__()
        
        self.SPINNER_SIZE = 32
        self.connect("destroy", self.on_destroy)
        self.set_border_width(5)
        self.set_size_request(780, 400)
        #TODO: set application image
        try:
            self.COUNTRY_ICON = gtk.gdk.pixbuf_new_from_file(
                os.path.join(sys.path[0], "images", "countries-16.png"))

            self.CITY_ICON = gtk.gdk.pixbuf_new_from_file(
                os.path.join(sys.path[0], "images", "city-16.png"))
        except Exception, e:
            print e.message
        self.set_title("Cities info")

        self.sp_load_db = gtk.Spinner()
        self.sp_load_db.set_size_request(self.SPINNER_SIZE, self.SPINNER_SIZE)

        self.countries_store = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        tv_countries = self.create_tree_view()
        tv_countries.set_model(self.countries_store)
        selection = tv_countries.get_selection()
        selection.connect("changed", self.countries_selection_changed)
        sw_countries = self.create_scrolled_window()
        sw_countries.add(tv_countries)
        self.fr_countries = gtk.Frame("Countries")
        self.fr_countries.add(sw_countries)
        self.fr_countries.show_all()

        self.cities_store = gtk.ListStore(gtk.gdk.Pixbuf, str)
        tv_cities = self.create_tree_view()
        tv_cities.set_model(self.cities_store)
        tv_cities.connect("row-activated", self.on_cities_activated)
        sw_cities = self.create_scrolled_window()
        sw_cities.add(tv_cities)
        fr_cities = gtk.Frame("Cities")
        fr_cities.add(sw_cities)
        fr_cities.show_all()
        
        btn_load_db_error = gtk.Button("Retry")
        btn_load_db_error.connect("clicked", self.btn_load_db_error_clicked)
        btn_load_db_error.show()
        self.vb_load_db_error = gtk.VBox(False, 1)
        self.vb_load_db_error.pack_start(btn_load_db_error, True, False, 10)
        
        hbox = gtk.HBox(False, 5)
        hbox.pack_start(self.sp_load_db, True, False, 1)
        hbox.pack_start(self.vb_load_db_error, True, False, 1)
        hbox.pack_start(self.fr_countries, True, True, 5)
        hbox.pack_start(fr_cities, True, True, 5)
    
        self.add(hbox)
        hbox.show()
        self.show()

        self.db_loader = DbLoader(self)
        self.load_countries()

    def create_tree_view(self):
        tree_view = gtk.TreeView()
    
        renderer_pixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn("Image", renderer_pixbuf, pixbuf=0)
        tree_view.append_column(column)
        
        renderer_text = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Title", renderer_text, text=1)
        tree_view.append_column(column)
        
        tree_view.set_headers_visible(False)
        
        return tree_view

    def on_destroy(self, widget):
        gtk.main_quit()
        
    def btn_load_db_error_clicked(self, widget):
        self.load_counries()

    def create_scrolled_window(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        return scrolled_window

    def show_loading_indicator(self):
        self.sp_load_db.show()
        self.sp_load_db.start()
        self.fr_countries.hide()
        self.vb_load_db_error.hide()

    def show_data(self):
        self.sp_load_db.hide()
        self.sp_load_db.stop()
        self.fr_countries.show()

    def show_error(self):
        self.sp_load_db.hide()
        self.sp_load_db.stop()
        self.fr_countries.hide()
        self.vb_load_db_error.show()

    def add_to_countries_model(self, title, country_id):
        self.countries_store.append([self.COUNTRY_ICON, title, country_id])

    def add_to_cities_model(self, title):
        self.cities_store.append([self.CITY_ICON, title])

    def load_countries(self):
        task = AsyncTask(self.db_loader)
        task.start()

    def load_cities(self, country_id):
        self.db_loader.country_id = country_id
        task = AsyncTask(self.db_loader)
        task.start()
        
    def countries_selection_changed(self, selection):
        model, countries_iter = selection.get_selected()
        values = model.get(countries_iter, 2)
        self.cities_store.clear()
        self.load_cities(values[0])

    def on_cities_activated(self, treeview, path, view_column):
        cities_iter = self.cities_store.get_iter(path)
        values = self.cities_store.get(cities_iter, 1)
        print values[0]
        
