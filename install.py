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
        # check platform.freedesktop_os_release() to try and detect with distribution the user is using
        platform_info = platform.freedesktop_os_release()
        # if ID contain arch Arch endeavouros manjaro artix use pacman
        if "arch" in platform_info["ID"] or "endeavouros" in platform_info["ID"] or "manjaro" in platform_info[
            "ID"] or "artix" in platform_info["ID"] or "arch" in platform_info["ID_LIKE"]:
            launch.run("sudo pacman -S aria2", "Installing requirements for Model Downloader")
        else:
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
