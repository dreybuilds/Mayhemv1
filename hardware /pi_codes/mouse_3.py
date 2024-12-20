import spidev
import time
from pynput.mouse import Controller

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

# Mouse controller
mouse = Controller()

# Screen dimensions (adjust as per your setup)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

# Joystick sensitivity
SENSITIVITY = 0.05  # Increase for more noticeable movement
DEAD_ZONE = 100  # Dead zone to avoid drift near the center position

def read_adc(channel):
    """Read data from a specific MCP3008 channel."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7.")
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    return data

def map_value(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    print("Use joystick to control the mouse. Press Ctrl+C to exit.")
    while True:
        # Read joystick values from MCP3008
        x_value = read_adc(0)  # X-axis connected to CH0
        y_value = read_adc(1)  # Y-axis connected to CH1

        # Apply dead zone
        if abs(x_value - 512) < DEAD_ZONE:
            x_value = 512
        if abs(y_value - 512) < DEAD_ZONE:
            y_value = 512

        # Map joystick values to relative mouse movement
        x_movement = map_value(x_value, 0, 1023, -SENSITIVITY * SCREEN_WIDTH, SENSITIVITY * SCREEN_WIDTH)
        y_movement = map_value(y_value, 0, 1023, -SENSITIVITY * SCREEN_HEIGHT, SENSITIVITY * SCREEN_HEIGHT)

        # Debug: print joystick values and movement
        print(f"X ADC: {x_value}, Y ADC: {y_value}")
        print(f"X movement: {x_movement}, Y movement: {y_movement}")

        # Get the current mouse position
        current_x, current_y = mouse.position

        # Calculate new mouse position
        new_x = max(0, min(SCREEN_WIDTH - 1, current_x + int(x_movement)))
        new_y = max(0, min(SCREEN_HEIGHT - 1, current_y - int(y_movement)))  # Invert Y-axis for natural movement

        # Debug: print current and new mouse positions
        print(f"Current Mouse Position: ({current_x}, {current_y})")
        print(f"New Mouse Position: ({new_x}, {new_y})")

        # Move mouse to the new position
        mouse.position = (new_x, new_y)

        # Polling delay
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    spi.close()
