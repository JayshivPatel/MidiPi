class Note:
    # Names for debugging
    letters = ["C", "C#", "D", "Eb", "E", "F", "F#", "Ab", "A", "Bb", "B"] 
    
    def __init__(self, value):
        self.value = value
        
    def modulate(self, amount):
        return Note(self.value + amount)
        
    def name(self):
        octave = int(self.value / 12)
        letter = self.value % 12

        return self.letters[letter] + str(octave)