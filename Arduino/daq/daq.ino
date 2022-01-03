#include "sfm3019.h"
#include <SPI.h>
#include "Adafruit_MAX31855.h"

// Define hardware SPI
#define TC_DO   48
#define TC_CLK  49
#define TC_1_CS 37
#define TC_2_CS 35
#define TC_3_CS 33

// Initialize thermocouples
Adafruit_MAX31855 TC1(TC_CLK, TC_1_CS, TC_DO);
Adafruit_MAX31855 TC2(TC_CLK, TC_2_CS, TC_DO);
Adafruit_MAX31855 TC3(TC_CLK, TC_3_CS, TC_DO);

// Initialize mass flow meter
int error = 0;
SfmConfig sfm3019;

int inletPressurePin = A2;
int tankPressurePin = A1;

int pressureValue = 0;
float inletPressurePSI= 0;
float tankPressurePSI = 0;

void setup() {
  Serial.begin(9600);

  while (!Serial) delay(1);

  Serial.println("<DAQ>");
  
  // Setup mass flow meter
  const char* driver_version = sfm_common_get_driver_version();
  if (driver_version) {
    Serial.print("<stdinfo,SFM Driver Version: ");
    Serial.print(driver_version);
    Serial.println(">");
  } else {
    Serial.println("<stderr,Could not get SFM driver version>");
  }

  sensirion_i2c_init();


  /* Reset all I2C devices */
//    Serial.println("hit1");
  error = sensirion_i2c_general_call_reset();
  if (error) {
    Serial.println("<stderr,SFM general call reset failed>");
  }
//  Serial.println("hitt2");
  /* Wait for the SFM3019 to initialize */
  sensirion_sleep_usec(SFM3019_SOFT_RESET_TIME_US);
//  Serial.println("hit3");
  while (sfm3019_probe()) {
    Serial.println("<stderr,SFM sensor probing failed>");
    sensirion_sleep_usec(100000);
  }
//  Serial.println("hit4");
  uint32_t product_number = 0;
  uint8_t serial_number[8] = {};
  error = sfm_common_read_product_identifier(SFM3019_I2C_ADDRESS,
          &product_number, &serial_number);
//    Serial.println("hit5");
  if (error) {
    Serial.println("<stderr,SFM failed to read product identifier>");
  } else {
    Serial.print("<stdinfo,SFM product: 0x");
    Serial.print(product_number, HEX);
    Serial.print(" serial: 0x");
    for (size_t i = 0; i < 8; ++i) {
      Serial.print(serial_number[i], HEX);
    }
    Serial.println(">");
  }
//    Serial.println("hit6s");

  sfm3019 = sfm3019_create();

  error = sfm_common_start_continuous_measurement(
            &sfm3019, SFM3019_CMD_START_CONTINUOUS_MEASUREMENT_AIR);

  if (error) {
    Serial.println("<stderro,SFM failed to start measurement>");
  }

  /* Wait for the first measurement to be available. Wait for
     SFM3019_MEASUREMENT_WARM_UP_TIME_US instead for more reliable results */
  sensirion_sleep_usec(SFM3019_MEASUREMENT_INITIALIZATION_TIME_US);

  // Setup thermocouples
//  Serial.println("<stdinfo,Initializing thermocouples>");
//  if (!TC1.begin()) {
//    Serial.println("<stderr,TC1 did not start>");
//    while (1) delay(10);
//  }
//  if (!TC2.begin()) {
//    Serial.println("<stderr,TC2 did not start>");
//    while (1) delay(10);
//  }
//  if (!TC3.begin()) {
//    Serial.println("<stderr,TC3 did not start>");
//    while (1) delay(10);
//  }
//  Serial.println("<stdinfo,Thermocouples initialized>");
  
}

void loop() {
  // Call setup again if there were errors
  if (error) {
    Serial.println("<stderr,SFM error: redoing setup>");
    sensirion_sleep_usec(100000);
    error = 0;
    setup();
  }

  int16_t flow_raw;
  int16_t temperature_raw;
  uint16_t status;
  error = sfm_common_read_measurement_raw(&sfm3019, &flow_raw, &temperature_raw, &status);

  float flow;
  float flow_temperature;
  if (error) {
    Serial.println("<stderr,SFM error while reading measurement>");
    return;
  } else {

    error = sfm_common_convert_flow_float(&sfm3019, flow_raw, &flow);
    if (error) {
      Serial.println("<stderr,SFM error while converting flow>");
      return;
    }
    flow_temperature = sfm_common_convert_temperature_float(temperature_raw);
    
    Serial.print("<stdinfo, SFM status: ");
    Serial.print(status, HEX);
    Serial.println(">");
//
  }

double c1 = 0;
double c2 = 0;
double c3 = 0;

double it1 = 0;
double it2 = 0;
double it3 = 0;

//  // Read thermocouples
//  double c1 = TC1.readCelsius();
//  double c2 = TC2.readCelsius();
//  double c3 = TC3.readCelsius();
//  if (isnan(c1)) {
//    Serial.println("<stderr,TC1 NaN>");
//  }
//  if (isnan(c2)) {
//    Serial.println("<stderr,TC2 NaN>");
//  }
//  if (isnan(c3)) {
//    Serial.println("<stderr,TC3 NaN>");
//  }
//  double it1 = TC1.readInternal();
//  double it2 = TC2.readInternal();
//  double it3 = TC3.readInternal();

  pressureValue = analogRead(inletPressurePin);
  float pressureValueFloat = (float)pressureValue;

  inletPressurePSI = (pressureValueFloat / 1024)*100;
  
  pressureValue = analogRead(tankPressurePin);
  pressureValueFloat = (float)pressureValue;
  
  tankPressurePSI = (((pressureValueFloat/ 1024)*5)-1) *(200/4);
  
  float heater_current = 0;
  float heater_temp = 0;
  float heater_it = 0;
  float mid_press = 0;
  float outlet_press = 0;
  
  // Send data stream
  Serial.print("<stdout, ");
  Serial.print(flow);
  Serial.print(", ");
  Serial.print(flow_temperature);
  Serial.print(", ");
  Serial.print(heater_current);
  Serial.print(", ");
  Serial.print(heater_temp);
  Serial.print(", ");
  Serial.print(heater_it);
  Serial.print(", ");
  Serial.print(c1);
  Serial.print(", ");
  Serial.print(it1);
  Serial.print(", ");
  Serial.print(c2);
  Serial.print(", ");
  Serial.print(it2);
  Serial.print(", ");
  Serial.print(c3);
  Serial.print(", ");
  Serial.print(it3);
  Serial.print(", ");
  Serial.print(tankPressurePSI, 7);
  Serial.print(", ");
  Serial.print(inletPressurePSI, 7);
  Serial.print(", ");
  Serial.print(mid_press);
  Serial.print(", ");
  Serial.print(outlet_press);
  Serial.println(">");

  delay(250);
}
