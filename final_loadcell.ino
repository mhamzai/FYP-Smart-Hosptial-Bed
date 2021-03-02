#include "Arduino.h"
#include "SPIFFS.h"
#include "FS.h"
#include <HX711_ADC.h>
#include <EEPROM.h>
#include <TimeLib.h>

#define CHANGE_THRESH 3
#define HX711_dout 21 //mcu > HX711 dout pin
#define HX711_sck 22  //mcu > HX711 sck pin
//Variables

time_t set; //a variable to get the current time using now()
File testFile;


int bag = 0;                 //bag=0 means no bag,bag=1 means a bag is hanging,bag=2 means the bag was hanging but has been removed
bool print_info = false;     //a variable to ensure that the same message is not printed unnecessarily
bool is_patient = true;      //represents the presence of patient on the bed
//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
long t;


int iter = 0;
bool global_is_change = false; //
float current , previous = 0, global_previous;        // global_previous keeps track of the initial value of a change continuity

String a;

void setup()
{
  //delay(10);
  float calibrationValue = 445.0; //set the calibration value in the sketch
  long stabilizingtime = 2000;    // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;           //tare to be performed in the next step

  pinMode(2, OUTPUT);             //setting the pin for led on node mcu
  LoadCell.begin();
  EEPROM.get(calVal_eepromAdress, calibrationValue); //fetch the calibration value from eeprom


  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag())
  {
    while (1);
  }
  else
  {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
  }

  set = now();                 //getting the start time
  Serial.begin(57600);
  Serial.println(second(set)); //printing the start time in seconds

  Serial.println("Inizializing FS...");
  SPIFFS.begin(true);
  /*{
    break;
      //Serial.println(F("done."));
    }
    else
    {
    Serial.println(F("fail."));
    }
  */
}
void loop()
{
  bool is_change = false;
  //Serial.println("----");
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity
  testFile = SPIFFS.open(F("/testCreate.txt"), "a+");

  // check for new data/start next conversion:

  if (LoadCell.update())
    newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady)
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
          //Serial.println("First bag has been installed!");
          String a = "";
          a = a + "    First bag";
          WriteToFile(a);

        }
        if (bag == 2)
        {
      //Serial.println("New bag has been installed!");
          //Serial.print(now());
          Serial.print("BC"); //bag is changed
          Serial.println();
          WriteCapacity(current);
          a = "";
          a = a + now() + "    BC";
          WriteToFile(a);

          bag = 1;
        }

        print_info = false;
        is_change = true;
        if (global_is_change == false)
        {
          global_previous = previous;
        }

        previous = current;         //setting the previous to the current
        set = now();          //getting the time
        digitalWrite(2, LOW); //led is off
      }

      else if ((now()) - (set) > 9 and current >= 5 && !print_info) //if a change in the reading has not been detected in 9 secs, we generate an alert
      {
        Serial.println();
        //Serial.print(now());

        Serial.println("PP"); //patient not peeing
        WriteCapacity(current);
        a = "";
        a = a + now() + "    PP";
        WriteToFile(a);


        digitalWrite(2, HIGH); //alert generated through led
        print_info = true;
      }

      else if (current < 5 && bag == 0 && !print_info) //a reading<5 indicates the absence of the bag
      {
        //Serial.println("A bag needs to be installed");
        a = "A bag needs to be installed";

        WriteToFile(a);

        print_info = true;
      }

      else if (current < 5 && bag == 1 && !print_info) //bag has been removed
      {
        Serial.println();
        //Serial.print(now());
        Serial.print("BR"); //bag is removed
        Serial.println();
        WriteCapacity(current);

        a = "";
        a = a + now() +  "    BR";
        WriteToFile(a);


        print_info = true;
        bag = 2;
      }

      if (current > 500 && bag == 1 && !print_info)
      {
        Serial.println();
        // Serial.print(now());
        Serial.print("BF"); //bag is full
        Serial.println();
        WriteCapacity(current);

        a = "";
        a = a + now() +  "    BF";
        WriteToFile(a);

        print_info = true;
      }

      newDataReady = 0;
      t = millis();
      //////////////////////////////////////
      if (is_change == false && global_is_change == true) // if there is no local change in this loop and previously there was a global change continouty
      { // this ends the continuity and  logs the change and resets the global change variable

        if (abs(global_previous - current) >= 2) // fluctuations

        {
          // Serial.print(now());
          //Serial.print("  ");
          //Serial.print("LR   ");
          //Serial.print(global_previous);
          //Serial.print("\t");
          WriteCapacity(current);
          //Serial.println(current);

          a = "";
          a = a + now() +  "    LR " + global_previous  + "\t" + current;
          WriteToFile(a);

          global_is_change = false;
        }
      }
      if (is_change == true)
      {
        global_is_change = true;
      }

      testFile.close();
      /////////////////////////////////////
    }
  }
  WriteCapacity(current);
}
void WriteToFile(String s)
{
  if (testFile)
  {
    testFile.println(s);
  }
  else
  {
    Serial.println("Problem on create file!");
  }
}
void WriteCapacity(float curr)
{ Serial.print("<");
  if (curr / 5 < 0)
  {
    Serial.print(0);
  }
  else if (curr / 5 <= 100)
  {
    Serial.print(curr/5);
  }
  else
  {
    Serial.print(100);
  }
  Serial.println(">");
}
