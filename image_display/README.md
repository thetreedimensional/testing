
### Setup and Cloning the Repository
1. **Clone the Repository:**
   ```bash
   rm -rf atlas-axiom
   git clone https://github.com/TyGuy/atlas-axiom/
   cd atlas-axiom/image-display
   ```

2. **Serial Port Configuration:**
   - Ensure the serial port is configured correctly in the script:
     ```python
     serial_port = '/dev/ttyACM0'  # Replace with the appropriate serial port
     baud_rate = 9600
     ```

3. **Burn Pi Credentials:**
   - Verify the credentials for the Burn Pi:
     ```python
     target_ip = '10.0.0.63'
     target_user = 'pi'
     target_pass = 'raspberry'
     ```

4. **Image Files:**
   - Ensure the images listed in the `image_files` dictionary are located in the `for_display_blue` directory in the same folder as the script:
     ```python
     image_files = {
         1: "Gear.png",
         2: "Boat.png",
         # Add all other image files here
     }
     ```

### Running the Script
1. **Navigate to the Script Directory:**
   ```bash
   cd atlas-axiom/image-display
   ```

2. **Execute the Script:**
   ```bash
   python3 image_display.py
   ```

### Other Versions of the Script:
- **`image_display_k.py`:** 
  - Works with keyboard input. Use the following commands:
    - Press `O` (capital O) to start.
    - Enter numbers `1-16` followed by `Enter` to select images.
    - To overlay more images, enter another number.
    - Press `R` to clear the screen if you want to start over.
    - Press `S` to submit your selection. You can submit even after entering just one number.

- **`image_display_t.py`:** 
  - A test file that uses serial input. Adjust debounce time (line 8) as needed:
    ```python
    DEBOUNCE = 0.1  # Start with 0.1 seconds, adjust as needed
    ```

### How the Script Works:
1. **Pygame Initialization:**
   - The script initializes Pygame, opens a fullscreen window, and matches the screen resolution.

2. **Serial Communication:**
   - Continuously listens to the serial port for incoming data, processing commands to display images.

3. **Image Display:**
   - Loads, scales, and displays images. Supports overlaying images and adding a "selected" overlay before submission.

4. **File Transfer:**
   - Upon receiving the `SUBMIT` command, selected image identifiers are saved to `selections.txt` and transferred to the remote machine using `scp`.

5. **Remote File Handling:**
   - Waits for the Burn Pi to handle `user_selection.txt` under the `/State/` directory before allowing further input.
