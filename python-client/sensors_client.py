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

serial_device = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_6EB94DED51514743594A2020FF06191B-if00'
server = None

def getFloatFromServer(option):
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
        raise Exception("Error wrong startbyte")

    if(option != response_option):
        raise Exception("Error wrong response option")

    if(endbyte != END_BYTE):
        raise Exception("Error wrong endbyte")

    # cast to float and return
    float_as_struct = struct.unpack('f', float_as_bytes)
    return float_as_struct[0]


#
#  
# Start main program
#
#

#
# Configure logging
#
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

# Open named port at “19200,8,N,1”, Xs timeout:
with serial.Serial(serial_device, BAUD_RATE, timeout=2) as server:

    ## Read and discard what is in buffer
    #time.sleep(3)
    while(server.isOpen() == False):
        time.sleep(0.1)
    
    server.reset_input_buffer()
    server.reset_output_buffer()
    
    time.sleep(0.2)

    while(True):
      
      try:
        # Get temp
        temperature = getFloatFromServer(OPTION_GET_BME280_TEMP)
        print("Temperature = " + str(temperature) + " C")

        # Get humidity
        humidity = getFloatFromServer(OPTION_GET_BME280_HUMID)
        print("Humidity = " + str(humidity) + " %")

        # Get pressure
        pressure = getFloatFromServer(OPTION_GET_BME280_PRESSURE)
        print("Pressure = " + str(pressure / 100) + " hPa")
      except Exception as e:
        print(traceback.format_exc())
        logging.error(e)
        time.sleep(1)
        server.reset_input_buffer()
        server.reset_output_buffer()

      time.sleep(1)

