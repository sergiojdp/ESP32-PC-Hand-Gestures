# 🤖 ESP32-PC-Hand-Gestures

This project connects an **ESP32** board to a personal computer to establish a communication channel based on hand gestures. It uses the ESP32's camera to interpret gestures and translate them into spoken commands or actions on the PC.

## 🎯 Objective

To create a natural and accessible interface where hand gestures are converted into language. The main goal of the project is to build a portable device that allows mute individuals to communicate through gestures using built-in speakers.

## 🧠 How It Works

1. The ESP32 camera captures hand gestures.
2. The system interprets the gestures using computer vision algorithms.
3. The gestures are translated into commands sent to the PC.
4. The PC can respond with actions or even synthesized speech back to the **ESP32**.

## 🛠 Technologies Used

- **ESP32-CAM** for image capture  
- **Python** on the PC to receive and process commands  
- **Serial or Wi-Fi** as the communication channel  
- Gesture recognition algorithms (including OpenCV and MediaPipe)

## 🔮 Upcoming Updates

In future versions, I plan to refine the hand gestures currently being detected, as the ones included so far are provisional and were added mainly for testing purposes. My goal is to assign a unique gesture to each letter of the alphabet, so that they can later be vocalized through the built-in speakers. This will allow for more expressive and complete communication, especially for individuals who rely on gesture-based interaction.


