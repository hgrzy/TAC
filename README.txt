Tektronix Acquisition Code (TAC) README 

07 February 2024

This script is used to collect data on 3 channels for the Tektronix Multi Source Oscilloscope (MSO) Series 6 via ethernet. The code follows the script in the 4-5-6-Series-MSO-Programmer_077130521.pdf Programmer manual provided by Tektronix. 


Notes on Tektronix Programmer Manual:
    - Many commands will not run without using another function in conjunction with it
        e.g. 
            scope.write("ACQUIRE:Sequence:Numsequence 1") #only take 1 data set
            scope.write("ACQUIRE:Stopafter sequence") #start taking data only for numsequence amount of data sets- prev set
      If a command is not working then you are likely missing a command's pair (maybe more).

 
    - TIMING IS VERY VERY VERY IMPORTANT. VERY.
        Python tends to run faster than the oscilliscope can execute commands. Due to this, sometimes your settings will not be executed on the oscilloscope. In this case, you may get odd default values returned to you when you later query these settings (e.g. scope.query("MEASUrement:MEAS1:RESUlts:CURRentacq:Maximum?") returns ~9.9e37 if you do not put a sleep after the scaling setting). We've also had an unexpected number of images back when not considering timing. Bottom line: if you get unexpected results try more dead time after sending commands to the oscilloscope. 

    - Capitalization of commands sent to oscilloscope do not matter. 
        Per the manual, the capitalization just indicates you can use only the capital letters as an abbreviated statement of the full command.

    - Measurement commands are very specific.
        If you try incorrect arguments with the measurement commands, your oscilloscope and computer will become out of sync. You can tell this happens because the code gets caught, doesn't time out, and trying to run another terminal that connects to the oscilloscope will give you a pyvisa error about not being able to connect and timing out. We've only found that restarting the oscilloscope and the computer remedies this issue.

    - You're sending settings TO THE OSCILLOSCOPE
        An important thing to remember is that you're sending commands TO and running commands ON the oscilloscope. This is how we are able to have looping behavior without having an actual for-loop in python. 

    - To change horizontal settings you need to enter into horizontal manual mode

    - The Horizontal Scale and Sample Rate have specific values they can be, they can't be just anything