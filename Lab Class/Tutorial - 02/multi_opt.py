import concurrent.futures
import time
from gtts import gTTS
from playsound import playsound

def speak_hello():
    tts = gTTS("Hello")
    tts.save("hello.mp3")
    playsound("hello.mp3")
    time.sleep(6)  # Run for 6 seconds

def print_hello():
    print("Printing: Hello")
    time.sleep(6)  # Run for 6 seconds

def print_thank_you():
    print("Printing: Thank you")
    time.sleep(5)  # Run for 5 seconds

def speak_callback(future):
    print("Speaking: Hello has ended.")

def print_callback(future):
    print("Printing: Hello has ended")

def thank_you_callback(future):
    print("Printing: Thank you has ended.")

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Schedule speak_hello to run
        future_speak = executor.submit(speak_hello)
        future_speak.add_done_callback(speak_callback)

        # Schedule print_hello to run along with speak_hello
        future_print = executor.submit(print_hello)
        future_print.add_done_callback(print_callback)

        # Schedule print_thank_you to run after 4 seconds of speak_hello
        time.sleep(4)
        print("4 seconds have passed.")
        future_thank_you = executor.submit(print_thank_you)
        future_thank_you.add_done_callback(thank_you_callback)

        # Wait for the tasks to complete individually
        for future in concurrent.futures.as_completed([future_speak, future_print, future_thank_you]):
            pass # wait for the threads to complete
