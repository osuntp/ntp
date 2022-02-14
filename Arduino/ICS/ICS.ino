#include <SPI.h>
#include <Servo.h>

Servo massFlowValve;

const byte numChars = 32;
char receivedChars[numChars];
char prefix[numChars];
char message[numChars];
boolean newMessageIsAvailable = false;

int heater_pin = 52;

void setup()
{

  // Setup serial connection
  Serial.begin(9600);
  while (!Serial) delay(1);

  Serial.println("<TSC>");

  massFlowValve.attach(9);

  pinMode(heater_pin,OUTPUT);
}

void loop()
{
  CheckSerialForMessage();

  if (newMessageIsAvailable)
  {
    HandleNewMessage();
  } 
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
      if (rc != endMarker)
      {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars)
        {
          ndx = numChars - 1;
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

  if (strcmp(prefix, "stdin") == 0)
  {
    strtokIndx = strtok(NULL, ", ");
    strcpy(prefix, strtokIndx);

    if (strcmp(prefix, "valve") == 0)
    {
      strtokIndx = strtok(NULL, ", ");
      float valvePosition;
      valvePosition = atof(strtokIndx);

      valvePosition = map(valvePosition,0,90,27,90);
      valvePosition = round(valvePosition);

      massFlowValve.write(valvePosition);
      delay(15);
      
      Serial.print("<stdinfo, TSC set the Valve Position to ");
      Serial.print(valvePosition);
      Serial.println(">");
    }

    if (strcmp(prefix, "heater") == 0)
    {
      strtokIndx = strtok(NULL, ", ");
      //char heaterState;
      //heaterState = atof(strtokIndx);

      if (strcmp(strtokIndx, "on") == 0)
      {
        digitalWrite(heater_pin,HIGH);
        delay(15);
        Serial.println("<stdinfo, ICS set heater ON>");
      }
      
      if (strcmp(strtokIndx, "off") == 0)
      {
        digitalWrite(heater_pin,LOW);
        delay(15);
        Serial.println("<stdinfo, ICS set heater OFF>");
      }
    }
  }
  
  newMessageIsAvailable = false;
}
