#include <Wire.h>

// I2C address for LSM6DS3
#define LSM6DS3_ADDR 0x6A

// LSM6DS3 Register addresses
#define LSM6DS3_REG_CTRL1_XL 0x10  // Accelerometer control register
#define LSM6DS3_REG_OUTX_L_XL 0x28  // Accelerometer data register (X axis)

void setup() {
  // Start serial communication
  Serial.begin(9600);
  
  // Initialize I2C
  Wire.begin();

  // Initialize the LSM6DS3 sensor
  initLSM6DS3();
}

void loop() {
  // Read accelerometer data
  int16_t x = readAccelData(LSM6DS3_REG_OUTX_L_XL);
  int16_t y = readAccelData(LSM6DS3_REG_OUTX_L_XL + 2); // Y data is 2 bytes after X
  int16_t z = readAccelData(LSM6DS3_REG_OUTX_L_XL + 4); // Z data is 2 bytes after Y
  
  // Send data to the serial port
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(z);

  delay(1000);  // Wait for 1 second (adjust this to change sampling frequency)
}

void initLSM6DS3() {
  // Set the accelerometer to a normal mode with a 104 Hz sampling rate
  Wire.beginTransmission(LSM6DS3_ADDR);
  Wire.write(LSM6DS3_REG_CTRL1_XL);  // Accelerometer control register
  Wire.write(0x60);  // 104 Hz, 2g sensitivity
  Wire.endTransmission();
}

int16_t readAccelData(uint8_t reg) {
  Wire.beginTransmission(LSM6DS3_ADDR);
  Wire.write(reg);  // Set the register to read from
  Wire.endTransmission(false);  // Repeated start
  
  // Request 2 bytes of data from the register
  Wire.requestFrom(LSM6DS3_ADDR, 2);
  
  // Read the 2 bytes of data
  uint8_t lowByte = Wire.read();
  uint8_t highByte = Wire.read();
  
  // Combine the two bytes into one 16-bit integer
  int16_t value = (int16_t)((highByte << 8) | lowByte);
  
  return value; 
}
