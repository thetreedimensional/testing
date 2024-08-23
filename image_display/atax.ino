// Define the baud rate
const long baudRate = 9600;

// Define the pin for the LED
const int ledPin = 13;

// Buffer to store incoming serial data
const int bufferSize = 50;
char inputBuffer[bufferSize];
int bufferIndex = 0;
bool openReceived = false;
bool lockout = false;

// Function to initialize the serial communication
void setup() {
  // Start serial communication at 9600 baud
  Serial.begin(baudRate);

  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
  
  // Seed the random number generator
  randomSeed(analogRead(0));
  
  // Wait for the serial port to initialize
  delay(1000);

  // Send a message to indicate that the Arduino is ready
  Serial.println("Waiting for command...");
}

// Function to handle received serial data
void processSerialData() {
  while (Serial.available()) {
    char receivedChar = Serial.read();

    // Check if we received a newline or carriage return
    if (receivedChar == '\n' || receivedChar == '\r') {
      inputBuffer[bufferIndex] = '\0';  // Null-terminate the buffer

      // Process the received message
      if (strcmp(inputBuffer, "OPEN") == 0) {
        openReceived = true;
        delay(3000);
        lockout = false;
        Serial.println("OPEN received. Proceeding...");
      } else if (strcmp(inputBuffer, "LOCKOUT") == 0) {
        lockout = true;
        openReceived = false;  // Reset openReceived on lockout
        Serial.println("LOCKOUT received. System locked out.");
      } else {
        Serial.println("Received message is not recognized.");
      }

      // Reset buffer index for the next message
      bufferIndex = 0;
    } else if (bufferIndex < bufferSize - 1) {
      // Store the incoming character in the buffer
      inputBuffer[bufferIndex++] = receivedChar;
    } else {
      // Buffer overflow protection
      Serial.println("Buffer overflow, resetting index.");
      bufferIndex = 0;
    }
  }
}

void loop() {
  processSerialData();

  // Only proceed if not in lockout state and OPEN has been received
  if (!lockout && openReceived) {
    Serial.println("Starting main sequence...");
    
    // Send START message
    Serial.println("START");
    
    // Wait for 1 second
    delay(3000);

    // Send the first random number
    sendRandomNumber();
    
    // Wait for 1 second
    delay(3000);

    // Send the second random number
    sendRandomNumber();
    
    // Wait for 1 second
    delay(3000);

    // Send SUBMIT message
    Serial.println("SUBMIT");
    
    // Flash the LED
    flashLED();

    // Reset state after completing the sequence
    openReceived = false;
  }
}

// Function to generate and send a random number between 1 and 16
void sendRandomNumber() {
  // Generate a random number between 1 and 16
  int randomNumber = random(1, 17);  // random() generates numbers from 1 to 16 inclusive

  // Send the random number over serial
  //Serial.print("Sending random number: ");
  Serial.println(randomNumber);
}

// Function to flash the LED
void flashLED() {
  // Turn the LED on
  digitalWrite(ledPin, HIGH);
  
  // Wait for 200 milliseconds
  delay(200);
  
  // Turn the LED off
  digitalWrite(ledPin, LOW);
  
  // Wait for another 200 milliseconds
  delay(200);
}
