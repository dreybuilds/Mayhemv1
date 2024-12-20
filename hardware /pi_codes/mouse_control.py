import spidev
import RPi.GPIO as GPIO
from pynput.mouse import Controller, Button
import time

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

# GPIO setup for joystick button
BUTTON_PIN = 23  # Change to the GPIO pin you're using
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Mouse controller
mouse = Controller()

# Screen dimensions (adjust as needed)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

# Sensitivity scaling factor
SENSITIVITY = 0.1

def read_adc(channel):
    """Read ADC data from MCP3008."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7.")
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    return data

def map_value(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

try:
    while True:
        # Read joystick X and Y axes
        x_axis = read_adc(0)  # Channel 0
        y_axis = read_adc(1)  # Channel 1

        # Map joystick values to screen dimensions
        x_movement = map_value(x_axis, 0, 1023, -SENSITIVITY * SCREEN_WIDTH, SENSITIVITY * SCREEN_WIDTH)
        y_movement = map_value(y_axis, 0, 1023, -SENSITIVITY * SCREEN_HEIGHT, SENSITIVITY * SCREEN_HEIGHT)

        # Move mouse
        mouse.move(x_movement, -y_movement)  # Invert Y for natural movement

        # Check joystick button state for clicks
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            mouse.click(Button.left, 1)
            time.sleep(0.2)  # Debounce delay

        time.sleep(0.01)  # Polling delay

except KeyboardInterrupt:
    print("Exiting...")
finally:
    spi.close()
    GPIO.cleanup()

