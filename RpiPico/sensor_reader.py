import time
import asyncio
import board
import busio
import adafruit_dht
import adafruit_bmp280
import analogio

# ✅ Initialize Sensors
i2c = busio.I2C(board.GP19, board.GP18)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
dht11 = adafruit_dht.DHT11(board.GP28_A2)
print(dht11.humidity)
# ✅ Shared Resource for Sensor Readings with Async Lock
sensor_data = {
    "temperature": None,
    "humidity": None,
    "pressure": None
}
data_lock = asyncio.Lock()

# ✅ Asynchronous Sensor Reading Function
async def read_sensors():
    global sensor_data

    while True:
        try:
            temperature = dht11.temperature
            humidity = dht11.humidity
            pressure = bmp280.pressure

            if temperature is not None and humidity is not None and pressure is not None:
                async with data_lock:
                    sensor_data["temperature"] = temperature
                    sensor_data["humidity"] = humidity
                    sensor_data["pressure"] = pressure

                print(f"🔄 Sensor Updated: T={temperature:.2f}°C, H={humidity:.2f}%, P={pressure:.2f} hPa")
        
        except RuntimeError as e:
            print(f"⚠️ Sensor Read Error: {e}")

        await asyncio.sleep(5)  # Read every 5 seconds
