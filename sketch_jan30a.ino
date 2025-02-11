void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
  Serial.println("Ready to communicate");
}

void loop() {
  // Step 1: Check if data is available on the serial port
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read the incoming number (newline character)
    int blinkCount = input.toInt(); // Convert the input to an integer

    if (blinkCount > 0) {
      // Step 2: Blink the LED
      for (int i = 0; i < blinkCount; i++) {
        digitalWrite(ledPin, HIGH);
        delay(1000);
        digitalWrite(ledPin, LOW);
        delay(1000);
      }

      // Step 3: Send a random number back to Python
      int randomDelay = random(1, 10);
      Serial.println(randomDelay);
    }
  }
}
