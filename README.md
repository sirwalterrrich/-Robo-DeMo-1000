
# Robo-DeMo-1000

This project centers around a 4 wheeled robot that follows or leads distance runners. It identifies other runners by use of computer vision and then proceeds to either start motivating or demotivating the other identified runners through speech audio by leveraging text to speech AI services and computer vision ML models.

https://github.com/sirwalterrrich/-Robo-DeMo-1000/blob/main/HUD-RoboDeMo1000/templates/robot-runner-hud.png


## Screenshots

![App Screenshot](https://github.com/sirwalterrrich/-Robo-DeMo-1000/blob/main/HUD-RoboDeMo1000/templates/robot-runner-hud.png)

Author : Sir Walter R. - April 20, 2024
Script Name - main.py 
 Project Title: Robo DeMo 1000

This script started from the Viam (viam.com) python code sample generated after all the components were added to the configuration in the Viam web app.

The code supports a robot base. The robot base has a RaspberryPi 5, PCA9685 (PWM), 

Motor controllers, 4 motors, a USB camera, USB soundcard, Audio Ampplifier and Audio speaker, and wireless XBOX controller

# Remote Control
This feature is achieved by using Viams built-in features.

# Text to Speech
This feature is achieved by leveraging Eleven Labs API
This main.py script calls another script called motivator_demotivator_1000.py. It implements the AI Text to Speech.

This motivator_demotivator_1000.py script uses the ElevenLabs API for speech to text generation and pygame libraries for audio output.

# Computer Vision - Runner Detection
Computer Vision is achieved by using Viam's built-in CV/ML features

A People Detector was developed to trigger on people. Vision -> mlmodel

Future work0: Custom head up display using a Flask Web App - Started on this 4/20/24

Future work1: Add wireless remote control via an ESP32 Microntoller- Start and stop ESTOP function, instant jokes etc.

Future work2: Use ChatGPT to respond to speech shouted at the robot.

Future work3: I hope to use Computer Vision facial recognition models to trigger the type of selected messages.
               For example, if the person looks super stressed during a run then tell them something motivational or funny.

Future work4: Save the output.mp3 files for later use to save on bandwidth and ElevenLabs API Usage.

Future work5: Implement the Viam 'navigation service' using a GPS module and IMU (9 axis accelerometer).

Future work6: Use VIAM builtin computer vision to identify path markings for navigation and obstacle avoidance.

Future work7: Implement status RGB LEDs using the Neopixel library. The RPI5 currently does not support the Neopixel library due to a hardware change.
                # This feature could be implement using an Arduino or other microcontroller but i'm short on time. 
                # Things to indicate using Neopixel LEDs. Network Status / Direction travel / Processor Heartbeat / an attraction pattern to bring curious runners closer to the camera
 

## Features

motivator_demotivator_1000.py

This script uses the ElevenLabs AI voice service to generate speech from text.

The text come from lists(motivations, demotivations, motivations2 ) of AI generated phrases (chatGPT)
that would either motivate or demotivate a distance runner.

Once executed, the messaging is at random. A random message from the list will be selected to be played. 
The script saves the audio file as output.mp3

# Future work: 
I hope to use Computer Vision facial recognition models to trigger the type of selected messages.

For example, if the person looks super stressed during a run then tell them something motivational or funny.

Future work: Save the output.mp3 files for later use to save on bandwidth and ElevenLabs API Usage.

This script uses the ElevenLabs API for speech to text generation and pygame libraries for audio output.
 


## Authors

- [@sirwalterrrich](https://www.github.com/sirwalterrrich)


## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)


## Lessons Learned

What did you learn while building this project? What challenges did you face and how did you overcome them?

Lots of challenges were faced on this project. More to come...

