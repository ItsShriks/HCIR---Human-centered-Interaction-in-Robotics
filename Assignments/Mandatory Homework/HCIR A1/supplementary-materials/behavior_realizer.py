from collections import Counter
from qibullet import SimulationManager
import gtts
from playsound import playsound
import threading

class BehaviorRealizer():

    def __init__(self):
        # Loading Robot and  Ground
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    


if __name__ == "__main__":

    behavior_realizer_class = BehaviorRealizer()  
    #TODO: Implement necessary code for robot behaviours 
    
    INPUT_OPTIONS=["done"]
        
    repeat_ = True
    while repeat_:
        user_input = input("INPUT : ")
        
        if str(user_input)==INPUT_OPTIONS[0]:
            repeat_=False
        
        if not user_input in INPUT_OPTIONS:
            print("Please enter 'done' to exit.")
        
