import os
import launch
import platform
import subprocess

def checking():
    try:
        subprocess.run("aria2c", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
           return False

if platform.system() == "Linux":
   if not checking():
      launch.run("apt update && apt -y install -qq aria2", "Installing requirements for Model Downloader")
   else:
        pass
elif platform.system() == "Darwin":
     if not checking():
        launch.run("brew install aria2", "Installing requirements for Model Downloader")
     else:
          pass
elif platform.system() == "Windows":
     if not checking():
        print("Model Downloader required aria2c, see tutorial https://www.youtube.com/watch?v=JnWQST4ay_E")
     else:
          pass
