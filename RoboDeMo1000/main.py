#!/usr/bin/env python

# Author : Sir Walter R. - April 20, 2024
# Script Name - main.py 
# Project Title: Robo DeMo 1000

# This script started from the Viam (viam.com) python code sample generated after all the components were added to the configuration in the Viam web app.
# The code supports a robot base. The robot base has a RaspberryPi 5, PCA9685 (PWM), 
# Motor controllers, 4 motors, a USB camera, USB soundcard, Audio Ampplifier and Audio speaker, and wireless XBOX controller

# Remote Control
# This feature is achieved by using Viams built-in features.

# Text to Speech
# This feature is achieved by leveraging Eleven Labs API
# This main.py script calls another script called motivator_demotivator_1000.py. It implements the AI Text to Speech.
# This motivator_demotivator_1000.py script uses the ElevenLabs API for speech to text generation and pygame libraries for audio output.

# Computer Vision - Runner Detection
# Computer Vision is achieved by using Viam's built-in CV/ML features
# A People Detector was developed to trigger on people. Vision -> mlmodel

# Future work0: Custom head up display using a Flask Web App - Started on this 4/20/24
# Future work1: Add wireless remote control via an ESP32 Microntoller- Start and stop ESTOP function, instant jokes etc.
# Future work2: Use ChatGPT to respond to speech shouted at the robot.
# Future work3: I hope to use Computer Vision facial recognition models to trigger the type of selected messages.
                # For example, if the person looks super stressed during a run then tell them something motivational or funny.
# Future work4: Save the output.mp3 files for later use to save on bandwidth and ElevenLabs API Usage.
# Future work5: Implement the Viam 'navigation service' using a GPS module and IMU (9 axis accelerometer).
# Future work6: Use VIAM builtin computer vision to identify path markings for navigation and obstacle avoidance.
# Future work7: Implement status RGB LEDs using the Neopixel library. The RPI5 currently does not support the Neopixel library due to a hardware change.
                # This feature could be implement using an Arduino or other microcontroller but i'm short on time. 
                # Things to indicate using Neopixel LEDs. Network Status / Direction travel / Processor Heartbeat / an attraction pattern to bring curious runners closer to the camera
 
import asyncio
from datetime import datetime
import subprocess

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.movement_sensor import MovementSensor
from viam.components.motor import Motor
from viam.components.base import Base
from viam.components.camera import Camera

from viam.components.input import Controller
from viam.services.navigation import NavigationClient
from viam.services.vision import VisionClient, Detection #, VisModelConfig, VisModelType

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='ADD VIAM API Key HERE',
        api_key_id='ADD VIAM API Key ID HERE'
    )
    return await RobotClient.at_address('ADD VIAM server address HERE', opts)

async def main():
    machine = await connect()

    # RPI5
    rpi_5 = Board.from_robot(machine, "RPI5")
    rpi_5_return_value = await rpi_5.gpio_pin_by_name("16")
    # print(f"RPI5 gpio_pin_by_name return value: {rpi_5_return_value}")
  
    # # adafruit_ultimate_gps - No longer using the GPS feature
    # adafruit_ultimate_gps = MovementSensor.from_robot(machine, "adafruit_ultimate_gps")
    # adafruit_ultimate_gps_return_value = await adafruit_ultimate_gps.get_linear_acceleration()
    # print(f"adafruit_ultimate_gps get_linear_acceleration return value: {adafruit_ultimate_gps_return_value}")
  
    # motorFL
    motor_fl = Motor.from_robot(machine, "motorFL")
    motor_fl_return_value = await motor_fl.is_moving()
    print(f"motorFL is_moving return value: {motor_fl_return_value}")
  
    # motorFR
    motor_fr = Motor.from_robot(machine, "motorFR")
    motor_fr_return_value = await motor_fr.is_moving()
    print(f"motorFR is_moving return value: {motor_fr_return_value}")
    
    # motorBL
    motor_bl = Motor.from_robot(machine, "motorBL")
    motor_bl_return_value = await motor_bl.is_moving()
    print(f"motorBL is_moving return value: {motor_bl_return_value}")
  
    # motorBR
    motor_br = Motor.from_robot(machine, "motorBR")
    motor_br_return_value = await motor_br.is_moving()
    print(f"motorBR is_moving return value: {motor_br_return_value}")

    # PCA9685
    pca_9685 = Board.from_robot(machine, "PCA9685")
    pca_9685_return_value = await pca_9685.gpio_pin_by_name("16")
    print(f"PCA9685 gpio_pin_by_name return value: {pca_9685_return_value}")
  
    # bolt_base
    bolt_base = Base.from_robot(machine, "bolt_base")
    bolt_base_return_value = await bolt_base.is_moving()
    print(f"bolt_base is_moving return value: {bolt_base_return_value}")
  
    # Logitech-C920
    logitech_c_920 = Camera.from_robot(machine, "Logitech-C920")
    logitech_c_920_return_value = await logitech_c_920.get_image()
    print(f"Logitech-C920 get_image return value: {logitech_c_920_return_value}")
  
    # XBOX_controller
    xbox_controller = Controller.from_robot(machine, "XBOX_controller")
    xbox_controller_return_value = await xbox_controller.get_controls()
    print(f"XBOX_controller get_controls return value: {xbox_controller_return_value}")
  
    # movement_sensor-2_fake
    movement_sensor_2_fake = MovementSensor.from_robot(machine, "movement_sensor-2_fake")
    movement_sensor_2_fake_return_value = await movement_sensor_2_fake.get_linear_acceleration()
    print(f"movement_sensor-2_fake get_linear_acceleration return value: {movement_sensor_2_fake_return_value}")

    # detectionCam
    detection_cam = Camera.from_robot(machine, "detectionCam")
    detection_cam_return_value = await detection_cam.get_image()
    print(f"detectionCam get_image return value: {detection_cam_return_value}")
  
    # make sure that your detector name in the app matches "myPeopleDetector"
    myPeopleDetector = VisionClient.from_robot(machine, "myPeopleDetector")
    # make sure that your camera name in the app matches "my-camera"
    my_camera = Camera.from_robot(robot=machine, name="Logitech-C920")
    


    while True:
        img = await my_camera.get_image(mime_type="image/jpeg")
        detections = await myPeopleDetector.get_detections(img)

        found = False
        for d in detections:
            if d.confidence > 0.7 and d.class_name.lower() == "person":
                # Console output indicating that a runner was spotted.
                print("I see a potential runner!")
                found = True
        if found:
            # Console output indicating when the runner was identified and timestamps the event.
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} - Runner Detected!")
            
            # Execute Motivation Demotivation 1000 Algorithm
            subprocess.run(['python', 'motivator_demotivator_1000.py'])

            # Saves an image of the runner
            img.save('./found_img/foundyou.jpeg')
                       
            # Sleeps for 10 secs to help avoid DeMo'ing the same runner more than once in 10 secs
            await asyncio.sleep(10)
        else:
            print("There's nobody here, don't send a message")
            await asyncio.sleep(10)
    await asyncio.sleep(5)


    # Don't forget to close the machine when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
