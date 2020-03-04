#!/usr/bin/env python3
import logging
import traceback
import time
import prometheus_client
from prometheus_client import Gauge
import requests
import json


# this might be the better way to code: https://github.com/prometheus/client_python/blob/master/README.md

UPDATE_PERIOD = 2 # in sec

SHAKER_STATUS_GAUGE = prometheus_client.Gauge('shaker',
                                             'Shaker status API',
                                             ['location'])


def getShakerStatus(gauge, location):
  url = 'http://washer.lab.pharmb.io:5000/is_ready'
  response = requests.get(url, timeout=1)
  logging.info(str(response.content))
  data = json.loads(response.content)
  logging.info(str(data))
  value = data['value']
  logging.info(str(value))
  gauge.labels(location).set(value)


if __name__ == '__main__':
  #
  # Configure logging
  #
  logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

  prometheus_client.start_http_server(10002)

  while True:
    logging.info("Hello")
    try:
      getShakerStatus(SHAKER_STATUS_GAUGE, 'inside')
    except Exception as e:
      print(traceback.format_exc())
      logging.error(e)

    time.sleep(UPDATE_PERIOD)
