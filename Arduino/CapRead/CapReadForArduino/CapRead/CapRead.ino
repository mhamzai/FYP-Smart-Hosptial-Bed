/*********************************************************
This is a library for the MPR121 12-channel Capacitive touch sensor

Designed specifically to work with the MPR121 Breakout in the Adafruit shop 
  ----> https://www.adafruit.com/products/

These sensors use I2C communicate, at least 2 pins are required 
to interface

Adafruit invests time and resources providing this open source code, 
please support Adafruit and open-source hardware by purchasing 
products from Adafruit!

Written by Limor Fried/Ladyada for Adafruit Industries.  
BSD license, all text above must be included in any redistribution
**********************************************************/

#include <Wire.h>
#include "Adafruit_MPR121.h"

// You can have up to 4 on one i2c bus but one is enough for testing!
//Adafruit_MPR121_STM32 cap = Adafruit_MPR121_STM32();
Adafruit_MPR121 cap = Adafruit_MPR121();

void setup() {

  while (!Serial);        // needed to keep leonardo/micro from starting too fast!

  Serial.begin(9600);
  Serial.println("Adafruit MPR121 Capacitive Touch sensor test"); 
  
  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  Serial.println("MPR121 found!");
}

void loop() {
    
  // debugging info, what
  //Serial.print("\t\t\t\t\t\t\t\t\t\t\t\t\t 0x"); Serial.println(cap.touched(), HEX);
  //Serial.print("Filt: ");
  for (uint8_t i=0; i<12; i++) {
    //Serial.print(i+1); to be added if author doesn't conforms to standards
    Serial.print(cap.filteredData(i));
    //Serial.print(" (");
    double C = calCap(cap.filteredData(i)); 
    //Serial.print(C, 5) ;
    //Serial.print("pF ");
    //Serial.print(calDistance(C), 5);
    Serial.print("\t");
  }
  Serial.println();
  /*Serial.print("Base: ");
  for (uint8_t i=0; i<12; i++) {
    Serial.print(cap.baselineData(i));
    //Serial.print(" (");
    double C = calCap(cap.baselineData(i)); 
    //Serial.print(C, 5) ;
    //Serial.print("pF ");
    //Serial.print(calDistance(C), 5);
    Serial.print(")\t");
  }
  Serial.println();
*/
  
  // put a delay so it isn't overwhelming
  delay(100);
}


double calCap(int pinVal)
{
  double I = 32.0;//0.000016;
  double T = 8.0; //0.0000005;
  double Vdd = 5.0;
  double V = (pinVal * Vdd)/1024;
  //double V = (0.001855 * double(pinVal)) + 0.7;    // for 3.3V
  //double V = (0.003515625 * double(pinVal)) + 0.7;   // for 5V
  //Serial.print(V, 5);
  //Serial.print("V ");

  //double cap = double(I*T)/ double(V);
  double cap = (I*T*1024) / (pinVal*Vdd);

  return cap;
}

double calDistance(double C)
{
  // capacitance is coming in as pF
  double A = 0.016129;
  double Er = 2*2.73;
  double d = 8.85*Er*(A/C);
  return d;
}
