import json
import os
from typing import Dict, List, Any
from pathlib import Path

class ConfigManager:
    """Manages saving and loading of application configuration"""
    
    def __init__(self, config_file: str = "air_midi_config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "chords": {
                "1": [60, 64, 67],  # C Major
                "2": [62, 66, 69],  # D Minor
                "3": [64, 68, 71],  # E Minor
                "4": [65, 69, 72],  # F Major
                "5": [67, 71, 74]   # G Major
            },
            "midi_settings": {
                "device_id": None,
                "velocity": 100,
                "channel": 0
            },
            "gesture_settings": {
                "stability_threshold": 0.7,
                "history_length": 5,
                "camera_index": 0
            },
            "ui_settings": {
                "window_width": 1000,
                "window_height": 700,
                "piano_width": 900,
                "piano_height": 200
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_file.exists():
            return self.get_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Ensure all required keys exist
            default_config = self.get_default_config()
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if subkey not in config[key]:
                            config[key][subkey] = subvalue
            
            return config
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_chords(self) -> Dict[int, List[int]]:
        """Get chord configurations"""
        chords = {}
        for key, value in self.config["chords"].items():
            try:
                chord_num = int(key)
                if isinstance(value, list):
                    chords[chord_num] = value
            except (ValueError, TypeError):
                continue
        return chords
    
    def set_chord(self, chord_number: int, notes: List[int]):
        """Set chord configuration"""
        self.config["chords"][str(chord_number)] = notes
    
    def get_midi_settings(self) -> Dict[str, Any]:
        """Get MIDI settings"""
        return self.config["midi_settings"].copy()
    
    def set_midi_settings(self, **kwargs):
        """Set MIDI settings"""
        for key, value in kwargs.items():
            if key in self.config["midi_settings"]:
                self.config["midi_settings"][key] = value
    
    def get_gesture_settings(self) -> Dict[str, Any]:
        """Get gesture recognition settings"""
        return self.config["gesture_settings"].copy()
    
    def set_gesture_settings(self, **kwargs):
        """Set gesture recognition settings"""
        for key, value in kwargs.items():
            if key in self.config["gesture_settings"]:
                self.config["gesture_settings"][key] = value
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI settings"""
        return self.config["ui_settings"].copy()
    
    def set_ui_settings(self, **kwargs):
        """Set UI settings"""
        for key, value in kwargs.items():
            if key in self.config["ui_settings"]:
                self.config["ui_settings"][key] = value
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.get_default_config()
    
    def export_chords(self, filename: str) -> bool:
        """Export chord configurations to a separate file"""
        try:
            chords_data = {
                "chords": self.config["chords"],
                "exported_from": "Air MIDI Controller"
            }
            with open(filename, 'w') as f:
                json.dump(chords_data, f, indent=2)
            return True
        except IOError as e:
            print(f"Error exporting chords: {e}")
            return False
    
    def import_chords(self, filename: str) -> bool:
        """Import chord configurations from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if "chords" in data:
                # Validate chord data
                for key, value in data["chords"].items():
                    try:
                        chord_num = int(key)
                        if isinstance(value, list) and 1 <= chord_num <= 5:
                            # Validate MIDI notes
                            valid_notes = [note for note in value 
                                         if isinstance(note, int) and 0 <= note <= 127]
                            self.config["chords"][key] = valid_notes
                    except (ValueError, TypeError):
                        continue
                return True
            return False
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error importing chords: {e}")
            return False
    
    def get_config_summary(self) -> str:
        """Get a human-readable summary of the configuration"""
        from midi_controller import MIDIController
        
        summary = "Air MIDI Controller Configuration:\n\n"
        
        # Chords
        summary += "Chords:\n"
        for i in range(1, 6):
            chord = self.config["chords"].get(str(i), [])
            if chord:
                note_names = [MIDIController.note_to_name(note) for note in chord]
                summary += f"  Chord {i}: {note_names} (MIDI: {chord})\n"
            else:
                summary += f"  Chord {i}: Not set\n"
        
        # MIDI Settings
        summary += f"\nMIDI Settings:\n"
        midi = self.config["midi_settings"]
        summary += f"  Device ID: {midi['device_id']}\n"
        summary += f"  Velocity: {midi['velocity']}\n"
        summary += f"  Channel: {midi['channel']}\n"
        
        # Gesture Settings
        summary += f"\nGesture Settings:\n"
        gesture = self.config["gesture_settings"]
        summary += f"  Stability Threshold: {gesture['stability_threshold']}\n"
        summary += f"  History Length: {gesture['history_length']}\n"
        summary += f"  Camera Index: {gesture['camera_index']}\n"
        
        return summary

def test_config_manager():
    """Test function for configuration manager"""
    config = ConfigManager("test_config.json")
    
    print("Default configuration loaded:")
    print(config.get_config_summary())
    
    # Modify some settings
    config.set_chord(1, [48, 52, 55])  # C Major in a lower octave
    config.set_midi_settings(velocity=80, channel=1)
    config.set_gesture_settings(stability_threshold=0.8)
    
    print("\nAfter modifications:")
    print(config.get_config_summary())
    
    # Save and reload
    config.save_config()
    
    config2 = ConfigManager("test_config.json")
    print("\nAfter save/reload:")
    print(config2.get_config_summary())
    
    # Clean up
    os.remove("test_config.json")
    print("\nTest completed")

if __name__ == "__main__":
    test_config_manager()