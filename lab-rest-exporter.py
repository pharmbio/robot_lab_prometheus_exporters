#!/usr/bin/env python3
import logging
import traceback
import time
import prometheus_client
from prometheus_client import Gauge
import requests
import json


# this might be the better way to code: https://github.com/prometheus/client_python/blob/master/README.md

UPDATE_PERIOD = 60 # in sec

SHAKER_URL = 'http://shaker.lab.pharmb.io:5000/is_ready'
INCUBATOR_URL = 'http://incubator.lab.pharmb.io:5001/is_ready'
WASHER_URL = 'http://washer.lab.pharmb.io:5000/is_ready'
DISPENSER_URL = 'http://dispenser.lab.pharmb.io:5001/is_ready'

ROBOT_STATUS_GAUGE = prometheus_client.Gauge('robots_ready_status',
                                             'Robots ready status API',
                                             ['robot'])


def getIsReadyValue(gauge, url, location):
  response = requests.get(url, timeout=1)
  logging.debug(str(response.content))
  data = json.loads(response.content)
  value = data['value']
  logging.debug(str(gauge.describe()) + " = " + str(url) + " = " + str(value))
  gauge.labels(location).set(value)


if __name__ == '__main__':
  #
  # Configure logging
  #
  logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

  prometheus_client.start_http_server(10002)

  while True:
    logging.info("Hello")
    try:
      getIsReadyValue(ROBOT_STATUS_GAUGE, SHAKER_URL, 'shaker')
      getIsReadyValue(ROBOT_STATUS_GAUGE, INCUBATOR_URL, 'incubator')
      getIsReadyValue(ROBOT_STATUS_GAUGE, WASHER_URL, 'washer')
      getIsReadyValue(ROBOT_STATUS_GAUGE, DISPENSER_URL, 'dispenser')
    except Exception as e:
      print(traceback.format_exc())
      logging.error(e)

    time.sleep(UPDATE_PERIOD)
