# 🎹 Air MIDI - Easy Installation Guide for Mac

**Created by Ronit Sachdev**

This guide will help you install and run Air MIDI on your Mac, even if you've never used programming tools before!

## ⏱️ Time Required
About 15-20 minutes for first-time setup.

## 📋 What You'll Need
- A Mac with macOS 10.15 or later
- Internet connection
- Built-in camera or external webcam

---

## 🚀 Step-by-Step Installation

### Step 1: Install Homebrew (Package Manager)

Homebrew makes it easy to install Python and other tools on Mac.

1. **Open Terminal**:
   - Press `Cmd + Space` to open Spotlight
   - Type "Terminal" and press Enter
   - A black window will appear - this is the Terminal

2. **Install Homebrew**:
   - Copy and paste this command into Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Press Enter and wait for it to finish (may take 5-10 minutes)
   - Enter your Mac password when asked (typing won't show on screen - this is normal)

### Step 2: Install Python 3.11

Python 3.11 is required for Air MIDI to work properly.

1. **Install Python 3.11**:
   ```bash
   brew install python@3.11
   ```
   - Wait for installation to complete

2. **Install Tkinter** (for the user interface):
   ```bash
   brew install python-tk@3.11
   ```

### Step 3: Download Air MIDI

1. **Create a folder for the project**:
   ```bash
   cd ~/Desktop
   mkdir AirMIDI
   cd AirMIDI
   ```

2. **Download the code**:
   - Go to the GitHub repository in your web browser
   - Click the green "Code" button
   - Click "Download ZIP"
   - Unzip the downloaded file
   - Move all files to the `AirMIDI` folder you created

   **OR** if you have git installed:
   ```bash
   git clone https://github.com/RonitSachdev/AirChords.git
   ```

### Step 4: Set Up Virtual Environment

A virtual environment keeps Air MIDI's requirements separate from other Python projects.

1. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv_mp
   ```

2. **Activate virtual environment**:
   ```bash
   source venv_mp/bin/activate
   ```
   - You should see `(venv_mp)` at the beginning of your terminal prompt

### Step 5: Install Required Packages

1. **Install Air MIDI dependencies**:
   ```bash
   pip install mediapipe opencv-python mido python-rtmidi numpy pillow
   ```
   - This will download and install all necessary packages (may take 5 minutes)

### Step 6: Run Air MIDI! 🎉

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Grant camera permissions**:
   - macOS will ask for camera access
   - Click "OK" to allow camera access

3. **Start making music**:
   - The Air MIDI interface will open
   - Select a MIDI device from the dropdown
   - Click "Start Gesture Mode"
   - Hold up 1-5 fingers to play chords!

---

## 🔧 Troubleshooting

### "Command not found" errors
If you get "command not found" errors, try:
```bash
# Add Homebrew to your PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Camera not working
- Go to System Settings → Privacy & Security → Camera
- Make sure Terminal has camera access
- Restart the app if needed

### No sound
- Install a software synthesizer like GarageBand
- Or use the built-in macOS Audio MIDI Setup

### Python version issues
Make sure you're using Python 3.11:
```bash
python3.11 --version
```
Should show: `Python 3.11.x`

---

## 🎯 Running Air MIDI Again (After First Install)

Once everything is installed, you only need to do this to run Air MIDI:

1. **Open Terminal**
2. **Navigate to Air MIDI folder**:
   ```bash
   cd ~/Desktop/AirMIDI
   ```
3. **Activate virtual environment**:
   ```bash
   source venv_mp/bin/activate
   ```
4. **Run the app**:
   ```bash
   python main.py
   ```

---

## 💡 Tips for Success

- **Keep Terminal open** while using Air MIDI
- **Good lighting** helps with hand detection
- **Clear background** behind your hand works best
- **Use your right hand** for gesture recognition
- **1-5 fingers** trigger different chords

---

## 🆘 Need Help?

If you run into issues:

1. **Check the error message** in Terminal - it usually tells you what's wrong
2. **Try restarting Terminal** and running the commands again
3. **Make sure your camera isn't being used** by other apps (Zoom, FaceTime, etc.)
4. **Contact Ronit Sachdev** - the creator can help troubleshoot!

---

## 🎵 Enjoy Your Music!

You're now ready to create music with your hands! Air MIDI uses advanced computer vision to detect your finger gestures and turn them into beautiful chord progressions.

**Created by Ronit Sachdev** - Enjoy making music with innovative gesture control! 🎹✨

---

*This installation guide is designed for complete beginners. Each step is carefully explained to ensure success!*