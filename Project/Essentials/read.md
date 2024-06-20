Step 1. Install pyvenv (it manipulates dep. only, unlike anaconda)
sudo apt install python3.8-venv

Step 2. Create virtual env
python -m venv your_env_name

Then you can find a "directory" named your_env_name

Step 3. Turn on your virtual env. If you want to exit, then just type deactivate
source your_env_name/bin/activate 

Step 4. Install pkgs listed in req.txt. Please note that RASA is not yet included in req.txt due to not free space error in my system......
pip install -r req.txt

Step 5. Check the followings are running
python Face.py (opencv && dlib)
python behavior_realizer.py (qibullet and gtts, pydub, etc)


Following is the first order dependencies. Again, RASA is not installed yet due to not free space error in my system. 
1. numpy
2. pybullet
3. qibullet
4. pydub
5. gtts
6. pyagrum
7. opencv-python
8. dlib

9. RASA
