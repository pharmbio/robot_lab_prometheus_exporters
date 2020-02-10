#include <Adafruit_BME280.h>

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme; // use I2C interface
 
bool DEBUG = false;

int8_t START_BYTE = '0';
int8_t END_BYTE = '\n';

int8_t OK = '1';
int8_t ERROR_WRONG_START_BYTE = '2';
int8_t ERROR_UNKNOWN_OPTION = '3';
int8_t ERROR_WRONG_END_BYTE = '4';

int8_t OPTION_GET_TEMP = 'a';
int8_t OPTION_GET_HUMID = 'b';
int8_t OPTION_GET_PRESSURE = 'c';

void setup() {
    Serial.setTimeout(1000);
    // set the baud rate 
    Serial.begin(9600);
    // time to get serial running
    while(!Serial);
    
    if(DEBUG){
       Serial.println("Serial started");
    }

    if (!bme.begin()) {
       Serial.println(F("Could not find a valid BME280 sensor, check wiring!"));
    }
/*
    if(DEBUG){
       bme_temp->printSensorDetails();
       bme_pressure->printSensorDetails();
       bme_humidity->printSensorDetails();

       sensors_event_t temp_event;
       bme_temp->getEvent(&temp_event);
       writeOptionResponse(OPTION_GET_TEMP, temp_event.temperature);
    }
  */  
}

void loop() {
  if(Serial.available() > 2){
    
      int8_t startByte = Serial.read();
      if(startByte == START_BYTE){
        
          int8_t option = Serial.read();
          executeOption(option);
          
          int8_t endByte = Serial.read();
          if(endByte != END_BYTE){
             writeError(ERROR_WRONG_END_BYTE);
          }
      }
      else{
          writeError(ERROR_WRONG_START_BYTE);
      }
     
  }
  delay(10); // wait a little bit
}


void executeOption(int8_t option){
  
    if(option == OPTION_GET_TEMP){
        writeOptionResponse(OPTION_GET_TEMP, bme.readTemperature());
    }
    else if(option == OPTION_GET_HUMID){
        writeOptionResponse(OPTION_GET_HUMID, bme.readHumidity());
    }
    else if(option == OPTION_GET_PRESSURE){
        writeOptionResponse(OPTION_GET_PRESSURE, bme.readPressure());
    }
    else{
      writeError(ERROR_UNKNOWN_OPTION);
    }
}

void writeOptionResponse(int8_t option, float value){
        Serial.write(START_BYTE);
        Serial.write(option);
        writeFloat(value);
        Serial.write(END_BYTE);
}

void writeFloat(float arg) {
  // get float as a byte-array:
  byte * data = (byte *) &arg; 
  Serial.write(data, 4);
}

void writeError(int8_t errorCode){
  Serial.write(START_BYTE);
  Serial.write(errorCode);
  Serial.write(END_BYTE);
}
