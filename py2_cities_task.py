# -*- coding: UTF-8 -*-
# py2_cities_task.py
import urllib2
import json

link = "https://raw.githubusercontent.com/David-Haim/CountriesToCitiesJSON/master/countriesToCities.json"
try:
    response = urllib2.urlopen(link)
    js = json.load(response)
    for country in js:
        print country
        for city in js[country]:
            print '\t' + city
except Exception as ex:
    print ex
    
    
