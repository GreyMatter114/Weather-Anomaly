import asyncio
import digitalio
import board
from sensor_reader import read_sensors
from model_executor import run_model

# Initialize button on pin D17
button = digitalio.DigitalInOut(board.GP22)
button.switch_to_input(pull=digitalio.Pull.UP)

# Toggle flag for running the sensors and model logic
is_running = False

# Function to handle asynchronous button press
async def check_button():
    """Checks if the button is pressed and toggles the state asynchronously."""
    global is_running
    last_state = button.value
    while True:
        current_state = button.value
        if last_state and not current_state:  # Button pressed (low state)
            is_running = not is_running
            print(f"🔄 Toggled: {'Running' if is_running else 'Paused'}")
        last_state = current_state
        await asyncio.sleep(0.05)  # Check button state every 50ms to handle debounce

# ✅ Run Everything with Toggle Control
async def main():
    global is_running

    # Start sensor and model reading tasks
    sensor_task = asyncio.create_task(read_sensors())
    model_task = asyncio.create_task(run_model())

    # Start asynchronous button press handling
    button_task = asyncio.create_task(check_button())

    while True:
        if is_running:
            # Enable sensor reading and model processing tasks
            if sensor_task.done():
                sensor_task = asyncio.create_task(read_sensors())
            if model_task.done():
                model_task = asyncio.create_task(run_model())
        else:
            # Stop sensor reading and model processing tasks
            if not sensor_task.done():
                sensor_task.cancel()
            if not model_task.done():
                model_task.cancel()

        await asyncio.sleep(0.1)  # Small delay to prevent excessive CPU usage

# Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())
