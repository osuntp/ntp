/***************************************************
  This is an example for the Adafruit Thermocouple Sensor w/MAX31855K

  Designed specifically to work with the Adafruit Thermocouple Sensor
  ----> https://www.adafruit.com/products/269

  These displays use SPI to communicate, 3 pins are required to
  interface
  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <SPI.h>
#include "Adafruit_MAX31855.h"

// Default connection is using software SPI, but comment and uncomment one of
// the two examples below to switch between software SPI and hardware SPI:

// Example creating a thermocouple instance with software SPI on any three
// digital IO pins.
#define MAXDO   3
#define MAXCS   4
#define MAXCLK  5

// initialize the Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

// Example creating a thermocouple instance with hardware SPI
// on a given CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS);

// Example creating a thermocouple instance with hardware SPI
// on SPI1 using specified CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS, SPI1);


float value = 0;
unsigned long timeSinceStart = 0;
boolean heaterIsOn = false;

float temperature = 25;
float pressure = 101325;

const byte numChars = 32;
char receivedChars[numChars];
char prefix[numChars];
char message[numChars];
boolean newMessageIsAvailable = false;

void setup() {
  Serial.begin(9600);

  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc
  Serial.print("<id, daq>\n");
  //Serial.println("MAX31855 test");
  // wait for MAX chip to stabilize
  delay(500);
  //Serial.print("Initializing sensor...");
  if (!thermocouple.begin()) {
    Serial.println("ERROR.");
    while (1) delay(10);
  }
  //Serial.println("DONE.");
}

void loop() {

  CheckSerialForMessage();

  if(newMessageIsAvailable)
  {
    HandleNewMessage();
  }

  if(heaterIsOn)
  {
    temperature += random(0,3);
  }
  else
  {
    temperature -= random(0,3);
  }

  pressure += random(-500, 1000);

  Serial.print("<");
  Serial.print("da");
  Serial.print(", ");
  Serial.print(millis());
  Serial.print(", ");
  Serial.print(temperature);
  Serial.print(", ");
  Serial.print(pressure);
  Serial.print(", ");
  Serial.print(heaterIsOn);
  Serial.println(">");
  delay(10);

//  if(Serial.available() > 0)
//  {
////    String message = Serial.readStringUntil('\n');
//
//    char* message = "heater, on\n";
//    
//    char * strtokIndx;
//    strtokIndx = strtok(message, ", ");
//    strcpy(char prefix, index)



//    if(message == "heaterOn")
//    {
//      tempDelta = 1;
//    }
//    else if(message == "heaterOff")
//    {
//      tempDelta = -1;
//    }
//  }

//  temperature += tempDelta

//
//  double temp = thermocouple.readCelsius();
//  double internalTemp = thermocouple.readInternal();
//
//  timeSinceStart = millis();
//
//  Serial.print("da");
//  Serial.print(", ");
//  Serial.print(timeSinceStart);
//  Serial.print(", ");
//  Serial.print(temp);
//  Serial.print(", ");
//  Serial.print(internalTemp);
//  Serial.print("\n");

//   double c = thermocouple.readCelsius();
//   if (isnan(c)) {
//     Serial.println("Something wrong with thermocouple!");
//   } else {
//     //Serial.print("C = ");
//     Serial.println(c);
//   }
//   //Serial.print("F = ");
//   //Serial.println(thermocouple.readFahrenheit());
//   delay(1000);

}

void CheckSerialForMessage()
{
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newMessageIsAvailable == false)
  {
    rc = Serial.read();

    if (recvInProgress == true)
    {
       if(rc != endMarker) 
       {
          receivedChars[ndx] = rc;
          ndx++;
          if (ndx >= numChars)
          {
            ndx = numChars -1;
          }
       }
       else
       {
          receivedChars[ndx] = '\0';
          recvInProgress = false;
          ndx = 0;
          newMessageIsAvailable = true;
       }
    }
    else if (rc == startMarker)
    {
      recvInProgress = true;
    }
  }
}

void HandleNewMessage()
{
  char * strtokIndx;

  strtokIndx = strtok(receivedChars, ", ");
  strcpy(prefix, strtokIndx);
  
  if(strcmp(prefix, "heater") == 0)
  {
    strtokIndx = strtok(NULL, ", ");
    strcpy(message, strtokIndx);


    heaterIsOn = (strcmp(message, "on") == 0);
  }
  

  newMessageIsAvailable = false;
}
