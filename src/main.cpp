#include "SparkFunLSM6DSO.h"
#include "Wire.h"
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define LED_PIN 32
#define SIP_PIN 26

// Track clap detection
int soundState = 0;
unsigned long lastClapTime = 0;
int clapCount = 0;
bool ledState = false;
unsigned long lastLedToggleTime = 0;

void setup() {
  pinMode(SIP_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  soundState = digitalRead(SIP_PIN);

  unsigned long currentTime = millis();

  if (soundState == HIGH) {
    // If more than 3 seconds since the last clap, reset the clap count
    if (currentTime - lastClapTime > 3000) {
      clapCount = 0;
    }
    
    lastClapTime = currentTime;
    clapCount++;
    Serial.println("Clap detected");
    
    // Check for double clap (2 claps in 3 seconds)
    if (clapCount == 2 && !ledState && currentTime - lastLedToggleTime > 5000) {
      ledState = true;
      digitalWrite(LED_PIN, HIGH);
      lastLedToggleTime = currentTime;
      Serial.println("LED turned ON");
    }
    
    // Check for quadruple clap (4 claps in 3 seconds)
    if (clapCount == 4 && ledState && currentTime - lastLedToggleTime > 5000) {
      ledState = false;
      digitalWrite(LED_PIN, LOW);
      lastLedToggleTime = currentTime;
      Serial.println("LED turned OFF");
    }
  } else {
        Serial.println("No sound");
  }

  delay(50);
}
