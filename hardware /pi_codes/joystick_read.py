import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7.")
    # Send start bit, single-ended mode, and channel number
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    # Combine two bytes into a 10-bit result
    data = ((adc[1] & 3) << 8) | adc[2]
    return data

try:
    while True:
        x_axis = read_adc(0)  # Channel 0
        y_axis = read_adc(1)  # Channel 1
        print(f"X: {x_axis}, Y: {y_axis}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    spi.close()
