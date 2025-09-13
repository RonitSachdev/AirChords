# Air MIDI - Hand Gesture Chord Controller

A Python application that uses computer vision to detect hand gestures and trigger MIDI chords in real-time. Control your music with just your hands!

## Features

- **Hand Gesture Recognition**: Uses MediaPipe for accurate hand tracking and finger detection (1-5 fingers)
- **Custom Chord Editor**: Interactive piano roll interface for creating custom chords
- **Real-time MIDI Output**: Immediate chord playback through MIDI devices
- **5 Configurable Chords**: Map different finger counts to custom chord configurations
- **Persistent Settings**: Save and load your custom chord configurations
- **Visual Feedback**: Live camera view with MediaPipe hand landmarks overlay
- **High Accuracy**: MediaPipe provides professional-grade hand tracking

## How It Works

1. **Show Fingers**: Hold up 1-5 fingers on your right hand to the camera
2. **Trigger Chords**: Each finger count (1-5) triggers a different chord
3. **Customize Chords**: Click on the piano roll to add/remove notes from each chord
4. **Toggle Buttons**: Select which chord to edit using the 5 toggle buttons

## Installation

1. **Clone or download** this repository
2. **Install Python 3.11 and dependencies**:
   ```bash
   brew install python@3.11 python-tk@3.11
   python3.11 -m venv venv_mp
   source venv_mp/bin/activate
   pip install mediapipe opencv-python pygame numpy Pillow
   ```

## Requirements

- Python 3.11 (MediaPipe compatibility)
- Webcam/camera access
- MIDI output device (software synthesizer or hardware)

### Python Dependencies

- mediapipe (professional hand tracking)
- opencv-python (camera and computer vision)
- pygame (MIDI output)
- numpy (numerical operations)
- Pillow (image processing)

## Usage

### Quick Start

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Set up MIDI**:
   - Connect to a MIDI device using the dropdown menu
   - Click "Refresh Devices" if your device doesn't appear

3. **Customize chords**:
   - Click a chord button (1-5) to select it
   - Click on the piano roll to add/remove notes
   - Test your chord with "Play Chord"

4. **Start gesture mode**:
   - Click "Start Gesture Mode"
   - Show your right hand to the camera
   - Hold up 1-5 fingers to trigger chords

### Interface Guide

#### Control Panel (Left Side)

- **Chord Selection**: 5 toggle buttons for selecting which chord to edit
- **MIDI Settings**: Device selection and velocity control  
- **Gesture Control**: Start/stop camera and view current gesture
- **Chord Actions**: Play, clear, or test all chords

#### Piano Roll (Right Side)

- **Interactive Piano**: Click keys to add/remove notes from selected chord
- **Camera View**: Live view of gesture detection (when active)
- **Chord Info**: Shows currently selected notes

### Menu Options

- **File → Save/Load Configuration**: Persist your settings
- **File → Export/Import Chords**: Share chord configurations
- **Settings → Reset to Defaults**: Restore default chords

## Default Chords

The application comes with these default chord configurations:

1. **1 Finger**: C Major (C, E, G)
2. **2 Fingers**: D Minor (D, F, A) 
3. **3 Fingers**: E Minor (E, G, B)
4. **4 Fingers**: F Major (F, A, C)
5. **5 Fingers**: G Major (G, B, D)

## MIDI Setup

### Software Synthesizers

For software-based MIDI playback, try:

- **Windows**: Windows built-in synth, VirtualMIDISynth
- **macOS**: Built-in Audio MIDI Setup, GarageBand
- **Linux**: FluidSynth, QSynth

### Hardware MIDI

Connect any MIDI-capable device:
- Keyboards/synthesizers
- MIDI controllers
- Hardware sound modules

## Troubleshooting

### Camera Issues

- **"Camera not accessible"**: Close other applications using the camera
- **Poor detection**: Ensure good lighting and clear background
- **Wrong hand detected**: Make sure to use your right hand

### MIDI Issues

- **"No MIDI devices found"**: Install a software synthesizer or connect hardware
- **No sound**: Check your audio settings and MIDI device configuration
- **Connection failed**: Try refreshing devices or restarting the application

### Performance Issues

- **Slow gesture detection**: Close unnecessary applications
- **Camera lag**: Try reducing camera resolution in gesture_recognition.py

## Configuration Files

- `air_midi_config.json`: Main configuration (auto-created)
- Exported chord files: Shareable chord configurations

## Advanced Usage

### Customizing Gesture Recognition

Edit `gesture_recognition.py` to adjust:
- Detection sensitivity
- Stability filtering
- Camera settings

### Adding More Chords

The current design supports 5 chords, but you can modify the code to support more by editing the chord editor interface.

### Custom MIDI Mapping

Modify `midi_controller.py` to:
- Change MIDI channels
- Add program changes
- Implement velocity sensitivity

## Technical Details

- **Hand Tracking**: MediaPipe Hands solution
- **Gesture Logic**: Finger tip vs. PIP joint positioning
- **MIDI Protocol**: Standard MIDI note on/off messages
- **GUI Framework**: tkinter with custom widgets
- **Configuration**: JSON-based persistence

## Limitations

- Requires right hand for gesture detection
- Works best with good lighting
- Needs clear background for optimal detection
- Limited to 5 simultaneous chord mappings

## Contributing

Feel free to submit issues, suggestions, or pull requests to improve the application!

## License

This project is open source. Just mention my name and feel free to modify and distribute as needed.

---

**Enjoy making music with your hands! 🎵👋**