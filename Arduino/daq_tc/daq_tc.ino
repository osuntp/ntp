



/////////////// DEPRECATED

#include <SPI.h>
#include "Adafruit_MAX31855.h"

// Default connection is using software SPI, but comment and uncomment one of
// the two examples below to switch between software SPI and hardware SPI:

// Example creating a thermocouple instance with software SPI on any three
// digital IO pins.

#define TC_DO   48
#define TC_CLK  49
#define TC_1_CS 37
#define TC_2_CS 35
#define TC_3_CS 33

// initialize the Thermocouple
Adafruit_MAX31855 TC1(TC_CLK, TC_1_CS, TC_DO);
Adafruit_MAX31855 TC2(TC_CLK, TC_2_CS, TC_DO);
Adafruit_MAX31855 TC3(TC_CLK, TC_3_CS, TC_DO);

// Example creating a thermocouple instance with hardware SPI
// on a given CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS);

// Example creating a thermocouple instance with hardware SPI
// on SPI1 using specified CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS, SPI1);

void setup() {
  Serial.begin(9600);

  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc

  Serial.println("MAX31855 test");
  // wait for MAX chip to stabilize
  delay(500);
  Serial.print("Initializing sensors...");
  if (!TC1.begin()) {
    Serial.println("ERROR. TC1 did not start.");
    while (1) delay(10);
  }
  if (!TC2.begin()) {
    Serial.println("ERROR. TC2 did not start.");
    while (1) delay(10);
  }
  if (!TC3.begin()) {
    Serial.println("ERROR. TC3 did not start.");
    while (1) delay(10);
  }
  Serial.println("DONE.");
}

void loop() {

  Serial.print("TC1 IT = ");
  Serial.println(TC1.readInternal());
  Serial.print("TC2 IT = ");
  Serial.println(TC2.readInternal());
  Serial.print("TC3 IT = ");
  Serial.println(TC3.readInternal());

  double c = TC1.readCelsius();
  if (isnan(c)) {
    Serial.println("ERROR. TC1 NaN.");
  } else {
    Serial.print("TC1 ET = ");
    Serial.println(c);
  }
  c = TC2.readCelsius();
  if (isnan(c)) {
    Serial.println("ERROR. TC2 NaN.");
  } else {
    Serial.print("TC2 ET = ");
    Serial.println(c);
  }
  c = TC3.readCelsius();
  if (isnan(c)) {
    Serial.println("ERROR. TC3 NaN.");
  } else {
    Serial.print("TC3 ET = ");
    Serial.println(c);
  }
  
  delay(5000);
}
