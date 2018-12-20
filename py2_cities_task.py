# -*- coding: UTF-8 -*-
# py2_cities_task.py
import urllib2
import json
import sqlite3

import gtk
import gobject

from gui import Gui

##conn = sqlite3.connect('cities.db')
##cur = conn.cursor()
##
##def print_countries():
##    for country_id, country in cur.execute('SELECT * FROM countries'):
##        print country
##
##
##def print_cities(country_id):
##    for city, in cur.execute('SELECT city FROM cities WHERE country_id=?',
##                             (country_id,)):
##        print city
##        
##def load_db():
##    cur.execute('CREATE TABLE countries (id INTEGER PRIMARY KEY, country TEXT) WITHOUT ROWID')
##    cur.execute('CREATE TABLE cities (city TEXT, country_id INTEGER, FOREIGN KEY(country_id) REFERENCES countries(id))')
##
##    link = "https://raw.githubusercontent.com/David-Haim/CountriesToCitiesJSON/master/countriesToCities.json"
##    try:
##        print "Loading data into database..."
##        response = urllib2.urlopen(link)
##        js = json.load(response)
##        country_id = 1;
##        for country in js:
##            cur.execute('INSERT INTO countries VALUES (?, ?)',
##                        (country_id, country))
##            for city in js[country]:
##                cur.execute('INSERT INTO cities VALUES(?, ?)',
##                            (city, country_id))
##            country_id += 1
##        conn.commit()
##    except Exception as ex:
##        print ex
##
##try:
##    print_countries()
##    print_cities(93)
##except sqlite3.OperationalError as ex:
##    print ex
##    load_db()
##    print_db()
##conn.close()


def main():
    gobject.threads_init()
    Gui()
    gtk.main()

if __name__ == "__main__":
    main()

    
    
    
    
