import serial
from PIL import Image

# Dictionary mapping numbers to filenames
image_files = {
    1: "Boat.png",
    2: "Cat.png",
    3: "Clock.png",
    4: "Eyeball.png",
    5: "Gear.png",
    6: "Heart.png",
    7: "House.png",
    8: "Leaf.png",
    9: "Mountain.png",
    10: "Peace.png",
    11: "Scale.png",
    12: "Shield.png",
    13: "Skull.png",
    14: "Spider.png",
    15: "Sunset.png",
    16: "Wave.png",
}

def display_image(number):
    """Display the image corresponding to the number."""
    if number in image_files:
        try:
            # Open and display the image
            img = Image.open(image_files[number])
            img.show()
        except FileNotFoundError:
            print(f"File {image_files[number]} not found.")
    else:
        print("Invalid number. Please enter a number between 1 and 16.")

def main():
    # Replace 'COM3' with your serial port name (e.g., '/dev/ttyUSB0' for Linux)
    serial_port = 'COM3'
    baud_rate = 9600  # Adjust if necessary

    try:
        # Open serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Listening on {serial_port}...")

        while True:
            if ser.in_waiting > 0:
                try:
                    # Read line from serial port
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Received: {line}")
                    # Split the line by commas and process each number
                    numbers = line.split(',')
                    id_list = input_data.split(',')
                    # Get corresponding image filenames
                    image_files = get_image_list(id_list)
                    print(image_files) # images selected
                    #combine_images(image_files, output_file, show=True)
                    # to do 
                    # resize image
                    # display image
                    #send file via serial poert
                except ValueError:
                    print("Received invalid data. Please send a number in text format.")
    
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()