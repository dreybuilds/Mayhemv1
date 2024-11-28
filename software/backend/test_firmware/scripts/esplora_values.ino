#include <SPI.h>
#include <Esplora.h>

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop() {
  // Read joystick positions
  int xValue = Esplora.readJoystickX();
  int yValue = Esplora.readJoystickY();

  // Read the state of each switch
  int switch1State = Esplora.readButton(SWITCH_1);
  int switch2State = Esplora.readButton(SWITCH_2);
  int switch3State = Esplora.readButton(SWITCH_3);
  int switch4State = Esplora.readButton(SWITCH_4);

  // Read the slider position
  int sliderValue = Esplora.readSlider();

  // Read accelerometer values
  int accelX = Esplora.readAccelerometer(X_AXIS);
  int accelY = Esplora.readAccelerometer(Y_AXIS);
  int accelZ = Esplora.readAccelerometer(Z_AXIS);

  // Read light sensor value
  int lightLevel = Esplora.readLightSensor();

  // Read temperature sensor value
  int temperature = Esplora.readTemperature(0);

  // Read microphone input
  int soundLevel = Esplora.readMicrophone();

  // Print all sensor and input values
  Serial.println("==== Esplora Sensor and Input Values ====");
  
  // Joystick
  Serial.print("Joystick X: ");
  Serial.print(xValue);
  Serial.print(" | Joystick Y: ");
  Serial.println(yValue);

  // Switches
  Serial.print("Switch 1: ");
  Serial.print(switch1State);
  Serial.print(" | Switch 2: ");
  Serial.print(switch2State);
  Serial.print(" | Switch 3: ");
  Serial.print(switch3State);
  Serial.print(" | Switch 4: ");
  Serial.println(switch4State);

  // Slider
  Serial.print("Slider: ");
  Serial.println(sliderValue);

  // Accelerometer
  Serial.print("Accelerometer X: ");
  Serial.print(accelX);
  Serial.print(" | Accelerometer Y: ");
  Serial.print(accelY);
  Serial.print(" | Accelerometer Z: ");
  Serial.println(accelZ);

  // Light sensor
  Serial.print("Light Level: ");
  Serial.println(lightLevel);

  // Temperature sensor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");

  // Microphone
  Serial.print("Sound Level: ");
  Serial.println(soundLevel);

  Serial.println("=========================================");
  
  delay(500); // Delay to avoid overwhelming the Serial Monitor
}
