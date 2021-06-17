Robot lab prometheus exporters for lab sensors and robot status/statistics

We monitor Temperature, Humidity and Air Pressure with Prometheus and Visualize it in the “Robot Lab Grafana Dashboard”. This is done with a BME280 sensor that is connected to an Arduino Nano. Sensor values are read with a Python [sensor_client_bme280.py](sensor_client_bme280.py) using serial communication over USB 2.0 cable. The reading of sensor values are triggered by a Prometheus Exporter (implemented in Python).

## Arduino
```
# Install arduino-cli
cd /tmp
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
sudo mv bin/arduino-cli /usr/local/bin/

# setup arduini-cli
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:megaavr

# Add user to serial user group
sudo usermod -a -G dialout $USER
# Logout from computer (for getting the usermod changes)
```

# Arduino Lib requirements
```
arduino-cli lib install "Adafruit BME280 Library"@1.0.10
```

## Python
```
# create and activate venv
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Debugging serial
```
# Minicom is an OK serial consol program for Linux
 
minicom -b 9600 --noinit -D /dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_6EB94DED51514743594A2020FF06191B-if00

# Switch on Local Echo with Ctl + A and then E
