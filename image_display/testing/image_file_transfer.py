import random
import subprocess

# Function to collect user input for numbers
def get_user_numbers():
    selected_numbers = []
    while len(selected_numbers) < 3:
        try:
            # Get input from the user
            user_input = input(f"Enter a number between 0 and 15 ({3 - len(selected_numbers)} left): ")
            if user_input.strip() == '':
                if len(selected_numbers) > 0:
                    print("Input completed manually.")
                    break
                else:
                    print("You must select at least one number.")
                    continue
            
            # Convert to integer and validate the number
            number = int(user_input)
            if number < 0 or number > 15:
                print("Number out of range. Please enter a number between 0 and 15.")
            elif number in selected_numbers:
                print("Number already selected. Please choose a different number.")
            else:
                selected_numbers.append(number)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return selected_numbers

# Collect numbers from user input
selected_numbers = get_user_numbers()

# Write the selected numbers to a text file
file_path = 'user_selections.txt'
with open(file_path, 'w') as file:
    for number in selected_numbers:
        file.write(f"{number}\n")

# image pi credentials:
source_ip = '10.0.0.190'
source_user = 'bug'
source_pass = 'bugcat'

# Define the target machine's IP, target_user, and destination path
target_ip = '10.0.0.63'  # Change to your target IP
target_user = 'pi'  # Change to your target target_user
target_pass = 'raspberry'  # Change to your target target_pass
destination_path = f'/home/{target_user}/atlas/state/user_selections.txt'

# Use SCP to transfer the file
scp_command = f"scp {file_path} {target_user}@{target_ip}:{destination_path}"

# Run the SCP command and check if it was successful
result = subprocess.run(['sshpass', '-p', target_pass, 'scp', file_path, f'{target_user}@{target_ip}:{destination_path}'], capture_output=True)

# sshpass -p raspberry scp user_selections.txt pi@10.0.0.63:/home/pi/depthai-python/atax/atax_v1/user_selections.txt

# Check if the file transfer was successful
if result.returncode == 0:
    print("File transfer successful.")
    # Optional: Verify the file on the target machine
    verify_command = f"sshpass -p {target_pass} ssh {target_user}@{target_ip} 'test -f {destination_path}'"
    verify_result = subprocess.run(verify_command, shell=True)
    if verify_result.returncode == 0:
        print("File presence confirmed on the target machine.")
    else:
        print("File not found on the target machine.")
else:
    print("File transfer failed.")
    print(result.stderr.decode('utf-8'))