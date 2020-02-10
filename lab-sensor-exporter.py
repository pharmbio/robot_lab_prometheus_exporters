#!/usr/bin/python3
import time
import prometheus_client
from prometheus_client import Gauge
import sensor_client_bme280


# this might be the better way to code: https://github.com/prometheus/client_python/blob/master/README.md

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
  sensor.labels(location).set(sensor_client_bme280.getTemperature())





if __name__ == '__main__':
  prometheus_client.start_http_server(9999)
  
while True:
  readTempSensorBME280(TEMP_SENSOR_BME280, 'cage','/dev/tty...')
  time.sleep(UPDATE_PERIOD)
