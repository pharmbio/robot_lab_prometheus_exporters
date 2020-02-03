import prometheus_client
import time
import psutil

# this might be the better way to code: https://github.com/prometheus/client_python/blob/master/README.md

UPDATE_PERIOD = 300
LAB_SENSUS = prometheus_client.Gauge('robot_lab_sensus',
                                       'Holdis robot lab sensor status',
                                       ['resource_type'])

if __name__ == '__main__':
  prometheus_client.start_http_server(9999)
  
while True:
  LAB_SENSUS.labels('temp_1').set("getTemp1()")
  LAB_SENSUS.labels('humid_1').set("getHumid1()")
  time.sleep(UPDATE_PERIOD)
