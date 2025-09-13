import tkinter as tk
from tkinter import Canvas
from typing import Set, Callable, Optional, Dict
from midi_controller import MIDIController

class PianoRoll(Canvas):
    """Interactive piano keyboard widget for chord editing"""
    
    def __init__(self, parent, width=800, height=200, start_note=21, end_note=108, **kwargs):
        super().__init__(parent, width=width, height=height, bg='white', **kwargs)
        
        self.start_note = start_note  # A0 (MIDI note 21)
        self.end_note = end_note      # C8 (MIDI note 108)
        self.width = width
        self.height = height
        
        # Note states
        self.selected_notes: Set[int] = set()
        self.highlighted_notes: Set[int] = set()
        
        # Visual properties
        self.white_key_color = '#FFFFFF'
        self.black_key_color = '#000000'
        self.selected_color = '#FF4444'
        self.highlighted_color = '#4444FF'
        self.border_color = '#CCCCCC'
        
        # Callback for note selection changes
        self.on_note_change: Optional[Callable[[Set[int]], None]] = None
        
        # Key dimensions
        self.white_key_width = 0
        self.white_key_height = height - 20
        self.black_key_width = 0
        self.black_key_height = height * 0.6
        
        # Note layout
        self.white_notes = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B
        self.black_notes = [1, 3, 6, 8, 10]        # C#, D#, F#, G#, A#
        
        # Key rectangles for click detection
        self.key_rects: Dict[int, tuple] = {}
        
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        
        self.draw_keyboard()
    
    def calculate_key_positions(self):
        """Calculate positions and sizes of piano keys"""
        # Count white keys in the range
        white_key_count = 0
        for note in range(self.start_note, self.end_note + 1):
            if (note % 12) in self.white_notes:
                white_key_count += 1
        
        self.white_key_width = (self.width - 40) / white_key_count if white_key_count > 0 else 20
        self.black_key_width = self.white_key_width * 0.6
    
    def is_black_key(self, note: int) -> bool:
        """Check if a MIDI note is a black key"""
        return (note % 12) in self.black_notes
    
    def get_key_position(self, note: int) -> tuple:
        """Get the x, y, width, height of a key"""
        if note < self.start_note or note > self.end_note:
            return (0, 0, 0, 0)
        
        # Calculate white key index
        white_key_index = 0
        for n in range(self.start_note, note + 1):
            if (n % 12) in self.white_notes:
                if n < note:
                    white_key_index += 1
        
        x = 20 + white_key_index * self.white_key_width
        
        if self.is_black_key(note):
            # Black key positioning
            note_in_octave = note % 12
            if note_in_octave == 1:  # C#
                x -= self.black_key_width * 0.5
            elif note_in_octave == 3:  # D#
                x += self.white_key_width - self.black_key_width * 0.5
            elif note_in_octave == 6:  # F#
                x += self.white_key_width - self.black_key_width * 0.5
            elif note_in_octave == 8:  # G#
                x += self.white_key_width * 2 - self.black_key_width * 0.5
            elif note_in_octave == 10:  # A#
                x += self.white_key_width * 3 - self.black_key_width * 0.5
            
            return (x, 10, self.black_key_width, self.black_key_height)
        else:
            # White key
            return (x, 10, self.white_key_width, self.white_key_height)
    
    def draw_keyboard(self):
        """Draw the piano keyboard"""
        self.delete('all')
        self.calculate_key_positions()
        self.key_rects.clear()
        
        # Draw white keys first
        for note in range(self.start_note, self.end_note + 1):
            if not self.is_black_key(note):
                self.draw_key(note)
        
        # Draw black keys on top
        for note in range(self.start_note, self.end_note + 1):
            if self.is_black_key(note):
                self.draw_key(note)
    
    def draw_key(self, note: int):
        """Draw a single piano key"""
        x, y, width, height = self.get_key_position(note)
        
        if width <= 0 or height <= 0:
            return
        
        # Determine key color
        base_color = self.black_key_color if self.is_black_key(note) else self.white_key_color
        
        # Apply state colors
        if note in self.selected_notes:
            color = self.selected_color
        elif note in self.highlighted_notes:
            color = self.highlighted_color
        else:
            color = base_color
        
        # Draw key
        key_id = self.create_rectangle(
            x, y, x + width, y + height,
            fill=color, outline=self.border_color, width=1
        )
        
        # Store key rectangle for click detection
        self.key_rects[note] = (x, y, x + width, y + height)
        
        # Add note label for C notes
        if note % 12 == 0 and not self.is_black_key(note):
            octave = (note // 12) - 1
            self.create_text(
                x + width/2, y + height - 15,
                text=f'C{octave}', font=('Arial', 8), fill='gray'
            )
    
    def get_note_at_position(self, x: int, y: int) -> Optional[int]:
        """Get the MIDI note at the given screen position"""
        # Check black keys first (they're on top)
        for note in range(self.start_note, self.end_note + 1):
            if self.is_black_key(note):
                rect = self.key_rects.get(note)
                if rect and rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                    return note
        
        # Check white keys
        for note in range(self.start_note, self.end_note + 1):
            if not self.is_black_key(note):
                rect = self.key_rects.get(note)
                if rect and rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                    return note
        
        return None
    
    def on_click(self, event):
        """Handle mouse click on piano key"""
        note = self.get_note_at_position(event.x, event.y)
        if note is not None:
            self.toggle_note(note)
    
    def on_drag(self, event):
        """Handle mouse drag across piano keys"""
        note = self.get_note_at_position(event.x, event.y)
        if note is not None and note not in self.selected_notes:
            self.add_note(note)
    
    def toggle_note(self, note: int):
        """Toggle a note's selection state"""
        if note in self.selected_notes:
            self.remove_note(note)
        else:
            self.add_note(note)
    
    def add_note(self, note: int):
        """Add a note to selection"""
        if note not in self.selected_notes:
            self.selected_notes.add(note)
            self.draw_key(note)
            self.notify_change()
    
    def remove_note(self, note: int):
        """Remove a note from selection"""
        if note in self.selected_notes:
            self.selected_notes.remove(note)
            self.draw_key(note)
            self.notify_change()
    
    def set_selected_notes(self, notes: Set[int], notify: bool = True):
        """Set the selected notes"""
        self.selected_notes = notes.copy()
        self.draw_keyboard()
        if notify:
            self.notify_change()
    
    def get_selected_notes(self) -> Set[int]:
        """Get the currently selected notes"""
        return self.selected_notes.copy()
    
    def set_highlighted_notes(self, notes: Set[int]):
        """Set notes to highlight (for preview)"""
        self.highlighted_notes = notes.copy()
        self.draw_keyboard()
    
    def clear_selection(self):
        """Clear all selected notes"""
        self.selected_notes.clear()
        self.draw_keyboard()
        self.notify_change()
    
    def notify_change(self):
        """Notify callback of selection change"""
        if self.on_note_change:
            self.on_note_change(self.selected_notes.copy())
    
    def play_selected_notes(self, midi_controller: MIDIController, duration: float = 1.0):
        """Play the currently selected notes"""
        for note in self.selected_notes:
            midi_controller.note_on(note)
        
        # Schedule note off
        self.after(int(duration * 1000), lambda: self.stop_selected_notes(midi_controller))
    
    def stop_selected_notes(self, midi_controller: MIDIController):
        """Stop playing the currently selected notes"""
        for note in self.selected_notes:
            midi_controller.note_off(note)

def test_piano_roll():
    """Test function for piano roll widget"""
    root = tk.Tk()
    root.title("Piano Roll Test")
    root.geometry("900x300")
    
    # Create piano roll
    piano = PianoRoll(root, width=850, height=200)
    piano.pack(pady=20)
    
    # Add some test functionality
    def on_note_change(notes):
        note_names = [MIDIController.note_to_name(note) for note in sorted(notes)]
        print(f"Selected notes: {note_names}")
    
    piano.on_note_change = on_note_change
    
    # Test buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Clear", 
              command=piano.clear_selection).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="C Major", 
              command=lambda: piano.set_selected_notes({60, 64, 67})).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="Highlight C Major", 
              command=lambda: piano.set_highlighted_notes({60, 64, 67})).pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_piano_roll()