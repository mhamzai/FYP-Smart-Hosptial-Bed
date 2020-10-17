/*************************************************** 
  This is a library example for the MLX90614 Temp Sensor
Original Library and code source: https://github.com/adafruit/Adafruit-MLX90614-Library

 The code has been updated. I have added two funcitons. Also the Kelivin
 value added into the C and F units.
 1-First function to print the temperature on Serial Monitor
 2-2nd Funciton return the temperature so it can be used for Display or other purpose
 
   Want to get full explanation of this code
  and need wiring diagram? 
  Purchase My Arduino course on Udemy.com http://robojax.com/L/?id=62
 * 
 * Watch video instructions for this code: https://youtu.be/cFDSqiEIunw
updated/written by Ahmad Shamshiri on Mar 30, 2020 at 21:51 
 
 * in Ajax, Ontario, Canada. www.robojax.com
 * 

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
char *typeName[]={"Object","Ambient"};

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);

  Serial.println("Robojax MLX90614 test");  

  mlx.begin();  
}

void loop() {
  //Robojax Example for MLX90614
  printTemp('C');
  printTemp('D');
  
  printTemp('F');  
  printTemp('G'); 
  if( getTemp('C')>40)
  {
    //do something here
  }
  
  printTemp('K');   
  printTemp('L');  
  Serial.println("======");

  delay(3000);
  //Robojax Example for MLX90614
}

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
    float tempObjec = mlx.readObjectTempC();//in C object
    float tempAmbient = mlx.readAmbientTempC();
   if(type =='F')
   {
    value = mlx.readObjectTempF(); //Fah. Object
   }else if(type =='G')
   {
    value = mlx.readAmbientTempF();//Fah Ambient
   }else if(type =='K')
   {
    value = tempObjec + 273.15;// Object Kelvin
   }else if(type =='L')
   {
    value = tempAmbient + 273.15;//Ambient Kelvin
   }else if(type =='C')
   {
    value = tempObjec;
   }else if(type =='D')
   {
    value = tempAmbient;
   }
   return value;
    // Robojax.com MLX90614 Code
}//getTemp

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
  // Robojax.com MLX90614 Code
  float tmp =getTemp(type);

  if(type =='C')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");    
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("C");
  }else if(type =='D')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("C");
  }else if(type =='F')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("F");
  }else if(type =='G')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("F");
  }

  else if(type =='K')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);  
    Serial.print("°");       
    Serial.println(" K");
  }  
  else if(type =='L')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);  
    Serial.print("°");       
    Serial.println(" K");
  }

// Robojax.com MLX90614 Code
}//printTemp(char type)

 
