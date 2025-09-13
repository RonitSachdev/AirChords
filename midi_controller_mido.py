import mido
import time
from typing import List, Dict, Optional
import threading

class MIDIController:
    def __init__(self, device_name: Optional[str] = None):
        """Initialize MIDI controller using mido"""
        self.device_name = device_name
        self.outport = None
        self.current_notes = set()  # Track currently playing notes
        self.velocity = 100  # Default velocity
        self.channel = 0  # MIDI channel (0-15)
        
        # Default chord configurations (MIDI note numbers)
        self.default_chords = {
            1: [60, 64, 67],        # C Major (C, E, G)
            2: [62, 66, 69],        # D Minor (D, F, A)
            3: [64, 68, 71],        # E Minor (E, G, B)
            4: [65, 69, 72],        # F Major (F, A, C)
            5: [67, 71, 74]         # G Major (G, B, D)
        }
        
        self.chords = self.default_chords.copy()
        
    def list_devices(self) -> Dict[int, str]:
        """List available MIDI output devices"""
        devices = {}
        output_names = mido.get_output_names()
        
        for i, name in enumerate(output_names):
            devices[i] = name
                
        return devices
    
    def connect(self, device_id: Optional[int] = None) -> bool:
        """Connect to MIDI output device"""
        try:
            devices = self.list_devices()
            
            if device_id is None or device_id not in devices:
                # Try to find a default device
                if not devices:
                    print("No MIDI output devices found")
                    return False
                device_id = list(devices.keys())[0]
            
            device_name = devices[device_id]
            self.outport = mido.open_output(device_name)
            self.device_name = device_name
            print(f"Connected to MIDI device: {device_name}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to MIDI device: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MIDI device"""
        if self.outport:
            self.stop_all_notes()
            self.outport.close()
            self.outport = None
            print("MIDI device disconnected")
    
    def note_on(self, note: int, velocity: int = None):
        """Send MIDI note on message"""
        if not self.outport:
            print("MIDI not connected - cannot send note on")
            return
        
        if velocity is None:
            velocity = self.velocity
        
        # Ensure note is off first to avoid stuck notes
        if note in self.current_notes:
            msg_off = mido.Message('note_off', channel=self.channel, note=note, velocity=0)
            self.outport.send(msg_off)
            time.sleep(0.001)  # Small delay
            
        msg = mido.Message('note_on', channel=self.channel, note=note, velocity=velocity)
        self.outport.send(msg)
        self.current_notes.add(note)
        # print(f"MIDO Note ON: {note} ({self.note_to_name(note)}) vel={velocity}")
    
    def note_off(self, note: int):
        """Send MIDI note off message"""
        if not self.outport:
            print("MIDI not connected - cannot send note off")
            return
            
        msg = mido.Message('note_off', channel=self.channel, note=note, velocity=0)
        self.outport.send(msg)
        self.current_notes.discard(note)
        # print(f"MIDO Note OFF: {note} ({self.note_to_name(note)})")
    
    def play_chord(self, chord_number: int, duration: float = None):
        """Play a chord based on gesture number (1-5)"""
        if not self.outport:
            print("MIDI not connected - cannot play chord")
            return
            
        if chord_number not in self.chords:
            print(f"Chord {chord_number} not configured")
            return
        
        chord = self.chords[chord_number]
        # print(f"MIDO Playing chord {chord_number}: {chord}")
        
        # Play all notes in the chord
        for note in chord:
            try:
                self.note_on(note, self.velocity)
            except Exception as e:
                print(f"Error playing note {note}: {e}")
        
        # If duration is specified, stop notes after duration
        if duration:
            def stop_chord():
                time.sleep(duration)
                for note in chord:
                    self.note_off(note)
            
            thread = threading.Thread(target=stop_chord)
            thread.daemon = True
            thread.start()
    
    def stop_chord(self, chord_number: int):
        """Stop playing a chord"""
        if not self.outport:
            print("MIDI not connected - cannot stop chord")
            return
            
        if chord_number not in self.chords:
            return
        
        chord = self.chords[chord_number]
        # print(f"MIDO Stopping chord {chord_number}: {chord}")
        
        for note in chord:
            try:
                self.note_off(note)
            except Exception as e:
                print(f"Error stopping note {note}: {e}")
    
    def stop_all_notes(self):
        """Stop all currently playing notes"""
        if not self.outport:
            return
            
        # print("MIDO Stopping all notes")
        for note in list(self.current_notes):
            self.note_off(note)
        
        # Send All Notes Off message as well
        msg = mido.Message('control_change', channel=self.channel, control=123, value=0)
        self.outport.send(msg)
    
    def set_chord(self, chord_number: int, notes: List[int]):
        """Set custom chord configuration"""
        if 1 <= chord_number <= 5:
            self.chords[chord_number] = notes.copy()
    
    def get_chord(self, chord_number: int) -> List[int]:
        """Get chord configuration"""
        return self.chords.get(chord_number, [])
    
    def get_all_chords(self) -> Dict[int, List[int]]:
        """Get all chord configurations"""
        return self.chords.copy()
    
    def reset_to_defaults(self):
        """Reset chords to default configurations"""
        self.chords = self.default_chords.copy()
    
    def set_velocity(self, velocity: int):
        """Set MIDI velocity (0-127)"""
        self.velocity = max(0, min(127, velocity))
    
    def set_channel(self, channel: int):
        """Set MIDI channel (0-15)"""
        self.channel = max(0, min(15, channel))

    @staticmethod
    def note_to_name(note: int) -> str:
        """Convert MIDI note number to note name"""
        if note < 0 or note > 127:
            return "Invalid"
        
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        note_name = notes[note % 12]
        return f"{note_name}{octave}"
    
    @staticmethod
    def name_to_note(note_name: str) -> int:
        """Convert note name to MIDI note number"""
        notes = {'C': 0, 'C#': 1, 'DB': 1, 'D': 2, 'D#': 3, 'EB': 3, 'E': 4, 
                'F': 5, 'F#': 6, 'GB': 6, 'G': 7, 'G#': 8, 'AB': 8, 'A': 9, 
                'A#': 10, 'BB': 10, 'B': 11}
        
        # Parse note name (e.g., "C4", "F#3")
        if len(note_name) < 2:
            return -1
        
        note_part = note_name[:-1].upper()
        try:
            octave_part = int(note_name[-1])
        except ValueError:
            return -1
        
        if note_part not in notes:
            return -1
        
        return (octave_part + 1) * 12 + notes[note_part]

def test_mido_controller():
    """Test function for mido MIDI controller"""
    controller = MIDIController()
    
    # List available devices
    print("Available MIDI devices:")
    devices = controller.list_devices()
    for device_id, name in devices.items():
        print(f"  {device_id}: {name}")
    
    if not devices:
        print("No MIDI devices found. Testing without actual MIDI output.")
        return
    
    # Connect to first available device
    if controller.connect():
        print("Testing chord playback...")
        
        # Test each chord
        for i in range(1, 6):
            print(f"Playing chord {i}: {[controller.note_to_name(note) for note in controller.get_chord(i)]}")
            controller.play_chord(i, duration=1.0)
            time.sleep(1.5)
        
        controller.disconnect()
        print("MIDO MIDI test completed")
    else:
        print("Failed to connect to MIDI device")

if __name__ == "__main__":
    test_mido_controller()