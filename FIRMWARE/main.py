# main.py  - KMK firmware for your MicroPad (XIAO RP2040)
# Matrix: rows [GP1, GP2, GP26]  (3 rows)
#         cols [GP27, GP28, GP29, GP0] (4 cols)
# Encoder: A -> GP4, B -> GP3, C -> GND
# OLED:   SDA -> GP6, SCL -> GP7, VCC -> 3V3, GND -> GND

import board
import busio
import time

# KMK imports
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

# Matrix scanning helpers (may vary slightly between KMK versions)
# If you get ImportError here, tell me the error text and I'll adjust.
from kmk.scanners.keypad import MatrixScanner, DiodeOrientation

# Encoder module
from kmk.modules.encoder import EncoderHandler

# Optional: SSD1306 OLED (Adafruit library)
# Requires adafruit_ssd1306 and adafruit_bus_device in /lib on CIRCUITPY
try:
    import adafruit_ssd1306
    from kmk.extensions.oled import OledDisplay  # KMK sometimes provides a wrapper
    HAVE_OLED = True
except Exception:
    # If these imports fail it's safe — OLED will simply be disabled.
    HAVE_OLED = False

# === Create keyboard instance ===
keyboard = KMKKeyboard()

# === Matrix pins ===
# Rows (inputs), Columns (outputs) — match your schematic
ROW_PINS = [board.GP1, board.GP2, board.GP26]
COL_PINS = [board.GP27, board.GP28, board.GP29, board.GP0]

# Diode orientation: change if your diodes point the other way.
# Common values: DiodeOrientation.COL2ROW or DiodeOrientation.ROW2COL
diode = DiodeOrientation.COL2ROW

# Attach the matrix scanner to the keyboard
# (MatrixScanner API is common; if your KMK version uses a different class
# you'll get an ImportError — tell me the message and I'll update it.)
keyboard.matrix = MatrixScanner(row_pins=ROW_PINS, col_pins=COL_PINS, diode_orientation=diode)

# === Encoder setup ===
encoder = EncoderHandler()
# pins: tuple of (A_pin, B_pin, Switch_pin_or_None). You can add multiple encoders as additional tuples
encoder.pins = ((board.GP4, board.GP3, None),)
# Default encoder actions — map encoder turns to media keys (volume)
# If you want different behavior change to KC.VOLD / KC.VOLU or arrow scroll, etc.
# EncoderHandler typically uses encoder.handler_map or similar; KMK encoder API varies.
# We'll use the common simple pattern:
try:
    # Some KMK versions allow a "map" property; others need binding via modules. This is a best-effort.
    encoder.map = ((KC.VOLD, KC.VOLU, None),)
except Exception:
    # If this fails it's non-fatal; encoder will still send events that you can handle later.
    pass

keyboard.modules.append(encoder)

# === Keymap ===
# 3 rows × 4 cols = 12 keys. Order is row-major: row0 cols0..3, row1 cols0..3, row2 cols0..3
# Edit these KC.* entries to whatever you want.
keyboard.keymap = [
    # layer 0
    [
        KC.ESC,  KC.Q,    KC.W,    KC.E,    # row 0, cols 0..3
        KC.A,    KC.S,    KC.D,    KC.F,    # row 1
        KC.Z,    KC.X,    KC.C,    KC.V,    # row 2
    ]
]

# If you prefer a clearer nested layout (3 rows of 4), KMK accepts flat arrays mapped to the matrix:
# keyboard.coord_mapping = [ 0,1,2,3, 4,5,6,7, 8,9,10,11 ]
# (Usually only needed for funky handwires — KMK will default to row-major.)

# === OLED initialization (optional) ===
if HAVE_OLED:
    try:
        i2c = busio.I2C(board.GP7, board.GP6)  # SCL, SDA as you specified
        # Common SSD1306 sizes: 128x64 or 128x32. Change height if yours is 32.
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        # If KMK provides a small OledDisplay extension, register it:
        try:
            oled_display = OledDisplay(oled)
            keyboard.extensions.append(oled_display)
        except Exception:
            # If KMK doesn't have OledDisplay wrapper, just keep the raw display:
            pass

        # Draw a small startup message
        try:
            oled.fill(0)
            oled.text("MicroPad", 0, 0)
            oled.text("Layer: 0", 0, 12)
            oled.show()
        except Exception:
            pass

    except Exception as e:
        # If I2C init fails, continue without OLED but inform via REPL
        print("OLED init failed:", e)

# === Start KMK ===
if __name__ == "__main__":
    keyboard.go()
