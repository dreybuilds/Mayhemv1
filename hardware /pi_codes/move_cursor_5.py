import spidev
import time

# Set up SPI communication with MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CE0)

def read_adc(channel):
    """Read ADC value from MCP3008 (0-1023)"""
    if channel < 0 or channel > 7:
        return -1
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((r[1] & 3) << 8) + r[2]
    return value

def map_value(val, in_min, in_max, out_min, out_max):
    """Map a value from one range to another"""
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Main loop to read the joystick and print the X/Y values
while True:
    x_value = read_adc(0)  # Read X-axis from CH0
    y_value = read_adc(1)  # Read Y-axis from CH1

    # Map the ADC values to a range of -1 to 1
    x_movement = map_value(x_value, 0, 1023, -1, 1)
    y_movement = map_value(y_value, 0, 1023, -1, 1)

    print(f"Joystick X: {x_movement}, Y: {y_movement}")
    
    # Delay before next read
    time.sleep(0.1)
