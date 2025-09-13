# 🎵 Air MIDI Setup & Run Guide

A complete guide to set up and run your hand gesture MIDI controller.

## 🚀 Quick Start

### 1. **System Requirements**
- macOS (tested on macOS Sequoia)
- Python 3.7+
- Webcam/camera access
- Terminal access

### 2. **Initial Setup**

#### Step 1: Navigate to the Project
```bash
cd "/Users/sachdevronit/Desktop/Personal Testing/air midi"
```

#### Step 2: Install Python 3.11 (for MediaPipe support)
```bash
brew install python@3.11 python-tk@3.11
```

#### Step 3: Create Virtual Environment with MediaPipe
```bash
python3.11 -m venv venv_mp
```

#### Step 4: Activate Virtual Environment
```bash
source venv_mp/bin/activate
```

#### Step 5: Install Dependencies with MediaPipe
```bash
pip install mediapipe opencv-python pygame numpy Pillow
```

**Note**: MediaPipe requires Python 3.11 or older. Python 3.13+ is not yet supported.

### 3. **Run the Application**

#### Method 1: Run with Dependency Checking
```bash
python main.py
```

#### Method 2: Manual run
```bash
source venv_mp/bin/activate
python main.py
```

### 4. **First Run Experience**

When you run the application, you'll see:

1. **Dependency Check**: Console output showing which packages are found
2. **Camera Check**: Verification that your camera is accessible
3. **GUI Launch**: The main Air MIDI interface opens

## 🎹 Using the Application

### **Main Interface Overview**

#### Left Panel - Controls
- **Chord Selection**: 5 buttons (Chord 1-5) for selecting which chord to edit
- **MIDI Settings**: Device selection and velocity control
- **Gesture Control**: Start/stop gesture recognition mode
- **Chord Actions**: Play, clear, and test chord functions

#### Right Panel - Piano Editor
- **Interactive Piano**: Click keys to add/remove notes from selected chord
- **Camera View**: Live gesture recognition display (when active)
- **Chord Info**: Shows currently selected notes and chord names

### **Step-by-Step Usage**

#### 1. **Set Up MIDI Output**
```
1. Click "Refresh Devices" to find available MIDI devices
2. Select a device from the dropdown
3. If no devices found, install a software synthesizer:
   - macOS: Use GarageBand or Audio MIDI Setup
   - Install FluidSynth: brew install fluidsynth
```

#### 2. **Customize Your Chords**
```
1. Click "Chord 1" button (it will highlight blue)
2. Click piano keys to add/remove notes
3. Click "Play Chord" to test your chord
4. Repeat for Chords 2-5
5. Use File → Save Configuration to persist changes
```

#### 3. **Use Gesture Control**
```
1. Ensure your camera has permission (macOS will prompt)
2. Click "Start Gesture Mode"
3. Position your right hand in front of the camera
4. Hold up 1-5 fingers to trigger corresponding chords
5. Watch the gesture detection in the camera view
```

### **Default Chord Mappings**

- **1 Finger** → Chord 1: C Major (C, E, G)
- **2 Fingers** → Chord 2: D Minor (D, F, A)
- **3 Fingers** → Chord 3: E Minor (E, G, B)
- **4 Fingers** → Chord 4: F Major (F, A, C)
- **5 Fingers** → Chord 5: G Major (G, B, D)

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### 1. **"Command not found: pip"**
```bash
# Use pip3 instead
pip3 install -r requirements.txt

# Or create virtual environment first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. **"No module named '_tkinter'"**
```bash
# Install tkinter support
brew install python-tk
```

#### 3. **"Could not find a version that satisfies the requirement mediapipe"**
```
This is normal! The app will use simplified gesture recognition.
MediaPipe may not be available on all systems.
```

#### 4. **Camera Access Issues**
```
- macOS will prompt for camera permission
- Close other apps using the camera
- Try different camera index in settings
- Grant Terminal camera access in System Preferences
```

#### 5. **No MIDI Devices Found**
```bash
# Install a software synthesizer
brew install fluidsynth

# Or use built-in options:
# - Open Audio MIDI Setup (macOS)
# - Launch GarageBand
# - Use online synthesizers
```

#### 6. **Poor Gesture Recognition**
```
- Ensure good lighting
- Use plain background
- Keep hand in camera view
- Make clear finger gestures
- Adjust sensitivity in gesture settings
```

### **Performance Tips**

1. **Better Gesture Detection**:
   - Good lighting conditions
   - Solid color background
   - Clear hand positioning
   - Stable hand gestures

2. **MIDI Performance**:
   - Use dedicated MIDI software/hardware
   - Adjust buffer sizes if audio glitches occur
   - Close unnecessary applications

3. **System Performance**:
   - Close other camera-using apps
   - Sufficient RAM for real-time processing
   - Good CPU for gesture recognition

## 📁 File Structure

```
air midi/
├── main.py                     # Application entry point
├── chord_editor.py             # Main GUI application
├── gesture_recognition.py      # MediaPipe hand tracking
├── midi_controller.py          # MIDI output handling
├── piano_roll.py              # Piano keyboard widget
├── config_manager.py          # Settings management
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── SETUP_GUIDE.md            # This setup guide
├── run.sh                    # Quick run script
├── venv_mp/                  # Virtual environment (Python 3.11 + MediaPipe)
└── air_midi_config.json     # Configuration file (auto-created)
```

## 🎛️ Configuration Files

### **air_midi_config.json**
Automatically created when you first run the app. Contains:
- Custom chord configurations
- MIDI device settings
- Gesture recognition parameters
- UI preferences

### **Exporting/Importing Chords**
```
File → Export Chords  # Save chord presets
File → Import Chords  # Load chord presets
```

## 🆘 Getting Help

### **Console Output**
The application provides detailed console output for debugging:
```bash
# Run with verbose output
python main.py
```

### **Test Individual Components**
```bash
# Test gesture recognition only
python gesture_recognition_simple.py

# Test MIDI output only  
python midi_controller.py

# Test piano interface only
python piano_roll.py
```

### **Reset to Defaults**
```
Settings → Reset to Defaults  # In the GUI
# Or delete: air_midi_config.json
```

## 🎵 Advanced Usage

### **Custom Gesture Sensitivity**
Edit `gesture_recognition_simple.py` to adjust:
- `stability_threshold`: How consistent gestures need to be
- `history_length`: How many frames to consider
- `min_area`/`max_area`: Hand detection sensitivity

### **MIDI Customization**
Edit `midi_controller.py` to modify:
- MIDI channels
- Velocity curves
- Program changes
- Custom chord progressions

### **Adding More Chords**
Currently supports 5 chords, but can be extended by modifying:
- `chord_editor.py`: Add more buttons
- `config_manager.py`: Extend chord storage
- `midi_controller.py`: Handle more chord numbers

---

## 🎉 Enjoy Making Music!

You now have a fully functional hand gesture MIDI controller. Wave your hands and make music! 

### **Pro Tips:**
- Start with simple chord progressions
- Practice smooth finger transitions
- Experiment with different MIDI sounds
- Save multiple chord preset files for different songs
- Use good lighting for best gesture recognition

**Happy Music Making! 🎵👋**