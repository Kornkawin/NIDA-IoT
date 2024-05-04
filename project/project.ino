// C++
//
#define echoPin 2
#define trigPin 3
#define ledPin 4
#define tiltPin 5
#define buzzerPin 7
#define servoPin 8
#define dataPin 11
#define latchPin 12
#define clockPin 13
#define temperaturePin A0
#define gasPin A1
#include <Servo.h>

Servo servo;
int pos = 90;
int soundVelocity = 340; // define sound speed = 340 m/s
byte num[] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90}; // 0-9

void setup() {
  // 7-segment display
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  // ultrasonic
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  // Servo
  servo.attach(servoPin);
  servo.write(pos);
  // Buzzer
  pinMode(buzzerPin, OUTPUT);
  // LED
  pinMode(ledPin, OUTPUT);
  // Tilt Sensor
  pinMode(tiltPin, INPUT);
  digitalWrite(tiltPin, HIGH);
  // Gas Sensor
  pinMode(gasPin, INPUT);
  // Serial
  Serial.begin(9600);
}

void displayNum(int index) {
  index = index % 10;
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, num[index]);
  digitalWrite(latchPin, HIGH);
}

float getSonarDistance() {
  float distance;
  unsigned long pingTime;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  pingTime = pulseIn(echoPin, HIGH);
  distance = (float)pingTime / 58;
  // Serial.println(distance);
  return distance; // in cm
}

float getTemperatureInCelsius() {
  int reading = analogRead(temperaturePin);
  float millVolt = reading * (5000 / 1024.0);
  float temperature = millVolt / 10;
  //Serial.println(temperature);
  return temperature;
}

bool checkTilt() {
  int isTilt = digitalRead(tiltPin);
  Serial.println(isTilt);
  return !isTilt;
}

bool checkSmoke() {
  int gasState = analogRead(gasPin);
  //Serial.println(gasState);
  return gasState > 150;
}

void openBin() {
  pos = 90;
  servo.write(pos);
  digitalWrite(ledPin, LOW);
}

void closeBin() {
  pos = 180;
  servo.write(pos);
  digitalWrite(ledPin, HIGH);
}

void loop() {
  int celsius = (int)getTemperatureInCelsius();
  if (celsius > 60){ //|| checkSmode()) {
    // heat+smoke
    tone(buzzerPin, 700);
    closeBin();
  } else if (checkTilt()) {
    // tilt state
    tone(buzzerPin, 400);
    digitalWrite(ledPin, HIGH);
  } else {
    // Normal
    noTone(buzzerPin);
    digitalWrite(ledPin, LOW);

    int cm = (int)getSonarDistance();
    if (cm > 70) displayNum(0);
    else if (cm > 65) displayNum(1);
    else if (cm > 60) displayNum(2);
    else if (cm > 55) displayNum(3);
    else if (cm > 50) displayNum(4);
    else if (cm > 45) displayNum(5);
    else if (cm > 40) displayNum(6);
    else if (cm > 30) displayNum(7);
    else if (cm > 20) displayNum(8);
    else if (cm < 10) displayNum(9);

    if (cm < 10) closeBin();
    else openBin();
  }

  delay(1000);
}
