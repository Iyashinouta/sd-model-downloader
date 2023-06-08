import launch
import platform

if platform.system() == "Windows":
   if not launch.is_installed("aria2"):
      launch.run_python("apt -y install -qq aria2", "requirements for Model Downloader")
   if not launch.is_installed("wget"):
      launch.run_pip("install wget", "requirements for Model Downloader")
