#!/usr/bin/env python3
"""
Air MIDI - Hand Gesture Chord Controller

A Python application that uses computer vision to detect hand gestures
and trigger MIDI chords in real-time.

Features:
- Hand gesture recognition using MediaPipe
- Custom chord editor with interactive piano roll
- Real-time MIDI output
- Configurable chord assignments
- Save/load configurations

Usage:
    python main.py

Requirements:
    - Python 3.7+
    - OpenCV, MediaPipe, pygame
    - Camera access
    - MIDI output device (software or hardware)

Author: Generated with Claude Code
Version: 1.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    try:
        import cv2
    except ImportError:
        missing_deps.append("opencv-python")
    
    try:
        import mediapipe
    except ImportError:
        missing_deps.append("mediapipe")
    
    try:
        import pygame
    except ImportError:
        missing_deps.append("pygame")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        from PIL import Image, ImageTk
    except ImportError:
        missing_deps.append("Pillow")
    
    return missing_deps

def show_dependency_error(missing_deps):
    """Show error dialog for missing dependencies"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    message = f"""Missing required dependencies: {', '.join(missing_deps)}

To install the missing dependencies, run:

pip install {' '.join(missing_deps)}

Or install all requirements:

pip install -r requirements.txt"""
    
    messagebox.showerror("Missing Dependencies", message)
    root.destroy()

def check_camera_access():
    """Check if camera is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False
        cap.release()
        return True
    except Exception:
        return False

def main():
    """Main application entry point"""
    print("Air MIDI - Hand Gesture Chord Controller")
    print("=" * 50)
    
    # Check dependencies
    print("Checking dependencies...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"ERROR: Missing dependencies: {', '.join(missing_deps)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_deps)}")
        show_dependency_error(missing_deps)
        sys.exit(1)
    
    print("✓ All dependencies found")
    
    # Check camera access
    print("Checking camera access...")
    if not check_camera_access():
        print("WARNING: Camera not accessible. Gesture recognition will not work.")
        print("Please ensure your camera is connected and not in use by another application.")
        
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(
            "Camera Warning", 
            "Camera not accessible. Continue anyway?\n\n"
            "You can still use the chord editor, but gesture recognition will not work."
        )
        root.destroy()
        
        if not result:
            sys.exit(1)
    else:
        print("✓ Camera accessible")
    
    # Import and run the application
    try:
        print("Starting Air MIDI application...")
        from chord_editor import ChordEditor
        
        app = ChordEditor()
        app.run()
        
    except Exception as e:
        print(f"ERROR: Failed to start application: {e}")
        print("\nFull error traceback:")
        traceback.print_exc()
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Application Error", 
            f"Failed to start Air MIDI:\n\n{str(e)}\n\n"
            "Check the console for more details."
        )
        root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()