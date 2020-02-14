#!/usr/bin/env python3
import logging
import traceback
import time
import prometheus_client
from prometheus_client import Gauge
import sensor_client_bme280


# this might be the better way to code: https://github.com/prometheus/client_python/blob/master/README.md


SERIAL_DEVICE_BME280 = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_6EB94DED51514743594A2020FF06191B-if00'
UPDATE_PERIOD = 10 # in sec
TEMP_SENSOR_BME280 = prometheus_client.Gauge('temp_sensor_bme280',
                                             'Temperature sensor BME280',
                                             ['location'])
HUMID_SENSOR_BME280 = prometheus_client.Gauge('humidity_sensor_bme280',
                                             'Humidity sensor BME280',
                                             ['location'])
PRESSURE_SENSOR_BME280 = prometheus_client.Gauge('pressure_sensor_bme280',
                                             'Air pressure sensor BME280',
                                             ['location'])

def readSensorBME280Temp(sensor, location, serial_device):
  value = sensor_client_bme280.getTemperature(serial_device)
  sensor.labels(location).set(value)
  logging.info("value read: " + str(value))

def readSensorBME280Humid(sensor, location, serial_device):
  value = sensor_client_bme280.getHumidity(serial_device)
  sensor.labels(location).set(value)
  logging.info("value read: " + str(value))

def readSensorBME280Pressure(sensor, location, serial_device):
  value = sensor_client_bme280.getPressure(serial_device)
  sensor.labels(location).set(value)
  logging.info("value read: " + str(value))


if __name__ == '__main__':
  #
  # Configure logging
  #
  logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

  prometheus_client.start_http_server(9999)
  
  while True:
    logging.info("Hello")
    try:
      readSensorBME280Temp(TEMP_SENSOR_BME280, 'inside', SERIAL_DEVICE_BME280)
      readSensorBME280Humid(HUMID_SENSOR_BME280, 'inside', SERIAL_DEVICE_BME280)
      readSensorBME280Pressure(PRESSURE_SENSOR_BME280, 'inside', SERIAL_DEVICE_BME280)
    except Exception as e:
      print(traceback.format_exc())
      logging.error(e)

    time.sleep(UPDATE_PERIOD)