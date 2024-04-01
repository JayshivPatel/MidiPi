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
            data = json.load(file)["scales"]
            for scale_name, intervals in data:
                self._scales.append([scale_name, intervals])

        # Default to note only
        self._chord = 0
        # Read extension information from JSON
        self._extensions = []
        with open ("chords.json", "r") as file:
            data = json.load(file)["chords"]
            for chord_name, intervals in data:
                self._extensions.append([chord_name, intervals])
        
        self._change_scale(self.get_current_scale())

    def _change_scale(self, scale):
        # Regenerates keys
        notes = Scale(scale, self._root).get_notes(self.num_notes)
        self.keys = self.extend(notes, self._extensions[self._chord][1])

    def set_next_scale(self):
        # Set next scale in JSON
        self._scale = (self._scale + 1) % len(self._scales)
        self._change_scale(self.get_current_scale())
    
    def _modulate(self, amount):
        # Modulate root and regenerate keys
        self._root = self._root.modulate(amount)
        self._change_scale(self.get_current_scale())

    def get_current_scale(self):
        return self._scales[self._scale][1]

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

    def extend(self, notes, extensions):
        chords = []
        for i in range(self.num_notes):
            chords.append([notes[i]])
            
        for i in range(self.num_notes):
            for extension in extensions:
                chords[i].append(notes[i + extension])
        return chords

    def set_next_extension(self):
        # Set next extension in JSON
        self._chord = (self._chord + 1) % len(self._extensions)
        self._change_scale(self.get_current_scale())
