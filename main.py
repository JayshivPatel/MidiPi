import board
import busio
import usb_midi

import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from digitalio import DigitalInOut, Direction

from scale import Scale

# Pull CS pin low to enable level shifter
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0

# Set up APA102 pixels
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=1.0, auto_write=True)

# Set up I2C for IO expander (addr: 0x20)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)

# Set USB MIDI up on channel 0
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Function to map 0-255 to position on colour wheel
def colourwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

# List to store the button states
held = [0] * num_pixels

scale = Scale("minor_harmonic")
notes = scale.get_notes(num_pixels)

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
            if not (1 << i) & b:  # Pressed state
                pixels[i] = colourwheel(i * num_pixels)  # Map pixel index to 0-255 range
                if not held[i]:
                    midi.send(NoteOn(notes[15 - i].value, 100))  # If not already held, then send note
                held[i] = 1
            else:  # Released state
                if held[i]:
                    pixels[i] = (0, 0, 0)  # Turn pixel off
                    midi.send(NoteOff(notes[15 - i].value, 0))  # If not held, send note off
                    held[i] = 0  # Set held state to off