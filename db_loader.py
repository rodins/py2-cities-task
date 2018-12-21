# -*- coding: UTF-8 -*-
import os
import sys
import gobject

import urllib2
import json
import sqlite3

class DbLoader:
    def __init__(self, gui):
        self.NO_COUNTRY_ID = -1
        self.DATA_URL = "https://raw.githubusercontent.com/David-Haim/CountriesToCitiesJSON/master/countriesToCities.json"
        self.gui = gui
        self.country_id = self.NO_COUNTRY_ID
        self.db_directory = os.path.join(sys.path[0], 'data')
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)

    def open_connection(self):
        self.conn = sqlite3.connect(
            os.path.join(self.db_directory, 'cities.db'))
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
        
    def load(self):
        self.open_connection()
        if self.country_id == self.NO_COUNTRY_ID:
            try:
                self.add_countries_to_model()
            except sqlite3.OperationalError as ex:
                # No table found in db
                print ex
                self.get_data_from_net()
        else:
            self.add_cities_to_model()
        self.close_connection()

    def add_countries_to_model(self):
        for country_id, country in self.cur.execute('SELECT * FROM countries'):
            gobject.idle_add(
                self.gui.add_to_countries_model, country, country_id)

    def add_cities_to_model(self):
        for city, in self.cur.execute('SELECT city FROM cities WHERE country_id=?',
                                (self.country_id,)):
            gobject.idle_add(
                self.gui.add_to_cities_model, city)

    def create_tables(self):
        self.cur.execute('CREATE TABLE countries (id INTEGER PRIMARY KEY, country TEXT) WITHOUT ROWID')
        self.cur.execute('CREATE TABLE cities (city TEXT, country_id INTEGER, FOREIGN KEY(country_id) REFERENCES countries(id))')

    def get_data_from_net(self):
        try:
            gobject.idle_add(self.gui.show_loading_indicator)
            response = urllib2.urlopen(self.DATA_URL)
            js = json.load(response)
            self.create_tables()
            country_id = 1;
            for country in js:
                if country != '':
                    self.cur.execute('INSERT INTO countries VALUES (?, ?)',
                                (country_id, country))
                    for city in js[country]:
                        if city != '':
                            self.cur.execute('INSERT INTO cities VALUES(?, ?)',
                                        (city, country_id))
                    country_id += 1
            self.conn.commit()
            self.add_countries_to_model()
            gobject.idle_add(self.gui.show_data)
        except Exception as ex:
            print ex
            gobject.idle_add(self.gui.show_error)

    
