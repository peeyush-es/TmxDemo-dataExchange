import os
import time
import json
import redis
import pickle
import random
import logging
import requests
import grequests
import utils as ut
import numpy as np
import pandas as pd
import timeseries as ts
import app_config as cfg
from flask_cors import CORS
import paho.mqtt.client as mqtt
from subprocess import Popen, PIPE
from datetime import datetime, timedelta, date
from flask import Flask, jsonify, request, abort
from apscheduler.schedulers.background import BackgroundScheduler


config = cfg.getconfig()
#loadTagLimit = config["loadTagLimit"]
#loadBucketSize = config["loadBucketSize"]
redis = redis.StrictRedis(host='vml-2',db=0)

# logging.basicConfig(filename='log/data-api/kairos.log', filemode='a', format='%(name)s - {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
def getLastValues(taglist,end_absolute=0):
    if end_absolute !=0:
        query = {"metrics": [],"start_absolute": 1, end_absolute: end_absolute}
    else:
        query = {"metrics": [],"start_absolute":1}
    for tag in taglist:
        query["metrics"].append({"name": tag,"order":"desc","limit":1})
    try:
        res = requests.post(config['api']['query'],json=query).json()
        df = pd.DataFrame([{"time":res["queries"][0]["results"][0]["values"][0][0]}])
        for tag in res["queries"]:
            try:
                if df.iloc[0,0] <  tag["results"][0]["values"][0][0]:
                    df.iloc[0,0] =  tag["results"][0]["values"][0][0]
                df.loc[0,tag["results"][0]["name"]] = tag["results"][0]["values"][0][1]
            except:
                pass
    
    except Exception as e:
        print(e)
        return pd.DataFrame()
    return df
    


_redis_data_ = {}
cooling_df = getLastValues(["TJY_ABS_PMP_DO"])
print(cooling_df)
heating_df = getLastValues(["DUN_M24_T"])
res = redis.set("62b4012d1bb30160b7ec85c9-shadow",cooling_df.loc[0,"time"])
print(res)
res = redis.set("62b3f0ae1bb30160b7ec8385-shadow",heating_df.loc[0,"time"])
print(res)

wws_df = getLastValues(["WWS1_BL_01"])
res = redis.set("63288a244512494172eb0cde-shadow",wws_df.loc[0,"time"])
print(res)

chemicals_df = getLastValues(["SMR_CORROSION"])

res = redis.set("6328837c4512494172eb0c2d-shadow",chemicals_df.loc[0,"time"])
print(res)

try:
    print("shadow")
    keys = ["62b3f0ae1bb30160b7ec8385-shadow","62b4012d1bb30160b7ec85c9-shadow","63288a244512494172eb0cde-shadow","6328837c4512494172eb0c2d-shadow"]

# print(len(keys))
    if len(keys) <= 120:
       
       for key in keys:
          value = redis.get(key)
          if value:
             value = float(redis.get(key))
          _redis_data_[key] = value
       print("req done")
       print json.dumps(_redis_data_)
    else:
       print json.dumps({}), 200
except Exception as e:
    print('-----error----')
    print(e)
    logging.info(e)

