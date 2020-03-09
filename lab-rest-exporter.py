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
SHAKER_STATUS_GAUGE = prometheus_client.Gauge('shaker',
                                             'Shaker status API',
                                             ['location'])

INCUBATOR_URL = 'http://incubator.lab.pharmb.io:5001/is_ready'
INCUBATOR_STATUS_GAUGE = prometheus_client.Gauge('incubator',
                                             'Incubator status API',
                                             ['location'])

WASHER_URL = 'http://washer.lab.pharmb.io:5000/is_ready'
WASHER_STATUS_GAUGE = prometheus_client.Gauge('washer',
                                             'Washer status API',
                                             ['location'])

DISPENSER_URL = 'http://dispenser.lab.pharmb.io:5001/is_ready'
DISPENSER_STATUS_GAUGE = prometheus_client.Gauge('dispenser',
                                             'Dispenser status API',
                                             ['location'])

def getIsReadyValue(gauge, url, location):
  response = requests.get(url, timeout=1)
  logging.debug(str(response.content))
  data = json.loads(response.content)
  value = data['value']
  boolValue = int(value == 'True')
  logging.debug(str(gauge.describe()) + " = " + str(url) + " = " + str(boolValue))
  gauge.labels(location).set(boolValue)


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
      getIsReadyValue(SHAKER_STATUS_GAUGE, SHAKER_URL, 'inside')
      getIsReadyValue(INCUBATOR_STATUS_GAUGE, INCUBATOR_URL, 'inside')
      getIsReadyValue(WASHER_STATUS_GAUGE, WASHER_URL, 'inside')
      getIsReadyValue(DISPENSER_STATUS_GAUGE, DISPENSER_URL, 'inside')
    except Exception as e:
      print(traceback.format_exc())
      logging.error(e)

    time.sleep(UPDATE_PERIOD)
