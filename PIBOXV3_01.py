import time
from PIJoystick import PIJoystick
from pipython.pidevice.interfaces.piserial import PISerial
from pipython.pidevice.gcsmessages import GCSMessages
from pipython.pidevice.gcscommands import GCSCommands
from Color_Ball_Detection import Auto_Solver
from Camera import VideoGet
#MACRO STATE GUIDE
#    MACRO = -2 : Analog Maze Mode
#    MACRO = -1 : Controller Autostarted Motion Mode
#    MACRO = 0  : Open state
#    MACRO = 1  : Motion Mode
#    MACRO = 2  : Auto Maze Mode

def QUIT(device):
    device.StopAll(noraise = True)
    time.sleep(2)
    device.MAC_START("QUIT2")
    time.sleep(2)

def main():
    time.sleep(1)#35)
    gateway = PISerial("/dev/ttyUSB0", 115200)
    messages = GCSMessages(gateway)
    c887 = GCSCommands(gcsmessage=messages)
    joy = PIJoystick()
    AXES = ["X", "Y", "Z", "U", "V", "W"]
    HOME = [0, 0, 0, 0, 0, 0]
    TRANSPORT = [0, 0, 0, 0, 0, 2.2]
    MACRO = -1
    LASTMACRO = -1
    LASTJOYSTATE = [0,0,0,0,0]
    while 1:
        time.sleep(0.1)
        joystate = joy.read()
        if MACRO == 1 or MACRO == 2 or MACRO == -1:
            try:
                if c887.IsRunningMacro() == 1:
                    joystate = joy.read()
                    if (MACRO == 2 or MACRO == -1) and joystate[2] == 1 and joystate[3] == 0 and joystate[4] == 0 and LASTJOYSTATE[2] == 0:
                        QUIT(c887)
                        LASTMACRO = MACRO
                        MACRO = 0
                    elif (MACRO == 1 or MACRO == -1) and joystate[2] == 0 and joystate[3] == 1 and joystate[4] == 0 and LASTJOYSTATE[3] == 0:
                        QUIT(c887)
                        LASTMACRO = MACRO
                        MACRO = 0
                    elif (MACRO == -1) and joystate[2] == 0 and joystate[3] == 0 and joystate[4] == 1 and LASTJOYSTATE[4] == 0:
                        QUIT(c887)
                        LASTMACRO = MACRO
                        MACRO = 0
                else:
                    MACRO = 0
            except:
                continue
        else:
            joystate = joy.read()
            if MACRO == -2:
                if joystate[1] < 0.08 and joystate[1] > -0.08:
                    joystate[1] = 0
                if joystate[0] < 0.08 and joystate[0] > -0.08:
                    joystate[0] = 0
                try:
                    while(c887.qSPI()['R'] != 0 or c887.qSPI()['S'] != 0 or c887.qSPI()['T'] != 0):
                        c887.SPI(["R","S","T"],[0,0,0])
                    c887.MOV(AXES, [0,0,0,-9*joystate[0],9*joystate[1],0])
                except:
                    continue
                if joystate[0] < -0.8 and joystate[4] == 1:
                    try:
                        c887.MOV(AXES, [0,0,0,14,0,0])
                    except:
                        continue
                    time.sleep(1)
            elif joystate[4] == 1 and joystate[3] == 0 and joystate[2] == 0:
                MACRO = -2
            if joystate[3] == 1 and joystate[4] == 0 and joystate[2] == 0 and LASTJOYSTATE[3] == 0:
                time.sleep(0.5) # found to be needed when print statements are removed, seems a minor race condition exists 
                if joystate[0] > 0.8: # without the delay an error is sometimes seen
                    try:
                        c887.MOV(AXES, TRANSPORT)
                    except:
                        continue
                    time.sleep(15)
                MACRO = 1
                try:
                    c887.MAC_START("MOTION")
                except:
                    continue
            if joystate[2] == 1 and joystate[3] == 0 and joystate[4] == 0 and LASTJOYSTATE[2] == 0:
                time.sleep(0.5) # found to be needed when print statements are removed, seems a minor race condition exists 
                MACRO = 2       # without the delay an error is sometimes seen
                try:
                    Auto_Solver(joy,c887)
                except:
                    continue
        LASTJOYSTATE = joystate
    
if __name__ == '__main__':
    main()
