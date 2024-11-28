https://www.youtube.com/watch?v=dnYhW7ltmNI&ab_channel=EasyTech
https://www.youtube.com/watch?app=desktop&v=T6HsRRXBVS8&ab_channel=PaulMcWhorter
https://tronche.com/gui/x/xlib/input/XWarpPointer.html
https://pyautogui.readthedocs.io/en/latest/


To use analog signals (e.g., from a joystick or potentiometer) to control the mouse position on an Ubuntu system running on a Raspberry Pi 4, you need the following steps:

---

### **1. Hardware Requirements**

- Raspberry Pi 4 running Ubuntu.
- Analog joystick module or potentiometers (e.g., 2-axis joystick with X and Y outputs).
- Analog-to-Digital Converter (ADC), such as **MCP3008**.
- Jumper wires and breadboard.

---

### **2. Setup and Wiring**

#### **MCP3008 Pin Connections**

1. Connect the MCP3008 to the Raspberry Pi using SPI:
    - **VDD** → 3.3V (power).
    - **VREF** → 3.3V.
    - **AGND** and **DGND** → Ground.
    - **CLK** → GPIO11 (SPI clock).
    - **DOUT** → GPIO9 (MISO).
    - **DIN** → GPIO10 (MOSI).
    - **CS/SHDN** → GPIO8 (Chip Select).

#### **Joystick Pin Connections**

- Connect the joystick’s:
    - **VCC** to 3.3V.
    - **GND** to Ground.
    - **X-axis output** to **CH0** on the MCP3008.
    - **Y-axis output** to **CH1** on the MCP3008.

---

### **3. Install Required Libraries**

Install the necessary Python libraries:

```bash
pip install spidev pyautogui
```

---

### **4. Python Code to Read Analog Inputs**

Read values from the joystick and map them to mouse movements using the `pyautogui` library.

```python
import spidev
import pyautogui
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

# Read MCP3008 channel
def read_channel(channel):
    assert 0 <= channel <= 7, "Channel must be between 0 and 7."
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

# Map analog value to screen coordinates
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Joystick neutral range
dead_zone = 100  # Adjust to reduce sensitivity in the center

# Main loop
try:
    while True:
        x_value = read_channel(0)  # Read X-axis
        y_value = read_channel(1)  # Read Y-axis

        # Map joystick values to screen resolution
        if abs(x_value - 512) > dead_zone:
            x_movement = map_value(x_value, 0, 1023, 0, screen_width)
            pyautogui.moveTo(x_movement, None, duration=0.01)

        if abs(y_value - 512) > dead_zone:
            y_movement = map_value(y_value, 0, 1023, 0, screen_height)
            pyautogui.moveTo(None, y_movement, duration=0.01)

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting.")
    spi.close()
```

---

### **5. Explanation**

1. **SPI Communication**:
    
    - The MCP3008 reads the analog signal and converts it to a 10-bit digital value (0–1023).
    - The `spidev` library communicates with the MCP3008 over the SPI bus.
2. **Dead Zone**:
    
    - A range around the joystick's center position is ignored to reduce unintended cursor drift.
3. **Mouse Movement**:
    
    - `pyautogui.moveTo(x, y)` moves the cursor to the desired coordinates.
    - The `map_value()` function scales joystick output to the screen resolution.

---

### **6. Testing**

1. Move the joystick and verify the mouse cursor responds accordingly.
2. Adjust the **dead zone** or scaling if the movements are too sensitive or sluggish.
3. Test the setup in Ubuntu to ensure compatibility with your applications.

---

### **7. Enhancements**

- Add **button support**:
    - Connect buttons to GPIO pins and use the `gpiozero` library to simulate clicks or other mouse actions.
- **Smooth movements**:
    - Use a filter (e.g., moving average) to smooth cursor movements.
- **Custom cursor speed**:
    - Introduce a scaling factor for fast or slow cursor movement.

This implementation allows precise control of the mouse using analog signals on Ubuntu running on a Raspberry Pi.