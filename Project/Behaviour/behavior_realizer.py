import time
import threading
import json

from concurrent.futures import ThreadPoolExecutor
from qibullet import SimulationManager
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play



class BehaviorRealizer():

    def __init__(self, behavior):
        # Loading Robot and  Ground
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
        
        # paprika represents a human whom pepper should look at
        paprika = simulation_manager.spawnPepper(client, translation=[2, 1, 0], quaternion=[0, 0, -2, 1], spawn_ground_plane=True)
        
        # load BML from json. stores it in dict
        with open(behavior) as f:
            self.plan = json.load(f)
        
        # parsing configs of modalities from the dict. Each config will be assigned on individual thread
        # the configures are stored in the list, pool  
        pool = self.job_list()
        N = len(pool)
        
        # submit configurations to threadpool
        with ThreadPoolExecutor(max_workers=N) as executor:
            for i in pool:
                executor.submit(*i)

            executor.shutdown()

    # job_list collects multi-modal configurations. The output of the method is submitted to the threadpool. 
    def job_list(self):
        threads = []

        for key in self.plan['bml'].keys():
            for i in self.plan['bml'][key]:
                func = i['id'].split('-')[1]
                start = i['start']
                
                if func == 'speak':
                    func = eval('self.'+func)
                    text = i['text']

                    threads.append([func, start, text])
                    
                else :
                    func = eval('self.'+func)
                    duration = i['duration']

                    threads.append([func, start, duration])
                    
        return threads

    # method for robot speaking
    # it starts after start seconds, it ends after speaking the text
    def speak(self, start, text):
        time.sleep(start)

        chat_stream = BytesIO()
        
        tts = gTTS(text)
        tts.write_to_fp(chat_stream)
        chat_stream.seek(0)

        chat = AudioSegment.from_file(chat_stream, format="mp3")
        play(chat)

    # method for robot waving
    # it starts after start seconds, it runs for duration seconds
    def wave(self, start, duration):
        time.sleep(start)
        
        checkpoint = time.time()

        self.pepper.setAngles('LHand', 0.98, 1.0)
        time.sleep(0.2)
        
        self.pepper.setAngles('LShoulderPitch', -0.9, 1.0)
        time.sleep(0.2)
                
        while True:
            self.pepper.setAngles('LElbowRoll', -0.5, 1.0)
            time.sleep(0.4)
            
            self.pepper.setAngles('LElbowRoll', -0.1, 1.0)
            time.sleep(0.4)

            end = time.time()
            
            if end - checkpoint > duration:
                break

    # method for robot swirl
    # it starts after start seconds, it runs for duration seconds
    def swirl(self, start, duration):
        time.sleep(start)

        checkpoint = time.time()
        
        while True:
            self.pepper.setAngles('HipRoll', -0.2, 1.0)
            time.sleep(0.4)
            
            self.pepper.setAngles('HipRoll', 0.2, 1.0)
            time.sleep(0.4)
            
            end = time.time()
            if end - checkpoint > duration:
                break

    # method for robot gaze
    # it starts after start seconds, it runs for duration seconds
    def look_at(self, start, duration):
        time.sleep(start)

        checkpoint = time.time()

        self.pepper.setAngles('HeadYaw', 0.26, 1.0)
        
        while True:
            
            end = time.time()
            if end - checkpoint > duration:
                
                break

    # method for robot nod
    # it starts after start seconds, it runs for duration seconds
    def nod(self, start, duration):
        time.sleep(start)

        checkpoint = time.time()
        
        while True:
            self.pepper.setAngles('HeadPitch', -0.2, 1.0)
            time.sleep(0.5)
            
            self.pepper.setAngles('HeadPitch', 0.2, 1.0)
            time.sleep(0.5)
            
            end = time.time()
            if end - checkpoint > duration:
                break
    


if __name__ == "__main__":

    behavior_file = 'behavior.json'
    behavior_realizer_class = BehaviorRealizer(behavior_file)  
    #TODO: Implement necessary code for robot behaviours 
    
    INPUT_OPTIONS=["done"]
        
    repeat_ = True
    while repeat_:
        user_input = input("INPUT : ")
        
        if str(user_input)==INPUT_OPTIONS[0]:
            repeat_=False
        
        if not user_input in INPUT_OPTIONS:
            print("Please enter 'done' to exit.")




        