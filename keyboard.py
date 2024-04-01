from scale import Scale
from note import Note
import json

class Keyboard:
    def __init__(self, num_notes):
        # Default root to C3
        self._root  = Note(60)
        self._octave = 3
        self._semitone = 1
        # Default to first scale
        self._scale = 0
        self.num_notes = num_notes
        # Read scale information from JSON
        self._scales = []
        with open ("scales.json", "r") as file:
            data = json.load(file)
            for name in data:
                self._scales.append([name, data[name]])
        
        self._change_scale(self._scales[self._scale][1])


    def _change_scale(self, scale):
        # Regenerates keys
        self.notes = Scale(scale, self._root)
        self.keys = self.notes.get_notes(self.num_notes)

    def set_next_scale(self):
        # Set next scale in JSON
        self._scale = (self._scale + 1) % len(self._scales)
        self._change_scale(self._scales[self._scale][1])
    
    def _modulate(self, amount):
        # Modulate root and regenerate keys
        self._root = self._root.modulate(amount)
        self._change_scale(self._scales[self._scale][1])

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
        if self._octave == 5:
            self._modulate(-4 * 12)
            self._octave = 1
        else:    
            self._modulate(12)
            self._octave += 1

