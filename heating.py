import gevent.monkey
gevent.monkey.patch_all()
import requests
from requests.exceptions import Timeout
import pandas as pd
import json
import os
import time
import datetime
from datetime import timedelta
import numpy as np
#import timeseries as ts
# import app_config as cfg
import paho.mqtt.client as paho
import math as m
# config = cfg.getconfig()
global cross_tags
from dataExchangelmpl import dataEx,config



currentTimeStamp = int(time.time()*1000)


currentTime = datetime.datetime.now()
currentMonth = currentTime.month
currentQuarter = (currentMonth-1)//3 + 1
currentDay = currentTime.day
currentHour = currentTime.hour
currentMinute =  currentTime.minute
currentSecond = currentTime.second
last5Minute = abs(currentMinute - 5)
validMonth = currentMonth - (currentQuarter-1)*3

startDate = "2022/{}/{} {}:{}:{}".format(validMonth,currentDay,currentHour,last5Minute,currentSecond)
endDate = "2022/{}/{} {}:{}:{}".format(validMonth,currentDay,currentHour,currentMinute,currentSecond)

startDate = datetime.datetime.strptime(startDate, '%Y/%m/%d %H:%M:%S')
endDate = datetime.datetime.strptime(endDate, '%Y/%m/%d %H:%M:%S')

print(startDate,endDate)

startTimestamp=time.mktime(startDate.timetuple())*1000
endTimestamp=time.mktime(endDate.timetuple())*1000


unitsId = "61c0c34bb45a623b64fc3b12"
dataEx = dataEx()
# try:
    # dataEx.getLoginToken()
# except:
    # dataEx.getLoginToken()

tag_df = dataEx.getTagmeta(unitsId)

tagList = list(tag_df["dataTagId"]) + ['CEN1_Direct_Boiler_Efficiency'] + ['CEN1_BLR1_STEAM_GEN_HRLY','CEN1_BLR1_FUEL_CONS_HRLY','CEN1_1_boiler_Efficiency_prc_hourly']

dataEx.dataExachangeHeating(tagList,startTimestamp,endTimestamp)