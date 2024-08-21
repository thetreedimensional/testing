import serial
import time

# Set up the serial connection
serial_port = '/dev/ttyACM0'  # Adjust this based on your setup (e.g., ttyUSB0, etc.)
baud_rate = 9600  # Match the baud rate with the Arduino

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Connected to {serial_port} at {baud_rate} baud rate.")

    # Send the "OPEN" command to the Arduino
    open_command = "OPEN\n"
    ser.write(open_command.encode('utf-8'))
    print(f"Sent: {open_command.strip()}")

    # Allow time for the Arduino to process the command
    time.sleep(1)

    while True:
        # Read data from the serial port
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")

except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Exiting the program.")
finally:
    if ser.is_open:
        ser.close()
        print(f"Closed connection to {serial_port}.")
