#include <Servo.h>

// Configuration
const int NUM_SERVOS = 5;
const int SERVO_PINS[NUM_SERVOS] = {9, 10, 11, 12, 13};
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;
const unsigned long BAUD_RATE = 115200;
const int SERVO_UPDATE_DELAY_MS = 15; // Delay between servo updates

Servo servos[NUM_SERVOS];
int targetAngles[NUM_SERVOS] = {90, 90, 90, 90, 90};
int currentAngles[NUM_SERVOS] = {90, 90, 90, 90, 90};

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial) { ; } // Wait for serial port to connect
  
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(SERVO_PINS[i]);
    servos[i].write(targetAngles[i]);
    delay(SERVO_UPDATE_DELAY_MS);
  }
  
  Serial.println("Servo Controller Ready");
  Serial.setTimeout(50); // Set shorter timeout for serial reads
}

void loop() {
  // Handle incoming serial data
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    processInput(input);
  }
  
  updateServosGradually();
}

void processInput(String input) {
  input.trim();
  
  // Validate input format
  if (input.length() == 0 || countCommas(input) != NUM_SERVOS - 1) {
    Serial.println("ERROR: Invalid input format");
    return;
  }
  
  // Temporary array for new angles
  int newAngles[NUM_SERVOS];
  
  // Parse angles
  int lastIndex = 0;
  for (int i = 0; i < NUM_SERVOS; i++) {
    int commaIndex = input.indexOf(',', lastIndex);
    if (i == NUM_SERVOS - 1) commaIndex = -1;
    
    String angleStr = (commaIndex == -1) ? 
      input.substring(lastIndex) : 
      input.substring(lastIndex, commaIndex);
      
    newAngles[i] = constrain(angleStr.toInt(), MIN_ANGLE, MAX_ANGLE);
    lastIndex = commaIndex + 1;
  }
  
  // Update target angles
  for (int i = 0; i < NUM_SERVOS; i++) {
    targetAngles[i] = newAngles[i];
  }
}

void updateServosGradually() {
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (currentAngles[i] != targetAngles[i]) {
      // Move one degree at a time toward target
      if (currentAngles[i] < targetAngles[i]) {
        currentAngles[i]++;
      } else {
        currentAngles[i]--;
      }
      
      servos[i].write(currentAngles[i]);
      delay(SERVO_UPDATE_DELAY_MS);
    }
  }
}

int countCommas(String s) {
  int count = 0;
  for (int i = 0; i < s.length(); i++) {
    if (s.charAt(i) == ',') count++;
  }
  return count;
}