For the uninitiated user's eyes only:

Step 1: Opening the Window, throwing out the Mac and letting Ubuntu in
Take the almighty flashdisk created by the one and only Brad Minch
(seriously thank you Brad so much, I hope you appreciate my humour)
and plug it into the computer. Restart it and press F12 the moment you see
the Dell(whatever your computer brand is) logo until you see words pop out on
the top right corner of the screen. Then select the Sandisc option when asked which 
OS to boot on. This should get your Linux running. Select "elecanisms" user and type
__mechatronics__ into the password.

Step 2: Walking down the path already traversed
Clone the repository from the github account of elecanism : https://github.com/OlinElecanisms/src
Open the command prompt and using the cd command, head down the path to where you cloned 
the repository. Open the blinkpoll folder and run scons3 in the terminal. This will build 
and compile your blink.c file into a hex file which can finally be understood by the 
microcontroller (machines need translators too). Then we go back to the main file in src,
and open the bootloader folder, open the software folder and run python3 bootloadergui.py.
Then hold down the black button next to the red one to allow communication between your computer 
and the elecanism board. Then you import the hex file created a few seconds ago.
You should see a Write button. Hit it. This will upload your code to the microcontroller.
You should see the green LED blink every 0.5seconds, and the red and blue LEDs depending on
whether you clicked the other buttons.

Step3: Change the code and get your coin detector working
Set your coin detector to recognise pennies. Connect the coin plug-in to any digital pin. 
Amend your code such that the board will continually search for a pulse in the digital pin 
you have used. The moment the board senses the pulse, make the LED light up and then go off.
Repeat the steps taken in Step 2.

Created by Jun Kaih. but you can call me JK or Kaih