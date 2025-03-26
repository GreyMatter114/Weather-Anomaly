import time
import board
import busio
import adafruit_bmp280

# Set up I2C communication (assuming your BMP280 is connected via I2C)
i2c = busio.I2C(board.GP19, board.GP18)

# Create an instance of the BMP280 sensor
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Optionally, you can set the sensor's sea level pressure (needed for accurate altitude measurements)
# bmp280.sea_level_pressure = 1013.25  # (in hPa)

# Main loop to continuously read and print temperature and pressure
while True:
    temperature = bmp280.temperature  # Get temperature in Celsius
    pressure = bmp280.pressure      # Get pressure in hPa
    altitude = bmp280.altitude      # Get altitude in meters (if sea level pressure is set)

    # Print the values
    print(f"Temperature: {temperature:.2f}°C")
    print(f"Pressure: {pressure:.2f} hPa")
    print(f"Altitude: {altitude:.2f} meters")

    # Wait for 2 seconds before reading again
    time.sleep(2)
