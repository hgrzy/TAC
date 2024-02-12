import pyvisa as visa
import time
from datetime import datetime



very_first_time = time.time()
visa_address='TCPIP::169.254.70.80::INSTR' #address of scope

#these set communications with the scope
rm = visa.ResourceManager()
scope = rm.open_resource(visa_address)
scope.timeout = 100000 # ms
scope.encoding = 'latin_1'
scope.read_termination = '\n'
scope.write_termination = None
scope.write('*cls') # clear ESR
scope.write('header OFF') # disable attribute echo in replies
print(scope.query('*idn?'))
# default scope setup
scope.write('*rst')


r = scope.query('*opc?') # sync
scope.write('trigger:a:level:ch1 0.8') 


def pre_processer_ch1():
    """
        pre_processer_ch1
        Sends commands to scope to turn on CH1, dynamically adjust the vertical scale to contain the ,waveform
        and sets horizontal scaling for all channels (since can only have one horizontal scaling) such that
        10% of the screen is to the left of the trigger on CH1.
    """
    #turns on ch and display 
    scope.write('display:global:ch1:state ON') #turns on channels
    scope.write("CH1:TERMINATION 50.0E+0") #sets ch1 input impedance to 50 ohms
    scope.write("CH1:BANdwidth 2.5E+9") #sets ch1 bandwidth limit to 2.5 GHz
    scope.write("MEASUREMENT:MEAS1:TYPE MAXIMUM") #actively measure max for current channel
    scope.write('CH1:SCALE 2') #changes y scaling to 2 v/div

    time.sleep(1) #need this after setting y scale otherwise osc doesn't have enough time to register

    #takes 'screenshot' of ch1
    scope.write("ACQUIRE:STATE 0") #stop taking data
    scope.write("ACTONEVent:ENable 1") #allow for taking data when triggered
    scope.write("ACQUIRE:Sequence:Numsequence 1") #only take 1 data set- doesnt take the data set now just sets this for later
    scope.write("ACQUIRE:Stopafter sequence") #start taking data only for numsequence amount of data sets- prev set 
    # time.sleep(1)

    #calcs new div for ch1 so signal max is at 80% of window
    test_max1 = float(scope.query("MEASUrement:MEAS1:RESUlts:CURRentacq:Maximum?")) #get current max for channel 1
    test_div1 = test_max1/3 #divisions on vscale ch1

    #sets new divs
    scope.write('CH1:SCALE {}'.format(test_div1)) #changes y scaling to test_div1 v/div
    time.sleep(1)#need this after setting y scale otherwise osc doesn't have enough time to register

    #horizontal adjustments (only need to do this on one channel bc they share horizontal axis)
    scope.write("Horizontal:Position 10") #make 10% of screen appear to left of trigger of CH1

    scope.write("HOR:MOD MAN") #sets horizontal mode to manual to allow for setting window based on record length
    scope.write("HOR:MOD:SAMPLER 6.25e9") #sets sample rate to 6.25e9 Hz
    scope.write("HOR:MOD:RECO 10000") #records 10,000 samples, when you change record lenght the horizontal scale also changes




def pre_processer_ch2():
    """
        pre_processer_ch2
        Sends commands to scope to turn on CH2 and dynamically adjust the vertical scale to contain the waveform.
    """

    #turns on ch and display 
    scope.write('display:global:ch2:state ON') #turns on channels
    scope.write("ACQUIRE:STATE 1")
    scope.write("CH2:TERMINATION 50.0E+0") #sets ch2 input impedance to 50 ohms
    scope.write("CH2:BANdwidth 2.5E+9") #sets ch2 bandwidth limit to 2.5 GHz
    scope.write("MEASUREMENT:MEAS2:TYPE MAXIMUM") #actively measure max for current channel
    scope.write('CH2:SCALE 2') #changes y scaling to 2 v/div

    time.sleep(1)#need this after setting y scale otherwise osc doesn't have enough time to register

    #takes 'screenshot' of ch2
    scope.write("ACQUIRE:STATE 0") #stop taking data
    scope.write("ACTONEVent:ENable 1") #allow for taking data when triggered
    scope.write("ACQUIRE:Sequence:Numsequence 1") #only take 1 data set- doesnt take the data set now just sets this for later
    scope.write("ACQUIRE:Stopafter sequence") #start taking data only for numsequence amount of data sets- prev set 
    # time.sleep(1)

    #calcs new div for ch2 so signal max is at 80% of window
    test_max2 = float(scope.query("MEASUrement:MEAS2:RESUlts:CURRentacq:Maximum?")) #get current max for channel 2
    test_div2 = test_max2/3 #divisions on vscale ch2

    scope.write('CH2:SCALE {}'.format(test_div2)) #changes y scaling to test_div2 v/div
    time.sleep(1)#need this after setting y scale otherwise osc doesn't have enough time to register



def pre_processer_ch3():
    """
        pre_processer_ch3
        Sends commands to scope to turn on CH3 and dynamically adjust the vertical scale to contain the waveform.
    """

    #turns on ch and display 
    scope.write('display:global:ch3:state ON') #turns on channels
    scope.write("ACQUIRE:STATE 1")
    scope.write("CH3:TERMINATION 50.0E+0") #sets ch3 input impedance to 50 ohms
    scope.write("CH3:BANdwidth 2.5E+9") #sets ch3 bandwidth limit to 2.5 GHz
    scope.write("MEASUREMENT:MEAS3:TYPE MAXIMUM") #actively measure max for current channel
    scope.write('CH3:SCALE 2') #changes y scaling to 2 v/div

    time.sleep(1)#need this after setting y scale otherwise osc doesn't have enough time to register

    #takes 'screenshot' of ch3
    scope.write("ACQUIRE:STATE 0") #stop taking data
    scope.write("ACTONEVent:ENable 1") #allow for taking data when triggered
    scope.write("ACQUIRE:Sequence:Numsequence 1") #only take 1 data set- doesnt take the data set now just sets this for later
    scope.write("ACQUIRE:Stopafter sequence") #start taking data only for numsequence amount of data sets- prev set 
    # time.sleep(1)

    #calcs new div for ch3 so signal max is at 80% of window
    test_max3 = float(scope.query("MEASUrement:MEAS3:RESUlts:CURRentacq:Maximum?")) #get current max for channel 3
    test_div3 = test_max3/2 #divisions on vscale ch3

    #sets new divs
    scope.write('CH3:SCALE {}'.format(test_div3)) #changes y scaling to test_div3 v/div
    time.sleep(1)#need this after setting y scale otherwise osc doesn't have enough time to register

    

def save_set_up():
    """
    save_set_up()
    Creates and switches to a directory on the oscilloscope to save data.
    """

    #get today's date
    todays_date = datetime.now()
    readable_todays_date = todays_date.strftime("%d_%m_%Y_impulse_measurements")

    scope.write("FILESYSTEM:CWD \"Hannah\"")
    #make directory with today's date on oscilloscope in home directory
    if readable_todays_date not in scope.query("FILESystem:LDir?"):
        cmd_mk_date_dir = "FILESystem:MKDir \"{}\"".format(readable_todays_date)
        scope.write(cmd_mk_date_dir)

    #change into date directory
    cmd_cd_date = "FILESystem:CWD \"{}\"".format(readable_todays_date)
    scope.write(cmd_cd_date)
    datedir = scope.query("FILESystem:CWD?")


    #request name of subdirectory from user (e.g. taking impulse measurements = probably good to input 'angle##')
    subdir_name = input("Input your subdirectory name then press enter:")
    if subdir_name in scope.query("FILESystem:LDir?"):
        subdir_name = input("This directory already exists. Input your subdirectory name then press enter:")

    #make subdirectory on oscilloscope
    cmd_mk_sub = "FILESystem:MKDir \"{}\"".format(subdir_name)
    scope.write(cmd_mk_sub)

    #change into subdirectory
    cmd_cd_sub = "FILESYstem:CWD \"{}\"".format(subdir_name)
    scope.write(cmd_cd_sub)

    save_dir = scope.query("FILESYstem:CWD?")
    return save_dir

def home_dir_save():
    """
    home_dir_save()
    Saves data to home directory on oscilloscope.
    """
    scope_home_dir = scope.query("FILESystem:HOMEDir?") #get home directory of the scope
    cmd_swt_home = "FILESystem:CWD {}".format(scope_home_dir) #dont need quotes around brackets bc obtained with query in scope_home_dir
    scope.write(cmd_swt_home) #switch to home directory if not already there
    save_dir = save_set_up()
    return save_dir

def ext_drv_save():
    """
    ext_drv_save()
    Saves data to directory on external or usb drive plugged into usb 3.0 on oscilloscope.
    """
    scope.write("FILESYSTEM:CWD \"E:\"")
    save_dir = save_set_up()
    return save_dir


def main():

    #set up windows
    pre_processer_ch1()
    pre_processer_ch2()
    pre_processer_ch3()

    #set save paths
    # save_dir = ext_drv_save()
    save_dir = home_dir_save()

    

    #set file save destination and format
    cmd_save_dest = 'SAVEONEvent:FILEDest {}'.format(save_dir) #dont need quotes around brackets bc strings from query already include
    scope.write(cmd_save_dest)
    file = scope.query("SAVEONEvent:FILEDest?")
    print("FIle destination: {}".format(file))
    scope.write('SAVEONEvent:WAVEform:FILEFormat SPREADSHEET') #save in csv format
    how_save = scope.query('SAVEONEvent:WAVEform:FILEFormat?')
    print(how_save)
    time.sleep(1)
    scope.write('SAVEONEvent:WAVEform:SOURce ALL') #save data from all channels

    #setting acquisition settings
    scope.write("ACQUIRE:STATE 0") #turn off collecting data to set following settings
    scope.write("ACTONEVent:ENable 1") #allows osc to do things when an event occurs
    scope.write("ACTONEVent:TRIGger:ACTION:SAVEWAVEform:STATE ON") #tells osc to save waveform when triggered

    num_wvfrms = input("Input integer number of waveforms then press enter: ")
    cmd_numseq = ("ACQUIRE:Sequence:Numsequence {}".format(num_wvfrms))
    scope.write(cmd_numseq) #setting that takes num_wvfrms number of "snapshots"
    # time.sleep(1)
    scope.write("ACQUIRE:Stopafter sequence") #setting that says use sequence setting instead of continuous data collection- tells osc to stop taking data after capturing seq
    # time.sleep(1)

    b4_acquire = time.time() #gets start time of data acquisition
    scope.write("ACQUIRE:STATE 1") #start taking data


    #while loop to time how long to take data
    while scope.query("ACQUIRE:STATE?") == "1": #see if data taking is on
        pass

    end_time = time.time() #gets end time of data acquisition

    total_time = end_time - very_first_time #time for entire script to run
    acq_time = end_time - b4_acquire #time for data acquisition to run

    print("Number of Waveforms: {}".format(num_wvfrms))
    print("Acquisition time: {}".format(acq_time))
    print("Total time: {}".format(total_time))

main() #runs this script whenever this file is called
