#include "Arduino.h"
#include "SPIFFS.h"
#include "FS.h"
#include <HX711_ADC.h>
#include <EEPROM.h>
#include <TimeLib.h>

//Variables
const int HX711_dout = 21;               //mcu > HX711 dout pin
const int HX711_sck = 22;               //mcu > HX711 sck pin
time_t set;   
File testFile;



//a variable to get the current time using now()
int bag=0;                            //bag=0 means no bag,bag=1 means a bag is hanging,bag=2 means the bag was hanging but has been removed
int print_info=0;                     //a variable to ensure that the same message is not printed unnecessarily  
bool is_patient=true; //represents the presenceof patient on the bed
//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
long t;

void setup()
{
  Serial.begin(57600); 
  delay(10);
  set = now(); //getting the start time
  
  pinMode(2,OUTPUT);                       //setting the pin for led on node mcu
  Serial.println(second(set));             //printing the start time in seconds
///////////////////////////////
  Serial.println("Inizializing FS...");
    if (SPIFFS.begin(true)){
        Serial.println(F("done."));
    }else{
        Serial.println(F("fail."));
    }
////////////////////////////////

  LoadCell.begin();
  float calibrationValue;                   
  calibrationValue = 445.0;                //set the calibration value in the sketch
#if defined(ESP8266)|| defined(ESP32)
  //EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  EEPROM.get(calVal_eepromAdress, calibrationValue);             //fetch the calibration value from eeprom

  long stabilizingtime = 2000;                          // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;                                //tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) 
  {
    while (1);
  }
  else 
  {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
  }


  //testFile = SPIFFS.open(F("/testCreate.txt"), "w");
}

float previous=0;
int iter=0;
bool global_is_change=false;//
float global_previous;//keeps track of the initial value of a change continuity




void loop() 
{ bool is_change=false;
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0;                        //increase value to slow down serial print activity
  testFile = SPIFFS.open(F("/testCreate.txt"), "a+");
/*Serial.println("*********************************************************");
Serial.println();
Serial.print(now());
Serial.print("\t seconds now:");
Serial.print(second(now()));
Serial.println("*********************************************************");
*/
  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;
  
  // get smoothed value from the dataset:
  if (newDataReady) 
  {
    if (is_patient==true && millis() > t + serialPrintInterval) 
    {
      float i = LoadCell.getData();
      //Serial.print(now());
      //Serial.print("  LD");                 //load cell initial reading
      if(iter==0)                           //storing the first reading of the load cell as the previous reading 
      {
        previous=i; 
        iter=iter+1;
      }

      
      if(abs(previous-i)>3)                //if the difference between the current and the previous reading crosses 3g, we detect a change. We chose 3g to eliminate minor fluctuations 
      { 
        if (bag==0)                        
        {
          bag=1;
          Serial.println("First bag has been installed!");
                if (testFile){
        testFile.println("    First bag");
 
        
    }else{
        Serial.println("Problem on create file!");
    }
        }
        if (bag==2)
        {
         //Serial.println("New bag has been installed!");
         Serial.print(now());
         Serial.print("  BC");             //bag is changed
         Serial.println();
         if (testFile){
        testFile.print(now());
        testFile.println("    BC");
 
        
    }else{
        Serial.println("Problem on create file!");
    }
         bag=1;
        }
        
        print_info=0;
        is_change=true;
        if(global_is_change==false)
        {global_previous=previous;}

        previous=i;                  //setting the previous to the current 
        set=now();                   //getting the time
        digitalWrite(2,LOW);          //led is off
      }
//second(now())-second(set)
      else if((now())-(set)>9 and i>=5 && !print_info)      //if a change in the reading has not been detected in 9 secs, we generate an alert
      { 
        Serial.println();
        Serial.print(now());
        
        Serial.print("  PP");                                //patient not peeing 
        Serial.println();
        if (testFile){
        testFile.print(now());
        testFile.println("    PP");
 
        
    }else{
        Serial.println("Problem on create file!");
    }
        digitalWrite(2,HIGH);                                //alert generated through led
        print_info=1;
      }
      
      else if(i<5 && bag==0 && !print_info)                 //a reading<5 indicates the absence of the bag
      {
        Serial.println("A bag needs to be installed"); 
        if (testFile){
        testFile.println("A bag needs to be installed");
 
        
    }else{
        Serial.println("Problem on create file!");
    }
        print_info=1; 
      }
      
      else if(i<5 && bag==1 && !print_info)               //bag has been removed
      {
        Serial.println();
        Serial.print(now());
        Serial.print("  BR");                        //bag is removed
        Serial.println();
        if (testFile){
        testFile.print(now());
        testFile.println("    BR");
 
        
    }else{
        Serial.println("Problem on create file!");
    }
        print_info=1;
        bag=2;
      }

      if(i>500 && bag==1 && !print_info)
      {
        Serial.println();
        Serial.print(now());
        Serial.print("  BF");                            //bag is full
        Serial.println(); 
        if (testFile){
        testFile.print(now());
        testFile.println("    BF");
 
        
    }else{
        Serial.println("Problem on create file!");
    }  
        print_info=1;
      } 
      
      newDataReady = 0;
      t = millis();
  //////////////////////////////////////
    if(is_change==false && global_is_change==true) // if there is no local change in this loop and previously there was a global change continouty
  { // this ends the continuity and  logs the change and resets the global change variable
    Serial.print(now());
    Serial.print("  ");
    Serial.print("LR   ");
    Serial.print(global_previous);
    Serial.print("\t");
    Serial.println(i);
    if (testFile){
        //Serial.println("Write file content!");
        testFile.print(now());
        testFile.print("    LR   ");
        testFile.print(global_previous);
        testFile.print("\t");
        testFile.println(i);
 
        
    }else{
        Serial.println("Problem on create file!");
    }
    global_is_change=false;
    }
  if(is_change==true) {
    global_is_change=true;
    }
  
    
    testFile.close();
    /////////////////////////////////////
    }
  
  }

  // receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0) {
    float i;
    char inByte = Serial.read();
    if (inByte == 't') {LoadCell.tareNoDelay();}
  }
    

}
