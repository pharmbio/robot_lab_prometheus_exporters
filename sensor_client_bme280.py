#!/usr/bin/env python3
import logging
import traceback
import serial
import serial.tools.list_ports
import time
import struct

BAUD_RATE = 9600

START_BYTE = b'0'
END_BYTE = b'\n'

OK = b'1'
ERROR_WRONG_START_BYTE = b'2'
ERROR_UNKNOWN_OPTION = b'3'
ERROR_WRONG_END_BYTE = b'4'

OPTION_GET_BME280_TEMP = b'a'
OPTION_GET_BME280_HUMID = b'b'
OPTION_GET_BME280_PRESSURE = b'c'

SERIAL_DEVICE = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_6EB94DED51514743594A2020FF06191B-if00'

def getFloatFromServer(server, option):
    # send message to server
    server.write(START_BYTE)
    server.write(option)
    server.write(END_BYTE)

    # read response
    start_byte = server.read(1)
    response_option = server.read(1)
    float_as_bytes = server.read(4)
    endbyte = server.read(1)

    # check response
    if(start_byte != START_BYTE):
        raise Exception("Error wrong startbyte:" + str(start_byte) + " expected: " + str(START_BYTE))

    if(option != response_option):
        raise Exception("Error wrong response option:" + str(response_option) + " expected: " + str(option))

    if(endbyte != END_BYTE):
        raise Exception("Error wrong endbyte:" + str(endbyte) + " expected: " + str(START_BYTE))

    # cast to float and return
    float_as_struct = struct.unpack('f', float_as_bytes)
    return float_as_struct[0]

def getSerialConnection(serial_device, baud_rate, timeout=2):
    conn = serial.Serial(serial_device, baud_rate, timeout=2)
    while(conn.isOpen() == False):
        time.sleep(0.05)
    
    conn.reset_input_buffer()
    conn.reset_output_buffer()

    time.sleep(0.01)

    return conn

def getTemperature(serial_device):
    server_conn = getSerialConnection(serial_device, BAUD_RATE)
    temperature = getFloatFromServer(server_conn, OPTION_GET_BME280_TEMP)
    return temperature

def getHumidity(serial_device):
    server_conn = getSerialConnection(serial_device, BAUD_RATE)
    humidity = getFloatFromServer(server_conn, OPTION_GET_BME280_HUMID)
    return humidity

def getPressure(serial_device):
    server_conn = getSerialConnection(serial_device, BAUD_RATE)
    pressure = getFloatFromServer(server_conn, OPTION_GET_BME280_PRESSURE)
    return pressure

#
# Main
#
if __name__ == '__main__':

    #
    # Configure logging
    #
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
    # print("Before get temp")

    temperature = getTemperature(SERIAL_DEVICE)
    print("Temperature = " + str(temperature / 100) + " °C")

    pressure = getPressure(SERIAL_DEVICE)
    print("Pressure = " + str(pressure / 100) + " hPa")

    humidity = getHumidity(SERIAL_DEVICE)
    print("Humidity = " + str(humidity) + " %")
