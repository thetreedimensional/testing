import pygame
import sys
import serial
import time
import subprocess
import os
import signal

# Initialize Pygame
pygame.init()

# Get display information
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Define the mapping of serial commands to image files
image_files = {
    1: "Gear.png",
    2: "Boat.png",
    3: "House.png",
    4: "Clock.png",
    5: "Shield.png",
    6: "Mountain.png",
    7: "Leaf.png",
    8: "Skull.png",
    9: "Cat.png",
    10: "Wave.png",
    11: "Spider.png",
    12: "Sunset.png",
    13: "Eyeball.png",
    14: "Heart.png",
    15: "Peace.png",
    16: "Scale.png",
}

# Configure serial port
serial_port = '/dev/ttyACM0'  # Replace with your serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Initialize variables
last_two_images = [None, None]
current_image = None
selected_images = []
submit_received = False

# To track the last command and its timestamp
last_command = None
last_command_time = 0

def load_image(image_name):
    """Load an image and scale it to fit the screen."""
    try:
        image_path = f'for_display_blue/{image_name}'
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (screen_width, screen_height))
        return image
    except pygame.error as e:
        print(f"Error loading image {image_name}: {e}")
        return None

def overlay_images(base_image, overlay_image):
    """Overlay one image on top of another."""
    if base_image is None:
        return overlay_image  # If the base image is None, return the overlay image
    if overlay_image is None:
        return base_image  # If the overlay image is None, return the base image
    combined = base_image.copy()
    
    # combined.blit(overlay_image, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    combined.blit(overlay_image, (0, 0))
    return combined

def save_selections(selections):
    """Save the last two selected image numbers to a text file with spaces separating the numbers and a zero at the end."""
    last_two_selections = selections[-2:]
    selections_str = ' '.join(map(str, last_two_selections)) + ' 0'
    file_path = 'user_sequence.txt'
    with open(file_path, 'w') as file:
        file.write(selections_str + '\n')

    target_ip = '10.0.0.63'
    target_user = 'pi'
    target_pass = 'raspberry'
    destination_path = f'/home/{target_user}/atlas/state/user_sequence.txt'

    scp_command = [
        'sshpass', '-p', target_pass, 'scp', file_path, f'{target_user}@{target_ip}:{destination_path}'
    ]
    
    try:
        result = subprocess.run(scp_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("File transfer successful.")
            os.remove(file_path)
            print("File removed from the host machine.")
        else:
            print("File transfer failed.")
            print(result.stderr)
    except Exception as e:
        print(f"Error occurred during file transfer: {e}")

    wait_for_no_file_on_target()  # Wait only after submitting and transferring the file

def file_exists_on_target():
    """Check if the user_sequence.txt file exists on the target machine."""
    target_ip = '10.0.0.63'
    target_user = 'pi'
    target_pass = 'raspberry'
    destination_path = f'/home/{target_user}/atlas/state/user_sequence.txt'
    
    check_command = f"sshpass -p {target_pass} ssh {target_user}@{target_ip} 'test -f {destination_path}'"
    result = subprocess.run(check_command, shell=True, capture_output=True)
    
    return result.returncode == 0

def wait_for_no_file_on_target():
    """Poll the target machine until user_sequence.txt is not found."""
    print("Polling for the absence of user_sequence.txt on the target machine...")
    while file_exists_on_target():
        print("File found. Waiting 10 seconds before retrying...")
        time.sleep(10)
    print("No file found. Proceeding with serial data processing.")
    ser.write(b'OPEN\n')  # Send OPEN command via serial once the file is not found
    print("open issued")

def delete_file_on_target():
    """Delete the user_sequence.txt file on the target machine if it exists."""
    if file_exists_on_target():
        print("Deleting existing user_sequence.txt on the target machine...")
        target_ip = '10.0.0.63'
        target_user = 'pi'
        target_pass = 'raspberry'
        destination_path = f'/home/{target_user}/atlas/state/user_sequence.txt'

        delete_command = f"sshpass -p {target_pass} ssh {target_user}@{target_ip} 'rm {destination_path}'"
        result = subprocess.run(delete_command, shell=True, capture_output=True)
        print("File deleted successfully on the target machine.")
        if result.returncode == 0:
            print("File deleted successfully on the target machine.")
        else:
            print(f"Failed to delete file on target: {result.stderr}")

# Graceful shutdown handling
def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    if ser.is_open:
        ser.close()
    pygame.quit()
    sys.exit()

signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Initial check: delete the existing file on target if it exists
delete_file_on_target()

# Load special images
start_image = load_image("Start.png")
selected_overlay = load_image("Selected.png")

ser.write(b'OPEN\n')  # Send OPEN command to start for the first time

# Main loop
running = True
data_buffer = ""
while running:
    if ser.in_waiting > 0:
        try:
            data = ser.read().decode('utf-8').strip()
            current_time = time.time()

            if data == last_command and (current_time - last_command_time) < 0.1:
                continue  # Ignore this command if it's a duplicate

            last_command = data
            last_command_time = current_time

            print(data) # just for debugging

            if data == 'RESET':
                current_image = None
                last_two_images = [None, None]
                selected_images = []
                screen.fill((0, 0, 0))  # Clear the screen at the start of each loop iteration
            elif data == 'START':
                current_image = start_image
                last_two_images = [None, None]
                selected_images = []
            elif data == 'SUBMIT':
                submit_received = True
            elif data.isdigit():
                image_key = int(data)
                if image_key in image_files:
                    if image_key not in selected_images:
                        selected_images.append(image_key)  # store only unique selections
                    if len(selected_images) > 2:
                        selected_images = selected_images[-2:]

                    last_two_images = [
                        load_image(image_files[selected_images[0]]),
                        load_image(image_files[selected_images[1]]) if len(selected_images) > 1 else None,
                    ]

                    current_image = overlay_images(last_two_images[0], last_two_images[1])

        except ValueError:
            pass  # Simply continue; don't set current_image to None here

    if submit_received:
        if selected_images:
            if selected_overlay:
                current_image = overlay_images(current_image, selected_overlay)
                screen.fill((0, 0, 0))
                screen.blit(current_image, (0, 0))
            save_selections(selected_images)
            ser.write(b'LOCKOUT\n')
            submit_received = False

    if current_image:  # Always display the last known good image
        screen.fill((0, 0, 0))
        screen.blit(current_image, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                running = False
                # Exit fullscreen mode before quitting
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    time.sleep(0.1)

if ser.is_open:
    ser.close()
pygame.quit()
sys.exit()
