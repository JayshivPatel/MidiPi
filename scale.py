class Scale:
    def __init__(self, scale, root):
        self.root = root.get_lowest_note()
        self.scale = scale

    def get_notes(self):
        current_note = self.root
        notes = [current_note]

        # Use intervals to generate notes in the scale
        while current_note.value < self.root.value + 72:
            for interval in self.scale:
                new_note = current_note.modulate(interval)
                notes.append(new_note)
                current_note = new_note

        return notes