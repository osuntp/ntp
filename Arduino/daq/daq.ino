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

int pressurePin = A0;
int pressureValue = 0;
float pressurePSI= 0;

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
  error = sensirion_i2c_general_call_reset();
  if (error) {
    Serial.println("<stderr,SFM general call reset failed>");
  }

  /* Wait for the SFM3019 to initialize */
  sensirion_sleep_usec(SFM3019_SOFT_RESET_TIME_US);

  while (sfm3019_probe()) {
    Serial.println("<stderr,SFM sensor probing failed>");
    sensirion_sleep_usec(100000);
  }

  uint32_t product_number = 0;
  uint8_t serial_number[8] = {};
  error = sfm_common_read_product_identifier(SFM3019_I2C_ADDRESS,
          &product_number, &serial_number);
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
    sensirion_sleep_usec(100000);
    error = 0;
    setup();
  }

  int16_t flow_raw;
  int16_t temperature_raw;
  uint16_t status;
  error = sfm_common_read_measurement_raw(&sfm3019, &flow_raw,&temperature_raw, &status);

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

  pressureValue = analogRead(pressurePin);

  float pressureValueFloat = (float)pressureValue;
  
  pressurePSI = (pressureValueFloat / 1024)*100;
  

  //String stringPressurePSI = String(pressurePSI, 6);
  
  // Send data stream
  Serial.print("<stdout, ");
  Serial.print(flow);
  Serial.print(", ");
  Serial.print(flow_temperature);
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
  Serial.print(pressurePSI, 7);
  Serial.println(">");

  delay(1000);
}
