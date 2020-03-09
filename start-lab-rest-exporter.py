#!/usr/bin/env bash

#
# Startup script for webserver
#
echo "Activate venv"
source "/pharmbio/robot_lab_ptometheus_exporters/venv/bin/activate"

echo "Start exporter"
python /pharmbio/robot_lab_ptometheus_exporters/lab-rest-exporter.py
