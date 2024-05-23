#!/usr/bin/env python
# coding: utf-8

import time
import concurrent.futures
from qibullet import SimulationManager
from qibullet import PepperVirtual
from gtts import gTTS
from playsound import playsound

def wave():
    try:
        # Create a simulation manager and launch the simulation
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        
        # Spawn a Pepper robot in the simulation and move it to the initial posture
        pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
        pepper.goToPosture("Crouch", 0.6) 
        time.sleep(1)
        pepper.goToPosture("StandInit", 0.6) 
        time.sleep(1)

        # Perform waving motion
        for _ in range(5):  # Loop to wave 5 times
            pepper.setAngles("RShoulderPitch",-0.5,0.5) #
            pepper.setAngles("RShoulderRoll",-1.5620, 0.5) 
            pepper.setAngles("RElbowRoll",1.5620,0.5)
            time.sleep(1.0) 
            pepper.setAngles("RElbowRoll",-1.5620,0.5)
            time.sleep(1.0)
    finally:
        # Stop the simulation when waving motion is completed or in case of an error
        simulation_manager.stopSimulation(client)

def speak():
    # Delay before starting to speak (6 seconds as specified)
    time.sleep(6)
    
    # Generate spoken message and play it
    tts = gTTS("Hello, welcome to Masters of Autonomous Systems")
    tts.save("message.mp3")
    playsound("message.mp3")
    
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Schedule wave and speak functions to run concurrently
        future_wave = executor.submit(wave)
        future_speak = executor.submit(speak)

        # Wait for both tasks to complete
        concurrent.futures.wait([future_wave, future_speak])
