# -*- coding: UTF-8 -*-
# Gui
import pygtk
pygtk.require('2.0')
import gtk

class Gui(gtk.Window):
    def __init__(self):
        super(Gui, self).__init__()
        
        self.SPINNER_SIZE = 32
        self.connect("destroy", self.on_destroy)
        self.set_border_width(5)
        self.set_size_request(780, 400)
        #TODO: set application image
        self.set_title("Cities info")

        self.sp_load_db = gtk.Spinner()
        self.sp_load_db.set_size_request(self.SPINNER_SIZE, self.SPINNER_SIZE)

        countries_store = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        tv_countries = self.create_tree_view()
        tv_countries.set_model(countries_store)
        sw_countries = self.create_scrolled_window()
        sw_countries.add(tv_countries)
        self.fr_countries = gtk.Frame("Countries")
        self.fr_countries.add(sw_countries)
        self.fr_countries.show_all()

        cities_store = gtk.ListStore(gtk.gdk.Pixbuf, str)
        tv_cities = self.create_tree_view()
        tv_cities.set_model(cities_store)
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

        self.show_loading_indicator()

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
        print "Retry load db"

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
        self.vb_load_db_error.show()
    