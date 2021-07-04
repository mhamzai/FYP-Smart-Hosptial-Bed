#include "Arduino.h"

#include <Wire_slave.h>
#include <HX711_ADC.h>
#include <EEPROM.h>
#include <TimeLib.h>

#define CHANGE_THRESH 3
#define HX711_dout PB7 //mcu > HX711 dout pin
#define HX711_sck PB6  //mcu > HX711 sck pin

time_t set; //a variable to get the current time using now()

int bag = 0;             //bag=0 means no bag,bag=1 means a bag is hanging,bag=2 means the bag was hanging but has been removed
bool print_info = false; //a variable to ensure that the same message is not printed unnecessarily
bool is_patient = true;  //represents the presence of patient on the bed
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
long t;

int iter = 0;
bool global_is_change = false;                //
float current, previous = 0, global_previous; //global_previous keeps track of the initial value of a change continuity

String a;

void setup()
{
  float calibrationValue = 445.0; //set the calibration value in the sketch
  long stabilizingtime = 2000;    //preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;           //tare to be performed in the next step

  pinMode(2, OUTPUT); //setting the pin for led on node mcu
  LoadCell.begin();

  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag())
  {
    while (1)
      ;
  }
  else
  {
    LoadCell.setCalFactor(calibrationValue); //set calibration value (float)
  }

  set = now(); //getting the start time
  Serial.begin(9600);
  //.println(second(set)); //printing the start time in seconds

  Wire1.begin(13); // join i2c bus with address #4
  Wire1.onReceive(receiveEvent);
}
int _flag = 0;
bool isReceive = false;
void loop()
{
  bool is_change = false;
  int ret = 0;
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  if (LoadCell.update())
    newDataReady = true;

  if (newDataReady && isReceive)
  {
    if (is_patient == true && millis() > t + serialPrintInterval)
    {
      current = LoadCell.getData();
      if (iter == 0) //storing the first reading of the load cell as the previous reading
      {
        previous = current;
        iter = iter + 1;
      }

      if (abs(previous - current) > CHANGE_THRESH) //if the difference between the current and the previous reading crosses 3g, we detect a change. We chose 3g to eliminate minor fluctuations
      {
        if (bag == 0)
        {
          bag = 1;
          String a = "";
          a = a + "    First bag";
        }
        if (bag == 2)
        {

          a = "";
          a = a + now() + "    BC";

          bag = 1;
        }

        print_info = false;
        is_change = true;
        if (global_is_change == false)
        {
          global_previous = previous;
        }

        previous = current;   //setting the previous to the current
        set = now();          //getting the time
        digitalWrite(2, LOW); //led is off
      }

      else if ((now()) - (set) > 20 and current >= 40 && !print_info) //if a change in the reading has not been detected in 9 secs, we generate an alert
      {

        _flag = 1;
        a = "";
        a = a + now() + "    PP";

        digitalWrite(2, HIGH); //alert generated through led
        print_info = true;
      }

      else if (current < 40 && bag == 0) //a reading<5 indicates the absence of the bag  ///40 here instead of 5
      {
        a = "A bag needs to be installed";

        _flag = 2;
        print_info = true;
      }

      else if (current < 40 && bag == 1) //bag has been removed
      {

        _flag = 2; //2 for BR, 1 for PP
        a = "";
        a = a + now() + "    BR";

        print_info = true;
        bag = 2;
      }

      if (current > 2040 && bag == 1 && !print_info)
      {

        a = "";
        a = a + now() + "    BF";

        print_info = true;
      }

      newDataReady = 0;
      t = millis();

      if (is_change == false && global_is_change == true) //if there is no local change in this loop and previously there was a global change continuity
      {                                                   //this ends the continuity and  logs the change and resets the global change variable

        if (abs(global_previous - current) >= 2) //fluctuations
        {
          _flag = 0;

          a = "";
          a = a + now() + "    LR " + global_previous + "\t" + current;

          global_is_change = false;
        }
      }
      if (is_change == true)
      {
        global_is_change = true;
      }
    }
    WriteCapacity(current);
    isReceive = false;
  }

  delay(42);
}

void WriteCapacity(float curr)
{
  if (_flag == 0)
  {
    if (curr / 20.4 < 0)
    {
      Serial.println(0);
    }
    else if (curr / 20.4 <= 100)
    {
      Serial.println(int(curr / 20.4));
    }
    else
    {
      Serial.println(100);
    }
  }

  else if (_flag == 1)
  {
    Serial.println("PP");
  }
  else if (_flag == 2)
  {
    Serial.println(-1);
  }
}

void SetReceive(int a) { isReceive = true; }
void receiveEvent(int a)
{

  uint8_t values[24];
  int i = 0;
  int total = 0;
  if ((char)Wire1.read() != '<')
  {
    return;
  }
  while (1 < Wire1.available()) // loop through all but the last
  {
    values[i] = (uint8_t)Wire1.read();
    total = total + values[i];
    i++;
  }

  /*for (int j = 0; j < 24; j++)
  {
    Serial.print(values[j]);
  }
  Serial.print(" ");
  Serial.print(total);
 Serial.println();
  */
  if ((char)Wire1.read() != '>' || i != 24)
  {
    return;
  }
  if (total > 3)
  {
    isReceive = true;
  }
  return;
}
