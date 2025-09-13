import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Dict, Set, Optional
import cv2
from PIL import Image, ImageTk

from midi_controller_mido import MIDIController
from piano_roll import PianoRoll
from config_manager import ConfigManager
from gesture_recognition import GestureRecognizer

class ChordEditor:
    """Main GUI application for chord editing and gesture recognition"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Air MIDI - Hand Gesture Chord Controller")
        self.root.geometry("1600x1200")  # Much larger window for 800x600 camera view
        self.root.resizable(True, True)
        
        # Application components
        self.config_manager = ConfigManager()
        self.midi_controller = MIDIController()
        self.gesture_recognizer = GestureRecognizer()
        
        # GUI state
        self.current_chord = 1
        self.chord_buttons: Dict[int, tk.Button] = {}
        self.is_gesture_mode = False
        self.gesture_thread = None
        self.camera_running = False
        self.currently_playing_chord = 0  # Track which chord is currently playing
        
        self.setup_gui()
        
        # Load configuration after GUI is set up
        self.load_configuration()
        self.update_chord_display()
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Left panel - Controls
        self.setup_control_panel(main_frame)
        
        # Right panel - Piano and gesture view
        self.setup_piano_panel(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
        # Menu bar
        self.setup_menu_bar()
    
    def setup_control_panel(self, parent):
        """Setup the left control panel"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Chord selection buttons
        chord_frame = ttk.LabelFrame(control_frame, text="Chord Selection", padding="10")
        chord_frame.pack(fill=tk.X, pady=(0, 10))
        
        for i in range(1, 6):
            btn = tk.Button(
                chord_frame, 
                text=f"Chord {i}\n(Show {i} finger{'s' if i > 1 else ''})",
                width=12, height=3,
                command=lambda x=i: self.select_chord(x)
            )
            btn.pack(pady=2)
            self.chord_buttons[i] = btn
        
        # MIDI controls
        midi_frame = ttk.LabelFrame(control_frame, text="MIDI Settings", padding="10")
        midi_frame.pack(fill=tk.X, pady=(0, 10))
        
        # MIDI device selection
        ttk.Label(midi_frame, text="MIDI Device:").pack(anchor=tk.W)
        self.midi_device_var = tk.StringVar()
        self.midi_device_combo = ttk.Combobox(
            midi_frame, textvariable=self.midi_device_var, state="readonly"
        )
        self.midi_device_combo.pack(fill=tk.X, pady=(0, 5))
        self.midi_device_combo.bind('<<ComboboxSelected>>', self.on_midi_device_change)
        
        ttk.Button(midi_frame, text="Refresh Devices", 
                  command=self.refresh_midi_devices).pack(pady=(0, 5))
        
        # Velocity control
        ttk.Label(midi_frame, text="Velocity:").pack(anchor=tk.W)
        self.velocity_var = tk.IntVar(value=100)
        velocity_scale = ttk.Scale(
            midi_frame, from_=1, to=127, 
            variable=self.velocity_var, orient=tk.HORIZONTAL
        )
        velocity_scale.pack(fill=tk.X)
        velocity_scale.bind('<ButtonRelease-1>', self.on_velocity_change)
        
        self.velocity_label = ttk.Label(midi_frame, text="100")
        self.velocity_label.pack()
        
        # Gesture controls
        gesture_frame = ttk.LabelFrame(control_frame, text="Gesture Control", padding="10")
        gesture_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.gesture_button = ttk.Button(
            gesture_frame, text="Start Gesture Mode", 
            command=self.toggle_gesture_mode
        )
        self.gesture_button.pack(pady=(0, 5))
        
        self.current_gesture_label = ttk.Label(gesture_frame, text="No gesture detected")
        self.current_gesture_label.pack()
        
        # Chord action buttons
        action_frame = ttk.LabelFrame(control_frame, text="Chord Actions", padding="10")
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="Play Chord", 
                  command=self.play_current_chord).pack(fill=tk.X, pady=2)
        
        ttk.Button(action_frame, text="Clear Chord", 
                  command=self.clear_current_chord).pack(fill=tk.X, pady=2)
        
        ttk.Button(action_frame, text="Test All Chords", 
                  command=self.test_all_chords).pack(fill=tk.X, pady=2)
    
    def setup_piano_panel(self, parent):
        """Setup the right panel with piano roll"""
        piano_frame = ttk.LabelFrame(parent, text="Piano Roll - Click to Edit Chord", padding="10")
        piano_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Piano roll widget
        self.piano_roll = PianoRoll(
            piano_frame, 
            width=900, height=200,
            start_note=21, end_note=108
        )
        self.piano_roll.pack(pady=(0, 10))
        self.piano_roll.on_note_change = self.on_piano_notes_changed
        
        # Camera view frame (initially hidden)
        self.camera_frame = ttk.LabelFrame(piano_frame, text="Camera View - Hand Gesture Recognition", padding="10")
        
        # Much larger camera display - size it for 800x600 camera view
        self.camera_label = tk.Label(self.camera_frame, text="Camera not active\nClick 'Start Gesture Mode' to begin", 
                                   width=100, height=40, bg='lightgray', font=('Arial', 14), 
                                   justify=tk.CENTER)
        self.camera_label.pack()
        
        # Chord info
        info_frame = ttk.Frame(piano_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(info_frame, text="Selected Notes:").pack(anchor=tk.W)
        self.chord_info_label = ttk.Label(info_frame, text="None", font=('TkDefaultFont', 10, 'bold'))
        self.chord_info_label.pack(anchor=tk.W)
    
    def setup_status_bar(self, parent):
        """Setup the status bar"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.connection_label = ttk.Label(self.status_frame, text="MIDI: 0 devices", foreground='orange')
        self.connection_label.pack(side=tk.RIGHT)
    
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Configuration", command=self.save_configuration)
        file_menu.add_command(label="Load Configuration", command=self.load_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Export Chords", command=self.export_chords)
        file_menu.add_command(label="Import Chords", command=self.import_chords)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Reset to Defaults", command=self.reset_to_defaults)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def select_chord(self, chord_number: int):
        """Select a chord for editing"""
        # Update button states
        for i, btn in self.chord_buttons.items():
            if i == chord_number:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        self.current_chord = chord_number
        self.update_chord_display()
        self.status_label.config(text=f"Editing Chord {chord_number}")
    
    def update_chord_display(self):
        """Update the piano roll to show the current chord"""
        chord_notes = set(self.midi_controller.get_chord(self.current_chord))
        self.piano_roll.set_selected_notes(chord_notes, notify=False)
        
        # Update chord info
        if chord_notes:
            note_names = [MIDIController.note_to_name(note) for note in sorted(chord_notes)]
            self.chord_info_label.config(text=f"Chord {self.current_chord}: {', '.join(note_names)}")
        else:
            self.chord_info_label.config(text=f"Chord {self.current_chord}: Empty")
    
    def on_piano_notes_changed(self, notes: Set[int]):
        """Handle piano roll note changes"""
        self.midi_controller.set_chord(self.current_chord, list(notes))
        self.config_manager.set_chord(self.current_chord, list(notes))
        self.update_chord_display()
    
    def refresh_midi_devices(self):
        """Refresh the list of available MIDI devices"""
        devices = self.midi_controller.list_devices()
        device_list = [f"{i}: {name}" for i, name in devices.items()]
        
        self.midi_device_combo['values'] = device_list
        
        if device_list:
            # Update connection label with device count
            self.connection_label.config(text=f"MIDI: {len(device_list)} devices", foreground='blue')
            
            # Auto-select first device if none selected
            if not self.midi_device_var.get():
                self.midi_device_combo.current(0)
                # Auto-connect to first device
                device_id = int(device_list[0].split(':')[0])
                if self.midi_controller.connect(device_id):
                    self.connection_label.config(text=f"MIDI: Connected ({len(device_list)} available)", foreground='green')
                    self.config_manager.set_midi_settings(device_id=device_id)
                    self.status_label.config(text=f"Auto-connected to {devices[device_id]}")
                else:
                    self.status_label.config(text=f"Found {len(device_list)} MIDI device(s) - connection failed")
            else:
                self.status_label.config(text=f"Found {len(device_list)} MIDI device(s)")
        else:
            self.connection_label.config(text="MIDI: 0 devices", foreground='red')
            self.status_label.config(text="No MIDI devices found")
    
    def on_midi_device_change(self, event=None):
        """Handle MIDI device selection change"""
        selection = self.midi_device_var.get()
        if selection:
            device_id = int(selection.split(':')[0])
            devices = self.midi_controller.list_devices()
            if self.midi_controller.connect(device_id):
                self.connection_label.config(text=f"MIDI: Connected ({len(devices)} available)", foreground='green')
                self.config_manager.set_midi_settings(device_id=device_id)
            else:
                self.connection_label.config(text=f"MIDI: Failed ({len(devices)} available)", foreground='red')
    
    def on_velocity_change(self, event=None):
        """Handle velocity change"""
        velocity = self.velocity_var.get()
        self.velocity_label.config(text=str(velocity))
        self.midi_controller.set_velocity(velocity)
        self.config_manager.set_midi_settings(velocity=velocity)
    
    def play_current_chord(self):
        """Play the currently selected chord"""
        if not self.midi_controller.outport:
            messagebox.showwarning("MIDI Not Connected", "Please connect to a MIDI device first.")
            return
        
        self.midi_controller.play_chord(self.current_chord, duration=2.0)
        self.status_label.config(text=f"Playing Chord {self.current_chord}")
    
    def clear_current_chord(self):
        """Clear the currently selected chord"""
        self.midi_controller.set_chord(self.current_chord, [])
        self.config_manager.set_chord(self.current_chord, [])
        self.update_chord_display()
        self.status_label.config(text=f"Cleared Chord {self.current_chord}")
    
    def test_all_chords(self):
        """Play all chords in sequence"""
        if not self.midi_controller.outport:
            messagebox.showwarning("MIDI Not Connected", "Please connect to a MIDI device first.")
            return
        
        def play_sequence():
            for i in range(1, 6):
                self.root.after(0, lambda x=i: self.status_label.config(text=f"Playing Chord {x}"))
                self.midi_controller.play_chord(i, duration=1.5)
                threading.Event().wait(2.0)
            self.root.after(0, lambda: self.status_label.config(text="Chord test complete"))
        
        threading.Thread(target=play_sequence, daemon=True).start()
    
    def toggle_gesture_mode(self):
        """Toggle gesture recognition mode"""
        if not self.is_gesture_mode:
            self.start_gesture_mode()
        else:
            self.stop_gesture_mode()
    
    def start_gesture_mode(self):
        """Start gesture recognition"""
        if not self.midi_controller.outport:
            messagebox.showwarning("MIDI Not Connected", "Please connect to a MIDI device first.")
            return
        
        if not self.gesture_recognizer.start_camera():
            messagebox.showerror("Camera Error", "Could not access camera.")
            return
        
        self.is_gesture_mode = True
        self.camera_running = True
        self.gesture_button.config(text="Stop Gesture Mode")
        self.camera_frame.pack(pady=(10, 0))
        
        # Note: We don't clear piano roll selection as it doesn't interfere with gesture chords
        
        # Start gesture recognition thread
        self.gesture_thread = threading.Thread(target=self.gesture_recognition_loop, daemon=True)
        self.gesture_thread.start()
        
        self.status_label.config(text="Gesture mode active - Show your right hand to the camera")
    
    def stop_gesture_mode(self):
        """Stop gesture recognition"""
        self.is_gesture_mode = False
        self.camera_running = False
        self.gesture_button.config(text="Start Gesture Mode")
        self.camera_frame.pack_forget()
        
        # Stop any currently playing chord
        if self.currently_playing_chord != 0:
            self.midi_controller.stop_chord(self.currently_playing_chord)
            self.currently_playing_chord = 0
        
        # Ensure all MIDI notes are stopped
        self.midi_controller.stop_all_notes()
        
        self.gesture_recognizer.stop_camera()
        self.current_gesture_label.config(text="No gesture detected")
        self.status_label.config(text="Gesture mode stopped")
    
    def gesture_recognition_loop(self):
        """Main gesture recognition loop"""
        last_gesture = 0
        
        while self.camera_running:
            try:
                frame, finger_count = self.gesture_recognizer.process_frame()
                
                if frame is not None:
                    # Update camera display
                    self.update_camera_display(frame)
                    
                    # Update gesture status
                    self.root.after(0, self.update_gesture_status, finger_count)
                    
                    # Always trigger chord update (handles starting, stopping, and switching)
                    if finger_count != last_gesture:
                        self.root.after(0, self.trigger_gesture_chord, finger_count)
                    
                    last_gesture = finger_count
                
            except Exception as e:
                print(f"Gesture recognition error: {e}")
                break
    
    def update_camera_display(self, frame):
        """Update the camera display with the current frame"""
        try:
            # Convert frame to PhotoImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Large camera view for better hand detection visibility
            frame_resized = cv2.resize(frame_rgb, (800, 600))  # Even larger!
            image = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image)
            
            # Update label - remove text constraints and let image size determine display
            self.camera_label.config(image=photo, width=800, height=600)
            self.camera_label.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"Camera display error: {e}")
    
    def update_gesture_status(self, finger_count):
        """Update the gesture status label"""
        if finger_count > 0:
            self.current_gesture_label.config(text=f"Detected: {finger_count} finger{'s' if finger_count > 1 else ''}")
        else:
            self.current_gesture_label.config(text="No gesture detected")
    
    def trigger_gesture_chord(self, chord_number):
        """Trigger a chord based on gesture"""
        print(f"Gesture trigger: current={self.currently_playing_chord}, new={chord_number}")
        
        # Always stop current chord first if there is one
        if self.currently_playing_chord != 0:
            print(f"Stopping current chord {self.currently_playing_chord}")
            self.midi_controller.stop_chord(self.currently_playing_chord)
            self.currently_playing_chord = 0
        
        if 1 <= chord_number <= 5:
            print(f"Starting new chord {chord_number}")
            # Start new chord
            self.midi_controller.play_chord(chord_number)
            self.currently_playing_chord = chord_number
            
            # Highlight the corresponding chord
            chord_notes = set(self.midi_controller.get_chord(chord_number))
            self.piano_roll.set_highlighted_notes(chord_notes)
        else:
            # No fingers detected - clear highlight
            # print("No fingers - clearing highlight")
            self.piano_roll.set_highlighted_notes(set())
    
    def save_configuration(self):
        """Save current configuration"""
        if self.config_manager.save_config():
            self.status_label.config(text="Configuration saved")
            messagebox.showinfo("Save", "Configuration saved successfully!")
        else:
            messagebox.showerror("Save Error", "Failed to save configuration.")
    
    def load_configuration(self):
        """Load configuration from file"""
        self.config_manager = ConfigManager()
        
        # Load MIDI controller chords
        chords = self.config_manager.get_chords()
        for chord_num, notes in chords.items():
            self.midi_controller.set_chord(chord_num, notes)
        
        # Load MIDI settings
        midi_settings = self.config_manager.get_midi_settings()
        self.velocity_var.set(midi_settings.get('velocity', 100))
        self.midi_controller.set_velocity(midi_settings.get('velocity', 100))
        
        self.update_chord_display()
        self.refresh_midi_devices()
        
        self.status_label.config(text="Configuration loaded")
    
    def export_chords(self):
        """Export chord configurations to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Chords"
        )
        
        if filename:
            if self.config_manager.export_chords(filename):
                messagebox.showinfo("Export", f"Chords exported to {filename}")
            else:
                messagebox.showerror("Export Error", "Failed to export chords.")
    
    def import_chords(self):
        """Import chord configurations from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Chords"
        )
        
        if filename:
            if self.config_manager.import_chords(filename):
                # Reload chords into MIDI controller
                chords = self.config_manager.get_chords()
                for chord_num, notes in chords.items():
                    self.midi_controller.set_chord(chord_num, notes)
                
                self.update_chord_display()
                messagebox.showinfo("Import", f"Chords imported from {filename}")
            else:
                messagebox.showerror("Import Error", "Failed to import chords.")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        result = messagebox.askyesno("Reset", "Reset all settings to defaults?")
        if result:
            self.config_manager.reset_to_defaults()
            self.load_configuration()
            messagebox.showinfo("Reset", "Settings reset to defaults")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Air MIDI - Hand Gesture Chord Controller

A Python application that uses computer vision to detect hand gestures and trigger MIDI chords.

Features:
• Hand gesture recognition using MediaPipe
• Custom chord editor with piano roll interface
• Real-time MIDI output
• Configurable chord assignments
• Save/load configurations

Controls:
• Show 1-5 fingers on your right hand to trigger chords
• Click piano keys to customize chord notes
• Use toggle buttons to select which chord to edit

Requirements:
• Python 3.7+
• OpenCV, MediaPipe, pygame
• Camera access
• MIDI output device (software or hardware)

Version 1.0"""
        
        messagebox.showinfo("About Air MIDI", about_text)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_gesture_mode:
            self.stop_gesture_mode()
        
        self.midi_controller.disconnect()
        self.config_manager.save_config()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize with first chord selected
        self.select_chord(1)
        self.refresh_midi_devices()
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ChordEditor()
    app.run()