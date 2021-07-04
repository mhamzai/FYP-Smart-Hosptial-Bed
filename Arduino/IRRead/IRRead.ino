//#include <Wire.h>
//#include <Servo.h>
//#include <Adafruit_MLX90614.h>
//#define servoPin A7
//
//
//Adafruit_MLX90614 mlx = Adafruit_MLX90614();
//Servo servo;
//int rot = 60;
//
//
//void setup() {
//  Serial.begin(9600);
//  servo.attach(servoPin);
//  mlx.begin();
//}
//
//void loop() {
//
//  if (rot < 30)
//    rot = 60;
//
//  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC());
//  Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");
//  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempF());
//  Serial.print("*F\tObject = "); Serial.print(mlx.readObjectTempF()); Serial.println("*F");
//
//  Serial.println();
//
//  delay(1000);
//  servo.write(rot);
//  delay(1000);
//
//
//  rot -= 10;
//
//}

/*************************************************** 
  This is a library example for the MLX90614 Temp Sensor
Original Library and code source: https://github.com/adafruit/Adafruit-MLX90614-Library

 this code has been mostly updated
 it displays the temperature on Serial1602 or LCD2004 in C, F and K for object and for ambient
 
   Want to get full explanation of this code
  and need wiring diagram? 
  Purchase My Arduino course on Udemy.com http://robojax.com/L/?id=62
 * 
 * Watch video instructions for this code:  https://youtu.be/_iO2L4P_irw
updated/written by Ahmad Shamshiri on Jun 28, 2020 
 
 * in Ajax, Ontario, Canada. www.robojax.com

Introduction to MLX90614 Infrared Temperature Sensor: https://youtu.be/cFDSqiEIunw

 * Get this code and other Arduino codes from Robojax.com
Learn Arduino step by step in structured course with all material, wiring diagram and library
all in once place. Purchase My course on Udemy.com http://robojax.com/L/?id=62

If you found this tutorial helpful, please support me so I can continue creating 
content like this. You can support me on Patreon http://robojax.com/L/?id=63

or make donation using PayPal http://robojax.com/L/?id=64

 *  * This code is "AS IS" without warranty or liability. Free to be used as long as you keep this note intact.* 
 * This code has been download from Robojax.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Origin
  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Servo.h>

char *typeName[] = {"Object:", "Ambient:"};

#define servoPin PB12
Servo servo;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
String toSend2;

void setup()
{
  Serial.begin(9600);
  servo.attach(servoPin);

  if (!mlx.begin()) //Begin returns 0 on a good init
  {

    while (1)
      ;
  }
  Wire.begin();

} //setup() end

void loop()
{

  float tempObjec;
  String toSend = "";
  float ambTemp;
  bool inPat = false;

  if (Serial.read() == '1')
  { // with patient

    ambTemp = mlx.readAmbientTempF();
    toSend += String(ambTemp);
    toSend += ",";

    for (int i = 60; i >= 50; i--)
    { // 60 degrees correspond to zero degrees
      servo.write(i);
      if (i % 5 == 0)
      {
        tempObjec = mlx.readObjectTempF();
        toSend += String(tempObjec);
        if (i == 50)
          toSend += "\n";
        else
          toSend += ",";
      }

      delay(100);
    }

    inPat = true;
  }

  else
  { // without patient
    servo.write(60);
    tempObjec = mlx.readObjectTempF();
    toSend += String(tempObjec);
    toSend += "\n";
  }

  Serial.print(toSend);

  delay(50);

  if (inPat)
  { // if the motor is not at zero degrees
    for (int i = 50; i <= 60; i++)
    {
      servo.write(i);
      delay(100);
    }
  }
}

//Serial.print(toSend);
//delay(50);

//Robojax Example for MLX90614 with LCD
//printTemp('C');//object temperature in C
//float tempObjec = mlx.readObjectTempC();//in C object
//float tempAmbient = mlx.readAmbientTempC();
//Serial.print("Ambient: ");
//Serial.print(tempAmbient);
//Serial.print("C           Object: ");//
//Serial.print(tempObjec);
//Serial.print("\n");
//delay(2000);

//printTemp('D');//ambient temperature in C
//delay(2000);
//
//  printTemp('F'); //object temperature in F
//  delay(2000);
//
//  printTemp('G'); //ambient temperature in F
//  delay(2000);
//  if( getTemp('C')>40)
//  {
//    //do something here
//  }
//
//  printTemp('K'); //object temperature in K
//  delay(2000);
//  printTemp('L');//ambient temperature in K
//  delay(2000);

//Robojax Example for MLX90614

/*
 * @brief returns temperature or relative humidity
 * @param "type" is character
 *     C = Object Celsius
 *     D = Ambient Celsius
 *     
 *     K = Object Keliven
 *     L = Ambient in Keilven
 *     
 *     F = Object Fahrenheit
 *     G = Ambient in Fahrenheit

 * @return returns one of the values above
 * Usage: to get Fahrenheit type: getTemp('F')
 * to print it on serial monitor Serial.println(getTemp('F'));
 * Written by Ahmad Shamshiri on Mar 30, 2020. 
 * in Ajax, Ontario, Canada
 * www.Robojax.com 
 */
float getTemp(char type)
{
  // Robojax.com MLX90614 Code
  float value;
  float tempObjec = mlx.readObjectTempC(); //in C object
  float tempAmbient = mlx.readAmbientTempC();
  if (type == 'F')
  {
    value = mlx.readObjectTempF(); //Fah. Object
  }
  else if (type == 'G')
  {
    value = mlx.readAmbientTempF(); //Fah Ambient
  }
  else if (type == 'K')
  {
    value = tempObjec + 273.15; // Object Kelvin
  }
  else if (type == 'L')
  {
    value = tempAmbient + 273.15; //Ambient Kelvin
  }
  else if (type == 'C')
  {
    value = tempObjec;
  }
  else if (type == 'D')
  {
    value = tempAmbient;
  }
  return value;
  // Robojax.com MLX90614 Code
} //getTemp

/*
 * @brief nothing
 * @param "type" is character
 *     C = Object Celsius
 *     D = Ambient Celsius
 *     
 *     K = Object Keliven
 *     L = Ambient in Keilven
 *     
 *     F = Object Fahrenheit
 *     G = Ambient in Fahrenheit

 * @return prints temperature value in serial monitor
 * Usage: to get Fahrenheit type: getTemp('F')
 * to print it on serial monitor Serial.println(getTemp('F'));
 * Written by Ahmad Shamshiri on Mar 30, 2020 at 21:51
 * in Ajax, Ontario, Canada
 * www.Robojax.com 
 */
void printTemp(char type)
{
  //clearCharacters(1,0, Serial_CHAR-1 );
  // Robojax.com MLX90614 Code
  float tmp = getTemp(type);

  if (type == 'C')
  {

    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("C");
  }
  else if (type == 'D')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("C");
  }
  else if (type == 'F')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("F");
  }
  else if (type == 'G')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("F");
  }

  else if (type == 'K')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("K");
  }
  else if (type == 'L')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print((char)223); //
    Serial.print("K");
  }

  // Robojax.com MLX90614 Code
} //printTemp(char type)
