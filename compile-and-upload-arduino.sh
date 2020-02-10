#!/bin/bash
NAME=arduino_environment_sensors_v_adafruit_1.0.10
FBQN=arduino:megaavr:nona4809
DEVICE=/dev/ttyACM0
arduino-cli compile --fqbn $FBQN $NAME
if [ $? -ne 0 ]; then
    echo "compile error, exit here"
    exit
fi
arduino-cli upload -v -p $DEVICE --fqbn $FBQN $NAME
