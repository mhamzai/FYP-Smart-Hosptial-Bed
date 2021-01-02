#include <Wire.h>
#include <Adafruit_MLX90614.h>
const int pingPin = 11; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 10; // Echo Pin of Ultrasonic Sensor

#define MAX_WORD_COUNT 12
char *Words[MAX_WORD_COUNT];
float values[MAX_WORD_COUNT];
char *typeName[] = {"Object", "Ambient", "Calculated Object Celsius", "Calculated Object Fahrenheit"};
double microsecondsToCentimeters(long microseconds);
float patientArea = -1;
float prev_val = 0;
double area = 0;
String serialRead = "";
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);
  pinMode(8, INPUT);
  pinMode(9, OUTPUT);
  pinMode(pingPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(9, HIGH);
  Serial.println("Robojax MLX90614 test");
  Wire.begin(9);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  mlx.begin();
}

void loop() {
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  // Sets the pingPin on HIGH state for 10 micro seconds
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  float duration = pulseIn(echoPin, HIGH);
  double cm = microsecondsToCentimeters(duration);
  double meters = cm / 100;
  area = 3.14159265358979 * (meters * meters);
  Serial.print("Sensor Area is : ");
  Serial.println(area);
  patientArea = bodyArea();
  if (patientArea == -1)
  {
    Serial.println("no patient area");
    delay(1000);
    //return;
  }
  else 
  {Serial.print("patient area = ");
    Serial.println(patientArea);  
  }
  printTemp('C');
  printTemp('D');

  printTemp('F');
  printTemp('G');
  printTemp('R');
  printTemp('S');
  if ( getTemp('C') > 40)
  {
    //do something here
  }

  printTemp('K');
  printTemp('L');
  Serial.println("======");

  delay(5000);
  //Robojax Example for MLX90614
}

/*
   @brief returns temperature or relative humidity
   @param "type" is character
       C = Object Celsius
       D = Ambient Celsius

       K = Object Keliven
       L = Ambient in Keilven

       F = Object Fahrenheit
       G = Ambient in Fahrenheit

   @return returns one of the values above
   Usage: to get Fahrenheit type: getTemp('F')
   to print it on serial monitor Serial.println(getTemp('F'));
   Written by Ahmad Shamshiri on Mar 30, 2020.
   in Ajax, Ontario, Canada
   www.Robojax.com
*/
float getTemp(char type)
{
  // Robojax.com MLX90614 Code
  float value;
  float ratio = patientArea / area;
  float tempObjec = mlx.readObjectTempC();//in C object
  float tempAmbient = mlx.readAmbientTempC();
  //float areaCone = 1.419; // in meteres
  float bodyTemp;
  if (digitalRead(8))
  {
    bodyTemp = ((tempObjec) - ((1 - ratio) * (prev_val))) / (ratio);
  }
  else
  {
    bodyTemp = tempObjec;
  }
  float bodyTempF = ((mlx.readObjectTempF()) - ((1 - ratio) * (mlx.readAmbientTempF()))) / (ratio);

  if (type == 'F')
  {
    value = mlx.readObjectTempF(); //Fah. Object
  } else if (type == 'G')
  {
    value = mlx.readAmbientTempF();//Fah Ambient
  } else if (type == 'K')
  {
    value = tempObjec + 273.15;// Object Kelvin
  } else if (type == 'L')
  {
    value = tempAmbient + 273.15;//Ambient Kelvin
  } else if (type == 'C')
  {
    value = tempObjec;
  } else if (type == 'D')
  {
    value = tempAmbient;
  }
  else if (type == 'R') // Calculated object temperature in Celsius
  {
    value = bodyTemp;
  }
  else if (type == 'S') // Calculated object temperature in Fahrenheit
  {
    value = bodyTempF;
  }

  if (!digitalRead(8))
  {
    prev_val = tempObjec;
  }
  return value;
  // Robojax.com MLX90614 Code
}//getTemp

/*
   @brief nothing
   @param "type" is character
       C = Object Celsius
       D = Ambient Celsius

       K = Object Keliven
       L = Ambient in Keilven

       F = Object Fahrenheit
       G = Ambient in Fahrenheit

       R = Calculated Object in Celsius
       S = Calculated Object in Fahrenheit

   @return prints temperature value in serial monitor
   Usage: to get Fahrenheit type: getTemp('F')
   to print it on serial monitor Serial.println(getTemp('F'));
   Written by Ahmad Shamshiri on Mar 30, 2020 at 21:51
   in Ajax, Ontario, Canada
   www.Robojax.com
*/
void printTemp(char type)
{
  // Robojax.com MLX90614 Code
  float tmp = getTemp(type);

  if (type == 'C')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("C");
  } else if (type == 'D')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("C");
  } else if (type == 'F')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("F");
  } else if (type == 'G')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("F");
  }

  else if (type == 'K')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println(" K");
  }
  else if (type == 'L')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println(" K");
  }
  else if (type == 'R')
  {
    Serial.print(typeName[2]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("C");
  }
  else if (type == 'S')
  {
    Serial.print(typeName[3]);
    Serial.print(" ");
    Serial.print(tmp);
    Serial.print("°");
    Serial.println("F");
  }

}

double microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
}

void SendData(double calcBodyTemp)
{
  // send data to machine most probably Raspberry
}

void receiveEvent(int howMany)
{
  //Serial.println("something came here!");
  String i2cData = "";
  if ((char)Wire.read() != '<')
  {serialRead == i2cData;
    return;
  }
  while(1 < Wire.available()) // loop through all but the last
  {
    i2cData += Wire.read();
    i2cData += (char)Wire.read();// receive byte as a character
  }
 /* if ((char)Wire.read() != '>')
  {serialRead = ""; return;} */
  //Serial.print("gen str ==>> ");Serial.println(i2cData);
 serialRead = i2cData;
}

float bodyArea()
{
  float areaCal = -1;
  if (serialRead != "") //verify if string is starting with telda i.e no data loss from start
  {
      char charRead[500];
      serialRead.toCharArray(charRead,serialRead.length());
      Serial.println(serialRead);
      split_message(charRead);
  }
  else
  {
    return patientArea;
  }
  areaCal = 0;
  for (int i = 0; i < 6; i++)
  {
    if (values[i] > 60)
    { areaCal += 1;
    }
    else if (values[i] > 30)
    {
      areaCal += 0.5;
    }
  }
  if (areaCal == 0){return -1;}
  areaCal = areaCal / 6;
  areaCal = areaCal * area;
  return areaCal;
}

int split_message(char* str) {
  int word_count = 0; //number of words
  char * item = strtok (str, ","); //getting first word (uses comma as delimeter)

  while (item != NULL) {
    Words[word_count] = item;
    item = strtok (NULL, ","); //getting subsequence word
    word_count++;
  }
  for (int i = 0; i < 12; i++)
  {
    values[i] = atof(Words[i]);
  }
  return  word_count;
}
