class Scale:
    def __init__(self, scale, root):
        self.root = root
        with open("scales.csv", "r") as file:
            for line in file:
                row = line.strip().split(',')
                name = row[0]
                intervals = row[1:]
                if scale == name:    
                    self.scale = [int(interval) for interval in intervals]

    def get_notes(self, num_notes):
        generated = 0
        current_note = self.root
        notes = [current_note]

        while generated < num_notes:
            for interval in self.scale:
                new_note = current_note.modulate(interval)
                notes.append(new_note)
                current_note = new_note
                generated += 1
                
                if generated >= num_notes:
                    break

        return notes
