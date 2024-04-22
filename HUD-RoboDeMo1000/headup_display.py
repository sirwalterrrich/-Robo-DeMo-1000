# Author : Sir Walter Richardson - April 20, 2024
# Script Name - headup_display.py 
# Project Title: Custom Head Up Display for Robo DeMo 1000 Project
# This project leverages the pygame, openCV, flask libraries.
    # Flask is used to serve the webpages for control
    # Pygame is used for playing audio locally through the RPI's speaker
    # OpenCV is called to interact with webcam. 

# This script creates a web app using Flask on http://127.0.0.1:5000
# Top Features  
    # Centered Webcam view ()
    # Button for activating the 'main.py' - 'Robo DeMo 1000' - Uses ComputerVision to identify runners and shouts demotivational or motivational messages
    # Soundboard for taunting other runners in real life if Robo DeMo is just not enough
    # Host System information (RPI5) is displayed on the bottom of the screen

# Design Considerations
# No robot controls were added here because the robot is supposed to be semi autonomous.


from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
from datetime import datetime
import cv2
import numpy as np
import pygame
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required to use sessions

AUDIO_FOLDER = os.path.join(app.static_folder, 'audio')
SCREENSHOT_FOLDER = os.path.join(app.static_folder, 'screenshots')

# Initialize USB webcam
camera = cv2.VideoCapture(2)  # Use 0 for the first connected webcam, 1 for the second, and so on

# Initialize pygame mixer
pygame.mixer.init()

def get_system_info():
    # Implement logic to fetch system information (e.g., CPU usage, memory usage, uptime)
    # For demonstration purposes, let's just return a static message
    # Get CPU usage
    cpu_usage = subprocess.getoutput("top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)}'")
    # Get memory usage
    memory_usage = subprocess.getoutput("free -m | awk 'NR==2{printf \"%s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'")
    # Get uptime
    uptime = subprocess.getoutput("uptime -p")
    # Get current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Return formatted system information
    return f"System Information as of {current_time}: \n - CPU Usage: {cpu_usage} \n - Memory Usage: {memory_usage} \n - Uptime: {uptime}"
    #return "System Information: Raspberry Pi running DOOM-style HUD"

@app.route('/')
def index():
    # Use a session variable to store and retrieve user preferences for audio playback
    if 'play_on_pi' not in session:
        session['play_on_pi'] = False
    sounds = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.mp3')]
    sounds.sort()
    return render_template('index4.html', system_info=get_system_info(), sounds=sounds, play_on_pi=session['play_on_pi'])

@app.route('/toggle_playback', methods=['POST'])
def toggle_playback():
    # Toggle the playback location preference
    session['play_on_pi'] = not session.get('play_on_pi', False)
    return redirect(url_for('index'))

@app.route('/play/<filename>')
def play_sound(filename):
    filepath = os.path.join(AUDIO_FOLDER, filename)
    if session.get('play_on_pi', False):
        # Play sound using Pygame
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        # Wait for the music to play before ending the function
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return redirect(url_for('index'))
    else:
        # Return a page where the sound can be played in the browser
        return render_template('play.html', filename=filename)

@app.route('/play_local/<filename>')
def play_sound_local(filename):
    filepath = os.path.join(AUDIO_FOLDER, filename)
    # Play sound locally using Pygame
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    # Wait for the music to play before ending the function
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    return '', 204  # Return an empty response with a 'No Content' status

@app.route('/webcam_feed')
def webcam_feed():
    return render_template('webcam_feed.html')

@app.route('/capture_frame')
def capture_frame():
    ret, frame = camera.read()
    if ret:
        # Convert frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            return jpeg.tobytes(), 200, {'Content-Type': 'image/jpeg'}
    return '', 204

@app.route('/save_screenshot', methods=['POST'])
def save_screenshot():
    data = request.json
    image_data = data['image']
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'screenshot_{timestamp}.jpg'
    filepath = os.path.join(SCREENSHOT_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)
    return jsonify({'message': 'Screenshot saved successfully.', 'filename': filename})

@app.route('/run_script')
def run_script():
    try:
        # Launches main.py - Robo DeMo - Running Demotivator Motivator
        subprocess.run(['python', 'main.py'], check=True)
        return jsonify({'message': 'Script executed successfully.'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'An error occurred while executing the script.', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
