# -*- coding: UTF-8 -*-
import gobject

import urllib
import urllib2
import json
from xml.sax import saxutils

from image_task import ImageTask

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

    def is_feature_city(self, item):
        try:
            return item['feature'] == 'city'
        except:
            return item['title'].find(self.city) == 0

    def load_image(self, link):
        task = ImageTask(self.gui, link)
        task.start()

    def parse_response(self, response):
        js = json.load(response)
        try:
            for item in js['geonames']:
                if self.is_feature_city(item):
                    self.load_image(item['thumbnailImg'])
                    return ('<b>' +
                            saxutils.escape(item['title']) +
                            '</b> \n\n <i>' +
                            saxutils.escape(item['summary']) +
                            '</i> \n\n Latitude: ' +
                            str(item['lat']) +
                            ' \n Longitude: ' +
                            str(item['lng']))
        except:
            return self.gui.LABEL_NO_INFO
        return self.gui.LABEL_NO_INFO
        
