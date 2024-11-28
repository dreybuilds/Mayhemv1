#include <SPI.h>
#include <Esplora.h>

const int ssPin = 10; // Slave select pin

void setup() {
  Serial.begin(9600);
  SPI.begin();
  pinMode(ssPin, OUTPUT);
  digitalWrite(ssPin, HIGH); // Deselect slave
}

void loop() {
  // Read all Esplora sensor values
  int xValue = Esplora.readJoystickX();
  int yValue = Esplora.readJoystickY();
  int switch1State = Esplora.readButton(SWITCH_1);
  int switch2State = Esplora.readButton(SWITCH_2);
  int switch3State = Esplora.readButton(SWITCH_3);
  int switch4State = Esplora.readButton(SWITCH_4);
  int sliderValue = Esplora.readSlider();
  int accelX = Esplora.readAccelerometer(X_AXIS);
  int accelY = Esplora.readAccelerometer(Y_AXIS);
  int accelZ = Esplora.readAccelerometer(Z_AXIS);
  int lightLevel = Esplora.readLightSensor();
  int temperature = Esplora.readTemperature();
  int soundLevel = Esplora.readMicrophone();

  // Send data over SPI
  digitalWrite(ssPin, LOW); // Select the slave
  SPI.transfer(xValue >> 8); SPI.transfer(xValue & 0xFF); // Joystick X
  SPI.transfer(yValue >> 8); SPI.transfer(yValue & 0xFF); // Joystick Y
  SPI.transfer(switch1State);
  SPI.transfer(switch2State);
  SPI.transfer(switch3State);
  SPI.transfer(switch4State);
  SPI.transfer(sliderValue >> 8); SPI.transfer(sliderValue & 0xFF); // Slider
  SPI.transfer(accelX >> 8); SPI.transfer(accelX & 0xFF); // Accelerometer X
  SPI.transfer(accelY >> 8); SPI.transfer(accelY & 0xFF); // Accelerometer Y
  SPI.transfer(accelZ >> 8); SPI.transfer(accelZ & 0xFF); // Accelerometer Z
  SPI.transfer(lightLevel >> 8); SPI.transfer(lightLevel & 0xFF); // Light sensor
  SPI.transfer(temperature); // Temperature (assuming one byte)
  SPI.transfer(soundLevel >> 8); SPI.transfer(soundLevel & 0xFF); // Microphone
  digitalWrite(ssPin, HIGH); // Deselect the slave

  delay(100); // Delay between transmissions
}
