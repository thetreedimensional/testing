import random
import subprocess

# Collect numbers from user input
selected_numbers = [3, 12, 0]

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