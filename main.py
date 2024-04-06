import board
import busio

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

# List to store the button states
held = [0] * num_pixels

# Define the config buttons
config = [0, 4, 8, 12]

# Initialise the keyboard
keyboard = Keyboard(num_pixels - len(config))

# Define the note button mapping
button_to_note = {15:0, 14:1, 13:2, 11:3, 10:4, 9:5, 7:6, 6:7, 5:8, 3:9, 2:10, 1:11}

# Define the config button mapping
config_to_function = {
    12: keyboard.set_next_scale,
    8: keyboard.modulate_up_one,
    4: keyboard.modulate_up_octave,
    0: keyboard.set_next_extension,
}

# Colours
CONFIG_OFF = (15, 30, 27)
CONFIG_ON  = (126, 247, 229)
NOTE_OFF = (30, 30, 20)
NOTE_ON  = (255, 247, 161)
ROOT_OFF = (30, 15, 20)
ROOT_ON = (250, 125, 202)
            
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
                # Config buttons change the state of the keyboard
                if i in config:
                    pixels[i] = CONFIG_ON

                    if not held[i]:
                        # Send NoteOff to any held notes during state change
                        for j, state in enumerate(held):
                            if j not in config and state == 1:
                                keyboard.turnOff(button_to_note[j])
                        
                        function = config_to_function[i]
                        function()
                else:
                    if keyboard.keys[button_to_note[i]][0].get_letter() == keyboard._root.get_letter():
                        pixels[i] = ROOT_ON
                    else:
                        pixels[i] = NOTE_ON

                    if not held[i]:
                        # If not already held, then send note
                        keyboard.turnOn(button_to_note[i])
                    
                held[i] = 1
            
            # Released state
            else:
                if i in config:
                    pixels[i] = CONFIG_OFF
                else:
                    if keyboard.keys[button_to_note[i]][0].get_letter() == keyboard._root.get_letter():
                        pixels[i] = ROOT_OFF
                    else:
                        pixels[i] = NOTE_OFF

                    if held[i]:
                        # If not held any longer, send note off
                        keyboard.turnOff(button_to_note[i])
            
                # Set held state to off
                held[i] = 0

        time.sleep(0.01)
