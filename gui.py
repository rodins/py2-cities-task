# -*- coding: UTF-8 -*-
# Gui
import pygtk
pygtk.require('2.0')
import gtk

import os
import sys

from async_task import AsyncTask
from db_loader import DbLoader
from info_loader import InfoLoader

class Gui(gtk.Window):
    def __init__(self):
        super(Gui, self).__init__()
        
        SPINNER_SIZE = 32
        LIST_SIZE = 210
        self.LABEL_NO_INFO = 'No info'
        
        self.connect("destroy", self.on_destroy)
        self.set_border_width(5)
        self.set_size_request(780, 400)
        try:
            self.set_icon_from_file(
                os.path.join(sys.path[0], "images", "city-64.png"))
            self.COUNTRY_ICON = gtk.gdk.pixbuf_new_from_file(
                os.path.join(sys.path[0], "images", "countries-16.png"))

            self.CITY_ICON = gtk.gdk.pixbuf_new_from_file(
                os.path.join(sys.path[0], "images", "city-16.png"))
        except Exception, e:
            print e.message
        self.set_title("Cities info")

        self.sp_countries = gtk.Spinner()
        self.sp_countries.set_size_request(SPINNER_SIZE, SPINNER_SIZE)

        self.countries_store = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.cb_countries = self.create_combo_box(self.countries_store)
        self.cb_countries.connect("changed", self.cb_countries_changed)
        self.cb_countries.show()

        self.btn_countries_error = gtk.Button("Retry")
        self.btn_countries_error.connect("clicked", self.btn_countries_error_clicked)

        vb_countries = gtk.VBox(False, 1)
        vb_countries.pack_start(self.sp_countries, False, False, 1)
        vb_countries.pack_start(self.cb_countries, False, False, 1)
        vb_countries.pack_start(self.btn_countries_error, False, False, 1)
        vb_countries.show()
        
        fr_countries = gtk.Frame("Countries")
        fr_countries.add(vb_countries)
        fr_countries.show()

        self.cities_store = gtk.ListStore(gtk.gdk.Pixbuf, str)
        tv_cities = self.create_tree_view()
        tv_cities.set_model(self.cities_store)
        tv_cities.connect("row-activated", self.on_cities_activated)
        sw_cities = self.create_scrolled_window()
        sw_cities.add(tv_cities)
        fr_cities = gtk.Frame("Cities")
        fr_cities.add(sw_cities)
        fr_cities.show_all()

        vb_left = gtk.VBox(False, 1)
        vb_left.set_size_request(LIST_SIZE, -1)
        vb_left.pack_start(fr_countries, False, False, 1)
        vb_left.pack_start(fr_cities, True, True, 1)
        vb_left.show()
        
        self.sp_info = gtk.Spinner()
        self.sp_info.set_size_request(SPINNER_SIZE, SPINNER_SIZE)
        self.lb_info = gtk.Label(self.LABEL_NO_INFO)
        self.lb_info.set_line_wrap(True)
        self.lb_info.show()
        btn_info_error = gtk.Button("Retry")
        btn_info_error.connect("clicked", self.btn_info_error_clicked)
        btn_info_error.show()
        self.hb_info_error = gtk.HBox(False, 1)
        self.hb_info_error.pack_start(btn_info_error, True, False, 1)

        self.im_info = gtk.Image()
        
        vb_info = gtk.VBox(False, 1)
        vb_info.pack_start(self.sp_info, True, False, 1)
        vb_info.pack_start(self.im_info, True, True, 1)
        vb_info.pack_start(self.lb_info, True, True, 1)
        vb_info.pack_start(self.hb_info_error, True, False, 1)
        vb_info.show()
        
        fr_info = gtk.Frame("Info")
        fr_info.add(vb_info)
        fr_info.show()
        
        hbox = gtk.HBox(False, 1)
        hbox.pack_start(vb_left, False, False, 1)
        hbox.pack_start(fr_info, True, True, 1)
    
        self.add(hbox)
        hbox.show()
        self.show()

        self.db_loader = DbLoader(self)
        self.load_countries()

        self.info_loader = InfoLoader(self)

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

    def create_combo_box(self, store):
        combo_box = gtk.ComboBox(store)
        
        renderer_pixbuf = gtk.CellRendererPixbuf()
        combo_box.pack_start(renderer_pixbuf, False)
        combo_box.add_attribute(renderer_pixbuf, 'pixbuf', 0)

        renderer_text = gtk.CellRendererText()
        combo_box.pack_start(renderer_text, False)
        combo_box.add_attribute(renderer_text, 'text', 1)

        return combo_box
        
    def on_destroy(self, widget):
        gtk.main_quit()
        
    def btn_countries_error_clicked(self, widget):
        self.load_countries()

    def create_scrolled_window(self):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        return scrolled_window

    def show_loading_indicator(self):
        self.sp_countries.show()
        self.sp_countries.start()
        self.cb_countries.hide()
        self.btn_countries_error.hide()

    def show_data(self):
        self.sp_countries.hide()
        self.sp_countries.stop()
        self.cb_countries.show()

    def show_error(self):
        self.sp_countries.hide()
        self.sp_countries.stop()
        self.cb_countries.hide()
        self.btn_countries_error.show()

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

    def load_city_info(self, city):
        self.info_loader.city = city
        task = AsyncTask(self.info_loader)
        task.start()

    def retry_load_city_info(self):
        task = AsyncTask(self.info_loader)
        task.start()
        
    def cb_countries_changed(self, combobox):
        countries_iter = combobox.get_active_iter()
        values = self.countries_store.get(countries_iter, 1, 2)
        self.info_loader.country = values[0]
        self.cities_store.clear()
        self.load_cities(values[1]) # pass country_id

    def on_cities_activated(self, treeview, path, view_column):
        cities_iter = self.cities_store.get_iter(path)
        values = self.cities_store.get(cities_iter, 1)
        self.load_city_info(values[0])

    def show_info_loading_indicator(self):
        self.sp_info.show()
        self.sp_info.start()
        self.im_info.hide()
        self.lb_info.hide()
        self.hb_info_error.hide()

    def show_info_data(self):
        self.sp_info.hide()
        self.sp_info.stop()
        self.lb_info.show()
        self.hb_info_error.hide()

    def show_info_error(self):
        self.sp_info.hide()
        self.sp_info.stop()
        self.lb_info.hide()
        self.hb_info_error.show()

    def btn_info_error_clicked(self, widget):
        self.retry_load_city_info()

    def set_text_to_lb_info(self, text):
        self.lb_info.set_markup(text)

    def set_info_image(self, pixbuf):
        self.im_info.show()
        self.im_info.set_from_pixbuf(pixbuf)
        
        
