#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import hashlib
import json
import time


class LocationSearch:
    def __init__(self, project_name, api_key, city_code):

        # set up API data
        self.project = project_name
        self.apikey = api_key
        self.city_code = city_code

        # create MD5 checksum to verfiy your identity at wetter.com API
        self.checksum = self.project+self.apikey+self.city_code
        self.md5_sum = hashlib.md5(self.checksum).hexdigest()

        def search_all(search_value):
            pass

        def search_country(search_value):
            pass

        def search_plz(search_value):
            pass




class WeatherForecast:
    def __init__(self, project_name, api_key, city_code):
        # set up API data
        self.project = project_name
        self.apikey = api_key
        self.city_code = city_code

        # create MD5 checksum to verfiy your identity at wetter.com API
        self.checksum = self.project+self.apikey+self.city_code
        self.md5_sum = hashlib.md5(self.checksum).hexdigest()
        self.url = "http://api.wetter.com/forecast/weather/city/{0}/project/{1}\
/cs/{2}/output/json".format(self.city_code, self.project, self.md5_sum)

        # get date and hour to read API results
        self.api_date = self.__get_date_str()
        self.api_hour = self.__get_hour()

        self.high_temp = None
        self.low_temp = None
        self.ave_temp = None
        self.weather_text = None
        self.rain_chance = None
        self.icon_code = None
        self.wind_speed = None
        self.wind_direction = None


    def __get_date_str(self):
        #create time string of the following format: "dd-mm-yyyy"
        t = time.localtime()
        yy = str(t[0])
        mm = str(t[1])
        dd = str(t[2])

        if len(mm) == 1:
            mm = "0"+mm
        if len(dd) == 1:
            dd = "0"+dd

        return yy+"-"+mm+"-"+dd


    def __get_hour(self):
        # get a hour to ask wetter.com API, cause the API offers 4 Times:
        # 06:00, 11:00, 17:00 and 23:00, so you have to select the time which is
        # nearly at the current real time - this function is doing this!

        # get current real time hour
        t = time.localtime()
        h = t[3]

        # check which of the API hours is nearby
        if h in [22,23,0,1,2,3,4]:
            used_h = "23:00"
        if h >= 5 and h <=10:
            used_h = "06:00"
        if h >= 11 and h <= 15:
            used_h = "11:00"
        if h >= 16 and h <= 21:
            used_h = "17:00"

        return used_h


    def get_forecast(self, wind_named=False):
        forecast_status = None

        # read data as JSON and transform it this way to a dict
        try:
            print "fetching data from API..."
            f = urllib2.urlopen(self.url)
            data = json.load(f)
            forecast_status = True
        except:
            print "Could not connect to the wetter.com server - sorry, please \
check your internet connection and possible server down times."
            forecast_status = False

        # read the forecast basis in the variable
        if forecast_status:
            forecast = data["city"]["forecast"][self.api_date][self.api_hour]
            self.high_temp = forecast["tx"]
            self.low_temp = forecast["tn"]
            self.ave_temp = str((int(self.high_temp) + int(self.low_temp)) / 2)
            self.weather_text = forecast["w_txt"]
            self.rain_chance = forecast["pc"]
            self.icon_code = forecast["w"][0] # used for pictures, code is just first num
            self.wind_speed = forecast["ws"]

            if wind_named:
                self.wind_direction = self.__get_wind_direction_name(forecast["wd"])
            else:
                self.wind_direction = forecast["wd"]
        else:
            print "WARNING: could not get forecast!"


    def __get_wind_direction_name(self, direction):
        directions = {  "0":"Norden", "45":"Nord-Osten", "90":"Osten",
                        "135":u"Südosten","180":u"Süden", "225":u"Süd-Westen",
                        "270":"Westen"}
        return directions[direction]
