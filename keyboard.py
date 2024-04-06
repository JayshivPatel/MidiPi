from scale import Scale
from note import Note
import usb_midi

import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import json

class Keyboard:
    def __init__(self, num_notes):
        # Default root to C1
        self._root  = Note(36)
        self._octave = 1
        self._semitone = 1
        # Default to first scale
        self._scale = 0
        self.num_notes = num_notes
        # Set default USB MIDI out for direct playback
        self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        self.notes = []
        self.keys = []

        # Read scale information from JSON
        self._scales = []
        with open ("scales.json", "r") as file:
            data = json.load(file)["scales"]
            for scale_name, intervals in data:
                self._scales.append([scale_name, intervals])

        # Default to note only
        self._extension = 0
        # Read extension information from JSON
        self._extensions = []
        with open ("chords.json", "r") as file:
            data = json.load(file)["chords"]
            for chord_name, intervals in data:
                self._extensions.append([chord_name, intervals])
        
        self._regenerate_notes(self.get_current_scale())

    def _set_keys(self):
        self.keys = []
        for i in range(self.num_notes):
            self.keys.append([self.notes[i + (self._octave - 1) * (len(self.get_current_scale()))]])
        
        for i in range(self.num_notes):
            for extension in self._extensions[self._extension][1]:
                if self._root.value + extension + self._get_octave_offset() >= 36 and self._root.value + extension + self._get_octave_offset() <= 119:
                    self.keys[i].append(self.notes[i + extension + self._get_octave_offset()])

    def _get_octave_offset(self):
        return (self._octave - 1) * len(self.get_current_scale())

    def _regenerate_notes(self, scale):
        self.notes = Scale(scale, self._root).get_notes()
        self._set_keys()

    def set_next_scale(self):
        # Set next scale in JSON
        self._scale = (self._scale + 1) % len(self._scales)
        self._regenerate_notes(self.get_current_scale())
    
    def _modulate(self, amount):
        # Modulate root and regenerate keys
        self._root = self._root.modulate(amount)
        self._regenerate_notes(self.get_current_scale())

    def get_current_scale(self):
        return self._scales[self._scale][1]
    
    def get_current_scale_name(self):
        return self._scales[self._scale][0]

    def modulate_up_one(self):
        # Loop back once octave hit
        if self._semitone == 12:
            self._modulate(-11)
            self._semitone = 1
        else:
            self._modulate(1)
            self._semitone += 1

    def modulate_up_octave(self):
        # Loop back once at top of keyboard
        if self._octave == 4:
            self._octave = 1
        else:    
            self._octave += 1
        self._set_keys()

    def set_next_extension(self):
        # Set next extension in JSON
        self._extension = (self._extension + 1) % len(self._extensions)
        self._set_keys()

    # Send NoteOn NoteOff MIDI signals
    def turnOn(self, key):
        notes = self.keys[key]
        for note in notes:
            self.midi.send(NoteOn(note.value, 100))

    def turnOff(self, key):
        notes = self.keys[key]
        for note in notes:
            self.midi.send(NoteOff(note.value, 0))