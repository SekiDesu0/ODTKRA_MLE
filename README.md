# ODTKRA_MLE
Uses the Oculus Debug Tool to keep your rift from going to sleep

I made this to keep my rift from going to sleep while using mm0zct's Oculus_Touch_Steam_Link Driver

Instructions:
- Download the exe file in releases.

- Run exe after starting Touch Link or Driver4VR (depending on what software you are running)

- Let ODTKRA_MLE do its thing, it will contantly check if the Oculus Debug Tool memory usage is too high and try to kill it.

- Your headset will now not go to sleep, if it does, restart ODTKRA_MLE.

Launch Options:

- --odt-path ``--odt-path [Oculus Diagnostics Directory]``
  - Example ``--odt-path "C:\\Program Files\\Oculus\\\Support\\\oculus-diagnostics\\"``
 
- --leak-size ``--leak-size [amount of memory in MB ODTKRA_MLE detects as a memory leak]``
  - Example ``--leak-size 750``
 

You can also add launch options by creating a shortcut, right clicking on it and going into properties and adding it here

![Path Image](/Images/odt-path.png)
