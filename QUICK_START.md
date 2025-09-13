# 🚀 Air MIDI - Quick Start

## Run the Application

### Option 1: Use the run script (Easiest)
```bash
./run.sh
```

### Option 2: Manual run
```bash
source venv_mp/bin/activate
python main.py
```

### Option 3: One-liner (if already set up)
```bash
cd "/Users/sachdevronit/Desktop/Personal Testing/air midi" && source venv_mp/bin/activate && python main.py
```

## First-Time Setup (One Time Only)

1. **Install system dependencies:**
   ```bash
   brew install python@3.11 python-tk@3.11
   ```

2. **Create virtual environment with MediaPipe:**
   ```bash
   python3.11 -m venv venv_mp
   ```

3. **Install Python packages:**
   ```bash
   source venv_mp/bin/activate
   pip install mediapipe opencv-python pygame numpy Pillow
   ```

## How to Use

1. **🎹 Edit Chords**: Click chord buttons (1-5), then click piano keys
2. **🎵 Connect MIDI**: Select device from dropdown, click "Refresh Devices" if needed  
3. **👋 Use Gestures**: Click "Start Gesture Mode", show 1-5 fingers to trigger chords
4. **💾 Save Settings**: Use File menu to save your custom chords

## Default Gestures

- 👆 **1 Finger** → C Major (C-E-G)
- ✌️ **2 Fingers** → D Minor (D-F-A)  
- 🖖 **3 Fingers** → E Minor (E-G-B)
- 🖐️ **4 Fingers** → F Major (F-A-C)
- ✋ **5 Fingers** → G Major (G-B-D)

## Troubleshooting

- **No camera?** → Grant camera permission to Terminal
- **No MIDI devices?** → Install GarageBand or FluidSynth
- **App won't start?** → Check SETUP_GUIDE.md for detailed help

---
**Ready to make music with your hands! 🎵👋**