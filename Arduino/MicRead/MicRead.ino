void setup() {
  // put your setup code here, to run once:
  pinMode(12, INPUT);
  Serial.begin(57600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int v;
  v = analogRead(12);
  //if(v>1024)
  Serial.println(v);
  //delayMicroseconds(23);
}
