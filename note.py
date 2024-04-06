class Note:
    # Names for debugging
    letters = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"] 
    
    def __init__(self, value):
        self.value = value
        
    def modulate(self, amount):
        return Note(self.value + amount)
        
    def name(self):
        octave = int(self.value / 12) - 2
        return self.get_letter() + str(octave)
    
    def get_letter(self):
        return self.letters[(self.value % 12)]
    
    def get_lowest_note(self):
        return Note((self.value % 12) + 36)
