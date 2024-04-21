/*
  https://arduinogetstarted.com/tutorials/arduino-lm35-temperature-sensor
*/

#define ADC_VREF_mV    5000.0 // in millivolt
#define ADC_RESOLUTION 1024.0
#define PIN_LM35       A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  // get the ADC value from the temperature sensor
  int adcVal = analogRead(PIN_LM35);
  // convert the ADC value to voltage in millivolt
  float milliVolt = adcVal * (ADC_VREF_mV / ADC_RESOLUTION);
  // convert the voltage to the temperature in Celsius
  float tempC = milliVolt / 10;

  // print the temperature in the Serial Monitor:
  Serial.print("Temperature (°C): ");
  Serial.println(tempC);   // print the temperature in Celsius
  delay(1000);
}
