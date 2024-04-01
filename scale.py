class Scale:
    def __init__(self, scale, root):
        self.root = root
        self.scale = scale

    def get_notes(self, num_notes):
        generated = 0
        current_note = self.root
        notes = [current_note]

        # Use intervals to generate notes in the scale
        while generated < 2 * num_notes:
            for interval in self.scale:
                new_note = current_note.modulate(interval)
                notes.append(new_note)
                current_note = new_note
                generated += 1
                
                if generated >= 2 * num_notes:
                    break

        return notes