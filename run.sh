#!/bin/bash

# Air MIDI - Quick Run Script
# This script activates the virtual environment with MediaPipe and runs the application

echo "🎵 Starting Air MIDI - Hand Gesture Chord Controller (with MediaPipe)"
echo "====================================================================="

# Check if MediaPipe virtual environment exists
if [ ! -d "venv_mp" ]; then
    echo "❌ MediaPipe virtual environment not found. Setting up..."
    echo "🔧 Creating Python 3.11 virtual environment for MediaPipe..."
    python3.11 -m venv venv_mp
    echo "✅ Virtual environment created"
    
    # Activate and install dependencies
    source venv_mp/bin/activate
    echo "📦 Installing MediaPipe and dependencies..."
    pip install -r requirements.txt
else
    # Activate existing virtual environment
    echo "🔧 Activating MediaPipe virtual environment..."
    source venv_mp/bin/activate
fi

# Run the application
echo "🚀 Launching Air MIDI with MediaPipe hand tracking..."
python main.py

echo "👋 Air MIDI has been closed. Thanks for making music with MediaPipe!"