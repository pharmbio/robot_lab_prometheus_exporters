#!/bin/bash
NAME=arduino_environment_sensors_v_adafruit_1.0.10
FBQN=arduino:megaavr:nona4809
DEVICE=/dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_6EB94DED51514743594A2020FF06191B-if00
# the arduino-cli program doesn't work if you try to upload to the symbolic link /dev/serial/by-id/ so we
# get the actual device with readlink program
PORT=$(readlink -f "$DEVICE")
arduino-cli compile --fqbn $FBQN $NAME
if [ $? -ne 0 ]; then
    echo "compile error, exit here"
    exit
fi
arduino-cli upload -v -p $PORT --fqbn $FBQN $NAME

