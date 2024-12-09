#PingSweeper project. 

this is a Python program, designed to ping a subnet. scan for open ports defined with following archuments all done via commandline:
  -p      specify ports seperated with a "," 
          example "PingSweep.exe 10.0.0.0/24 -p 21,81,8443"
          this will ping the subnet of 10.0.0.1 to 10.0.0.255 and check if there are open ports on 21, 81 and 8443 on the alive ip addresses. 
  -o      for not printing it in current screen but for outputting it to a file. 
          example "PingSweep.exe 10.0.0.0/24 -o ping.txt"
          this will ping the subnet like above on the ports test. default it will scan for 22, 80 and 443

keep in mind this is a commandline tool only. 

the python file in this repo is the source code aswell. 
only thing done to this python file to create a .exe file for windows is:

- created a .venv in python 3.12.8 with command:
    `python -m venv venv`

- then opend the venv and installed the ping3 library.
    `pip install ping3`

- then i installed pyinstaller.
    `pip install pyinstaller`

- then i created the PingSweep.exe file with command:
    `pyinstaller --onefile PingSweep.py`

A simple small tool which helps detecting certain devices online in your network. if which you might know the ports supposed to be open. 

additional i might try to include a function to show the Vendor id from the devices matched to the ip addresses. 
i made this script purely for my own bennefit of doing my job in a faster way without the use of Java. and share this overhere because i think this might benefit more users ;-) 


    
