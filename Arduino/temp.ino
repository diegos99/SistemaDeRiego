/*
 * Created by Pi BOTS MakerHub
 *
 * Email: pibotsmakerhub@gmail.com
 * 
 * Github: https://github.com/pibotsmakerhub
 *
 * Join Us on Telegram : https://t.me/pibots 
 * Copyright (c) 2020 Pi BOTS MakerHub
*/

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include "DHT.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor

#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.


// Constants
#define DELAY 500 // Delay between two measurements in ms
#define VIN 5 // V power voltage
#define R 10000 //ohm resistance value

DHT dht(DHTPIN, DHTTYPE);

// Parameters
const int sensorPin = A0; // Pin connected to sensor
//Variables
int sensorVal; // Analog value from the sensor
int lux; //Lux value


//Constants 
const int hygrometer = A1;  //Hygrometer sensor analog pin output at pin A0 of Arduino
//Variables 
int value;
 
void setup() {
  Serial.begin(9600);
  //Serial.println(F("DHTxx test!"));

  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

// -----------------------------------------------------------------------------------------------
// ---------- SENSOR DE HUMEDAD Y TEMPERATURA
// -----------------------------------------------------------------------------------------------
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  // COL A - TimeStamps
  // COL B - Humedad
  //Serial.print(F(" Humidity:"));
  Serial.print(h);
  Serial.print("%");
  Serial.print("\t");
  // COL C - Temperatura en C°
  //Serial.print(F("Temperature: "));
  Serial.print(t);
  Serial.print(F("C "));
  Serial.print("\t");
  // COL D - Temperatura en F°
  Serial.print(f);
  Serial.print(F("F"));
  Serial.print("\t");
  // COL E - Heat index en C°
  //Serial.print(F("Heat index C: "));
  Serial.print(hic);
  Serial.print(F("C "));
  Serial.print("\t");
  // COL F - Heat index en F°
  //Serial.print(F("Heat index F: "));
  Serial.print(hif);
  Serial.print(F("F"));

// -----------------------------------------------------------------------------------------------
// ---------- SENSOR DE LUZ
// -----------------------------------------------------------------------------------------------
  //  int value = analogRead(A0);
  //  Serial.println("Analog value : ");
  //  Serial.println(value);
  //  delay(250);
  sensorVal = analogRead(sensorPin);
  lux=sensorRawToPhys(sensorVal);
  // COL G - Raw value from light sensor
  //Serial.print("Raw value from sensor= ");
  Serial.print("\t");
  Serial.print(sensorVal); // the analog reading
  Serial.print("\t");
  // COL H - Raw value from light sensor in lumens
  //Serial.print("Physical value from sensor = ");
  Serial.print(lux); // the analog reading
  Serial.print(" lumen"); // the analog reading
  Serial.print("\t");
  delay(DELAY);

// -----------------------------------------------------------------------------------------------
// ---------- SENSOR DE HUMEDAD EN EL SUELO
// -----------------------------------------------------------------------------------------------
  // When the plant is watered well the sensor will read a value 380~400, I will keep the 400 
  // value but if you want you can change it below. 
  
    value = analogRead(hygrometer);   //Read analog value 
    value = constrain(value,400,1023);  //Keep the ranges!
    value = map(value,400,1023,100,0);  //Map value : 400 will be 100 and 1023 will be 0
    
    // COL I - Sensor de humedad
    //Serial.print("Soil humidity: ");
    Serial.println(value);
    //Serial.println(%);
    delay(2000); //Read every 2 sec.
}

// -----------------------------------------------------------------------------------------------
// ---------- SENSOR DE LUZ - CONVERSIÓN DE RESISTENCIA A LUMEN'S
// -----------------------------------------------------------------------------------------------
  int sensorRawToPhys(int raw){
    // Conversion rule
    float Vout = float(raw) * (VIN / float(1023));// Conversion analog to voltage
    float RLDR = (R * (VIN - Vout))/Vout; // Conversion voltage to resistance
    int phys=500/(RLDR/1000); // Conversion resitance to lumen
    return phys;
  }
