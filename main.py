import board
import busio
import usb_midi

import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from digitalio import DigitalInOut, Direction

from keyboard import Keyboard

# Pull CS pin low to enable level shifter
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0

# Set up APA102 pixels
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.5, auto_write=True)

# Set up I2C for IO expander (addr: 0x20)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)

# Set USB MIDI up on channel 0
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# List to store the button states
held = [0] * num_pixels

# Load the scales
scales = []
with open ("scales.csv", "r") as file:
    for line in file:
        row = line.strip().split(',')
        scales.append(row[0])

# Define the config buttons
config = [0, 4, 8, 12]

# Initialise the keyboard
keyboard = Keyboard(scales[0], num_pixels - len(config))

# Define the note button mapping
button_to_note = {15:0, 14:1, 13:2, 11:3, 10:4, 9:5, 7:6, 6:7, 5:8, 3:9, 2:10, 1:11}

# Colours
CONFIG_OFF = (15, 30, 27)
CONFIG_ON  = (126, 247, 229)
NOTE_OFF = (30, 30, 20)
NOTE_ON  = (255, 247, 161)

# Keep reading button states, setting pixels, sending notes
while True:
    with device:
        # Read from IO expander, 2 bytes (8 bits) correspond to the 16 buttons
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8

        # Loop through the buttons
        for i in range(num_pixels):
            # Pressed state
            if not (1 << i) & b:
                if i in config:
                    pixels[i] = CONFIG_ON
                    print("Config button pressed")
                else:
                    pixels[i] = NOTE_ON
                    if not held[i]:
                        # If not already held, then send note
                        midi.send(NoteOn(keyboard.notes[button_to_note[i]].value, 100))
                    
                held[i] = 1
            
            # Released state
            else:
                if i in config:
                    pixels[i] = CONFIG_OFF
                else:
                    pixels[i] = NOTE_OFF
                    
                    if held[i]:
                        # If not held any longer, send note off
                        midi.send(NoteOff(keyboard.notes[button_to_note[i]].value, 0))
                        # Set held state to off
                        held[i] = 0  
