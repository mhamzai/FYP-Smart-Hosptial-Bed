#include <Arduino.h>
#include <include/twi.h>

#define ADDR      0x5A

//EEPROM 32x16
#define TO_MAX    0x00
#define TO_MIN    0x01
#define PWM_CTRL  0x02

//RAM 32x16
#define RAW_IR_1  0x04
#define RAW_IR_2  0x05
#define TA        0x06
#define TOBJ_1    0x07
#define TOBJ_2    0x08

#define SYNC_PIN  2

static const uint32_t TWI_CLOCK = 100000;
static const uint32_t RECV_TIMEOUT = 100000;
static const uint32_t XMIT_TIMEOUT = 100000;

Twi *pTwi = WIRE_INTERFACE;

static void Wire_Init(void) {
  pmc_enable_periph_clk(WIRE_INTERFACE_ID);
  PIO_Configure(
  g_APinDescription[PIN_WIRE_SDA].pPort,
  g_APinDescription[PIN_WIRE_SDA].ulPinType,
  g_APinDescription[PIN_WIRE_SDA].ulPin,
  g_APinDescription[PIN_WIRE_SDA].ulPinConfiguration);
  PIO_Configure(
  g_APinDescription[PIN_WIRE_SCL].pPort,
  g_APinDescription[PIN_WIRE_SCL].ulPinType,
  g_APinDescription[PIN_WIRE_SCL].ulPin,
  g_APinDescription[PIN_WIRE_SCL].ulPinConfiguration);

  NVIC_DisableIRQ(TWI1_IRQn);
  NVIC_ClearPendingIRQ(TWI1_IRQn);
  NVIC_SetPriority(TWI1_IRQn, 0);
  NVIC_EnableIRQ(TWI1_IRQn);
}

static void Wire1_Init(void) {
    pmc_enable_periph_clk(WIRE1_INTERFACE_ID);
  PIO_Configure(
      g_APinDescription[PIN_WIRE1_SDA].pPort,
      g_APinDescription[PIN_WIRE1_SDA].ulPinType,
      g_APinDescription[PIN_WIRE1_SDA].ulPin,
      g_APinDescription[PIN_WIRE1_SDA].ulPinConfiguration);
  PIO_Configure(
      g_APinDescription[PIN_WIRE1_SCL].pPort,
      g_APinDescription[PIN_WIRE1_SCL].ulPinType,
      g_APinDescription[PIN_WIRE1_SCL].ulPin,
      g_APinDescription[PIN_WIRE1_SCL].ulPinConfiguration);

  NVIC_DisableIRQ(TWI0_IRQn);
  NVIC_ClearPendingIRQ(TWI0_IRQn);
  NVIC_SetPriority(TWI0_IRQn, 0);
  NVIC_EnableIRQ(TWI0_IRQn);
}
const int pingPin = 11; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 10; // Echo Pin of Ultrasonic Sensor

char *typeName[]={"Object","Ambient", "Calculated Object Celsius", "Calculated Object Fahrenheit"};
double microsecondsToCentimeters(long microseconds);
float patientArea = 0;
float prev_val=-1;
double area= 0;
#define MAX_WORD_COUNT 12
char *Words[MAX_WORD_COUNT];
uint16_t values[MAX_WORD_COUNT];
String serialRead = "";

void setup() {
  Serial.begin(9600);
  pinMode(8,INPUT);
  pinMode(9,OUTPUT);
  pinMode(pingPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(9, HIGH);
  Serial.println("Robojax MLX90614 test");  
  //Wire1.begin(9);                // join i2c bus with address #4
  //Wire1.onReceive(receiveEvent); // register event

  pinMode(SYNC_PIN, OUTPUT);
  digitalWrite(SYNC_PIN, LOW);

  Wire_Init();
  // Disable PDC channel
  pTwi->TWI_PTCR = UART_PTCR_RXTDIS | UART_PTCR_TXTDIS;
  TWI_ConfigureMaster(pTwi, TWI_CLOCK, VARIANT_MCK);
}

void loop() {
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  // Sets the pingPin on HIGH state for 10 micro seconds
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  float ratio = 0.5;
  float duration = pulseIn(echoPin, HIGH);
  double cm = microsecondsToCentimeters(duration);

  double meters = cm / 100;
  area = 3.14159265358979 * (meters * meters);
  Serial.print("Sensor Area is : ");
  Serial.println(area);
  //patientArea = bodyArea();
  uint16_t tempUK;
  float tempK;
  uint8_t hB, lB, pec;

  digitalWrite(SYNC_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(SYNC_PIN, LOW);

  TWI_StartRead(pTwi, ADDR, TOBJ_1, 1);

  lB = readByte();
  hB = readByte();
  
  //last read
  TWI_SendSTOPCondition(pTwi);
  pec = readByte();
  
  while (!TWI_TransferComplete(pTwi)) 
    ;
  //TWI_WaitTransferComplete(pTwi, RECV_TIMEOUT);

  tempUK = (hB << 8) | lB;
  if(tempUK & (1 << 16)) {
    Serial.print("Error !");
    Serial.println(tempK);
  } 
  else {
    tempK = ((float)tempUK * 2) / 100 ;
    Serial.print(" C: ");
    Serial.println(tempK - 273.15);
  }
  float tempObjec = tempK - 273.15;
   if (patientArea == -1)
  {
    Serial.println("no patient area");
    prev_val = tempObjec;
    delay(1000);
    return;
  }
  else 
  {Serial.print("patient area = ");
    Serial.println(patientArea); 
    ratio = patientArea/area;
  } 
  float bodyTemp = ((tempObjec) - ((1 - ratio) * (prev_val))) / (ratio);
  Serial.print("Body Temp -> ");
  Serial.println(bodyTemp);
  delay(1000);
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


uint8_t readByte() {
  //TWI_WaitByteReceived(pTwi, RECV_TIMEOUT);
  while (!TWI_ByteReceived(pTwi))
    ;
  return TWI_ReadByte(pTwi);
}

static inline bool TWI_WaitTransferComplete(Twi *_twi, uint32_t _timeout) {
  while (!TWI_TransferComplete(_twi)) {
    if (TWI_FailedAcknowledge(_twi))
      return false;
    if (--_timeout == 0)
      return false;
  }
  return true;
}

static inline bool TWI_WaitByteReceived(Twi *_twi, uint32_t _timeout) {
  while (!TWI_ByteReceived(_twi)) {
    if (TWI_FailedAcknowledge(_twi))
      return false;
    if (--_timeout == 0)
      return false;
  }
  return true;
}

static inline bool TWI_FailedAcknowledge(Twi *pTwi) {
  return pTwi->TWI_SR & TWI_SR_NACK;
}

double microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}


void SendData(double calcBodyTemp)
{
  // send data to machine most probably Raspberry
}
/*
void receiveEvent(int howMany)
{
  //Serial.println("something came here!");
  String i2cData = "";
  if ((char)Wire1.read() != '<')
  {serialRead == i2cData;
    return;
  }
  while(1 < Wire1.available()) // loop through all but the last
  {
    i2cData += Wire1.read();
    i2cData += (char)Wire1.read();// receive byte as a character
  }
  if ((char)Wire1.read() != '>')
  {serialRead = ""; return;}
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
    values[i] = atoi(Words[i]);
    values[i] = values[i] << 2;
    Serial.print(values[i]);
    Serial.print(",");
  }
  Serial.println();
  return  word_count;
}*/
