import board
import busio

# Create I2C object
i2c = busio.I2C(board.GP19, board.GP18)
# Wait until I2C lock is acquired
while not i2c.try_lock():
    pass

try:
    # Scan for I2C devices
    devices = i2c.scan()
    if devices:
        print("I2C devices found:", [hex(device) for device in devices])
    else:
        print("No I2C devices found.")
finally:
    # Release the I2C lock
    i2c.unlock()
