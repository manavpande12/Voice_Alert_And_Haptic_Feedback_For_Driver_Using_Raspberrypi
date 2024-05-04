# Voice_Alert_And_Haptic_Feedback_For_Driver_Using_Raspberrypi
![IMG-20231223-WA0019](https://github.com/manavpande12/Voice_Alert_And_Haptic_Feedback_For_Driver_Using_Raspberrypi/assets/143897253/83dbf640-eb71-4f70-b904-e83d786ba3da)


*Introduction:

As we have observed in expensive vehicles, 
the sensors detects drowsiness and stops 
the vehicle in the middle of the road or find 
the suitable place to stop the car, in case of 
high population country like india there is 
many factor on a road that can’t be 
detected and in highways if the car stop in 
middle of road  which is dangerous as 
another vehicle may collide with it.  
Therefore, alert system is important to 
make the driver more alert while driving so 
the accidents can be prevent.


*EQUIPMENT:

• Raspberry Pi  

• Web Camera/PI Camera  

• Speaker 

• Vibration Motor DC 

• Motor Driver L298n 

• Power Supply 


Library To Install 
1. OpenCV:-  
• https://youtu.be/QRe0QzS079s?si=YWvUTqrfQ48OACs7

• https://docs.opencv.org/4.x/d2/de6/tutorial_py_setup_in_ubuntu.html 

3. Dlib:-   
• https://youtu.be/uF4aDdxBm_M?si=iCCw4UM3ZvNQoVK-

• sudo nano /etc/dphys-swapfile  
• sudo /etc/init.d/dphys-swapfile stop  
• sudo /etc/init.d/dphys-swapfile start  
• free -m  
• sudo raspi-config  
• sudo apt-get update  
• sudo apt-get install build-essential cmake  
• sudo apt-get install libgtk-3-dev  
• sudo apt-get install libboost-all-dev  
• wget https://bootstrap.pypa.io/get-pip.py  
• sudo python3 get-pip.py  
• pip3 install numpy  
• pip3 install dlib

5. Python3 
6. Imutils 
7. Pygame 
8. face_utils 
9. scipy
10. Rpi.GPIO:- sudo apt install rpi-gpio-common 
11. time 
12. os 
13. pip3 
14. numpy 

*Resolution 
1. 256x144 

*How to Turn On PICAMERA() – sudo libcamera-hello/libcamera-hello 
1. sudo raspi-config 
2. On Legacy Camera 
3. On Full KMS 
4. ON Glamor 
5. Then Reboot 
6. Sudo su 
7. Sudo nano /boot/config.txt 
8. #start_x=1 
9. #camera_auto_detect=1 
10. Set Gpu_mem= 256 

*How To Set Audio As A Default From Config ? 
1. sudo nano /etc/asound.conf 
2. Set Value As Per Port – alsamixer 

• defaults.pcm.card 1 

• defaults.pcm.card 1 


*Conclusiom

In our model, we apply a logic where the camera continuously track the 
driver's eyes.  
If the driver closes their eyes for more than 2 seconds, indicating a state 
of  drowsiness, or if the driver consistently keeps their eyes open for 
more than 10 seconds, indicating a state of hypnosis.  
If either of the two conditions is true, the system will activate an voice 
alert message, and a vibration motor will generate haptic feedback on the 
steering. 
With the help of this mechanism ,the driver willl snap out from hypnosis 
or drowsinees state ,overall it will  heightened awareness and it will 
create a safer environment for driver ,passsenger and the family.








