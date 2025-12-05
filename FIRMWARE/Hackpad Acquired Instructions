Once my MicroPad arrives, these are the steps I will follow on my end to set up the firmware and get everything running.

1. Flash CircuitPython
After I receive the board, I will hold the BOOT/RESET button while plugging it in. A drive named RPI-RP2 will appear. 
I will download the correct CircuitPython UF2 file from circuitpython.org and drag it onto the RPI-RP2 drive. 
The board will reboot into a new drive called CIRCUITPY.

2. Install OLED Driver Libraries
Since the MicroPad uses a 0.91-inch SSD1306 I2C OLED display, I will add the required CircuitPython libraries into the CIRCUITPY/lib folder.

The files I will install are:
- adafruit_ssd1306.mpy
- adafruit_framebuf.mpy (if needed)
- the adafruit_bus_device folder
These will come from the official Adafruit CircuitPython bundle.

3. Expected File Layout
When everything is installed, the CIRCUITPY drive will look like this:
CIRCUITPY/
- main.py
- kmk/
- lib/
  - adafruit_ssd1306.mpy
  - adafruit_framebuf.mpy
  - adafruit_bus_device/

4. Pin Assignments I Will Use in Firmware
Matrix rows: GPIO1, GPIO2, GPIO26
Matrix columns: GPIO27, GPIO28, GPIO29, GPIO0
(12 keys total, using one diode per switch)

Rotary encoder:
- A → GPIO4
- B → GPIO3
- C → GND

OLED display:
- GND → GND
- VCC → 3V3
- SDA → GPIO6
- SCL → GPIO7
These pins will be defined in my main.py.

5. Load My Custom Firmware
After copying all files, I will place my main.py in the CIRCUITPY root. 
The board will reboot automatically and begin running the KMK firmware with my keymap, rotary encoder, and OLED display.

6. Final Testing
Once the firmware is loaded, I will test all 12 keys, verify encoder rotation, and confirm the OLED initializes properly. 
After these checks, the MicroPad will be fully ready to use.
