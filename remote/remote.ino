// Stupid simple controller for the visor of 0x4C6F75
//
// Published under the unlicense - 2025

// Define the pins for the buttons
const int inputButtonPins[] = {16, 14, 15, 18};
const int modButtonPins[] = {20, 21};

// Define keycodes for input buttons
const int keycodeInput[] = {0x01, 0x02, 0x03, 0x04};

// Define keycodes for modifier combinations
const int keycodeMod1[] = {0x05, 0x06, 0x07, 0x08};
const int keycodeMod2[] = {0x09, 0x0A, 0x0B, 0x0C};
const int keycodeModBoth[] = {0x0D, 0x0E, 0x0F, 0x10};

const int keyUpCode = 0x00;

// Variables to store the previous state of input buttons
bool prevInputButtonStates[] = {HIGH, HIGH, HIGH, HIGH};

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set button pins as inputs with pull-up resistors
  for (int pin : inputButtonPins) {
    pinMode(pin, INPUT_PULLUP);
  }
  for (int pin : modButtonPins) {
    pinMode(pin, INPUT_PULLUP);
  }
}

void loop() {
  // Read the state of each modifier button
  bool mod1Pressed = digitalRead(modButtonPins[0]) == LOW;
  bool mod2Pressed = digitalRead(modButtonPins[1]) == LOW;

  // Check each input button
  for (int i = 0; i < 4; i++) {
    bool currentState = digitalRead(inputButtonPins[i]);

    // Check if the button was just pressed (transition from HIGH to LOW)
    if (prevInputButtonStates[i] == HIGH && currentState == LOW) {
      // Determine which keycode to send based on modifier buttons
      if (mod1Pressed && mod2Pressed) {
        Serial.write(keycodeModBoth[i]);
      } else if (mod1Pressed) {
        Serial.write(keycodeMod1[i]);
      } else if (mod2Pressed) {
        Serial.write(keycodeMod2[i]);
      } else {
        Serial.write(keycodeInput[i]);
      }
    }
    // Check if the button was just released (transition from LOW to HIGH)
    else if (prevInputButtonStates[i] == LOW && currentState == HIGH) {
      Serial.write(keyUpCode);
    }

    // Update the previous state
    prevInputButtonStates[i] = currentState;
  }

  // Small delay to debounce the buttons
  delay(50);
}
