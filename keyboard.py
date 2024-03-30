from scale import Scale
from note import Note

class Keyboard:
    def __init__(self, scale, num_notes):
        # Default root to C4
        self.root  = Note(60)
        self.num_notes = num_notes
        self.change_scale(scale)

    def change_scale(self, scale):
        self.scale = Scale(scale, self.root)
        self.notes = self.scale.get_notes(self.num_notes)
    
    def modulate(self, amount):
        self.root = self.root.modulate(amount)
        self.change_scale(self.scale)

    def modulate_up_one(self):
        self.modulate(1)

    def modulate_up_octave(self):
        self.modulate(12)