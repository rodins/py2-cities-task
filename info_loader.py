# -*- coding: UTF-8 -*-
import gobject

import urllib
import urllib2
import json
from xml.sax import saxutils

class InfoLoader:
    def __init__(self, gui):
        self.gui = gui
        self.API_DOMAIN = 'http://api.geonames.org/wikipediaSearchJSON?'
        self.TIMEOUT = 15
        self.username = 'rodins'
        self.country = ''
        self.city = ''

    def build_url(self):
        data = {}
        data['q'] = self.country
        data['title'] = self.city # search city name in title
        data['username'] = self.username
        url_values = urllib.urlencode(data)
        return self.API_DOMAIN + url_values

    def load(self):
        if self.city != '':
            try:
                link = self.build_url()
                gobject.idle_add(self.gui.show_info_loading_indicator)
                response = urllib2.urlopen(link, None, self.TIMEOUT)
                text = self.parse_response(response)
                gobject.idle_add(self.gui.set_text_to_lb_info, text)
                gobject.idle_add(self.gui.show_info_data)
            except Exception as ex:
                gobject.idle_add(self.gui.show_info_error)
                print ex

    def parse_response(self, response):
        js = json.load(response)
        #print js['geonames'][0]['title']
        for item in js['geonames']:
            title = item['title']
            # City name should be first in title
            if title.find(self.city) == 0:
                return '<b>' + saxutils.escape(title) + '</b> \n\n <i>' + saxutils.escape(item['summary'])+ '</i>'
        return "No info"
        
