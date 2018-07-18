import os
import time
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1)
time.sleep(1)
import pigpio
import smbus
import math
import PID
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
# These are for the ultrasonic sensor
TRIG = 23
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)


import numpy as np

min_value=700
max_value=2000
#Setting the pins with the ESCs
ESC1=14
ESC2=15
ESC3=4
ESC4=18
pi1 = pigpio.pi();
pi2 = pigpio.pi();
pi3 = pigpio.pi();
pi4 = pigpio.pi();
pi1.set_servo_pulsewidth(ESC1, 0)
pi2.set_servo_pulsewidth(ESC2, 0)
pi3.set_servo_pulsewidth(ESC3, 0)
pi4.set_servo_pulsewidth(ESC4, 0)

def stop(): #This will stop every action your Pi is performing for ESC.
    pi1.set_servo_pulsewidth(ESC1, 0)
    pi2.set_servo_pulsewidth(ESC2, 0)
    pi3.set_servo_pulsewidth(ESC3, 0)
    pi4.set_servo_pulsewidth(ESC4, 0)
    pi1.stop()
    pi2.stop()
    pi3.stop()
    pi4.stop()

def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi1.set_servo_pulsewidth(ESC1, 0)
    pi2.set_servo_pulsewidth(ESC2, 0)
    pi3.set_servo_pulsewidth(ESC3, 0)
    pi4.set_servo_pulsewidth(ESC4, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi1.set_servo_pulsewidth(ESC1, max_value)
        pi2.set_servo_pulsewidth(ESC2, max_value)
        pi3.set_servo_pulsewidth(ESC3, max_value)
        pi4.set_servo_pulsewidth(ESC4, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = raw_input()
        if inp == '':
            pi1.set_servo_pulsewidth(ESC1, min_value)
            pi2.set_servo_pulsewidth(ESC2, min_value)
            pi3.set_servo_pulsewidth(ESC3, min_value)
            pi4.set_servo_pulsewidth(ESC4, min_value)
            print "Wierd eh! Special tone"
            time.sleep(7)

 print "Wait for it ...."
            time.sleep (5)
            print "Im working on it, DONT WORRY JUST WAIT....."
            pi1.set_servo_pulsewidth(ESC1, 0)
            pi2.set_servo_pulsewidth(ESC2, 0)
            pi3.set_servo_pulsewidth(ESC3, 0)
            pi4.set_servo_pulsewidth(ESC4, 0)
            time.sleep(2)
            print "Arming ESC now..."
            pi1.set_servo_pulsewidth(ESC1, min_value)
            pi2.set_servo_pulsewidth(ESC2, min_value)
            pi3.set_servo_pulsewidth(ESC3, min_value)
            pi4.set_servo_pulsewidth(ESC4, min_value)
            time.sleep(1)
            print "See.... uhhhhh"
# those are functions used for reading the angles from the IMU
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68


bus.write_byte_data(address, power_mgmt_1, 0)

 # print "Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

# this is the PID function
def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    # setting up the PID parameters. See more on the PID library for more intuiton
    pidX = PID.PID(P, I, D) # PID for the x angle
    pidY = PID.PID(P, I, D)  # PID for the x angle
    pidF = PID.PID(P, I, D)  # PID for the height

pidX.SetPoint=-1
    pidX.setSampleTime(0.01)

    pidY.SetPoint=-1
    pidY.setSampleTime(0.01)

    pidF.SetPoint=30
    pidF.setSampleTime(0.01)
    END = L
    feedbackX = 0    # obtained from the IMU sensor value
    feedbackY = 0    # obtained from the IMU sensor value
    feedbackF =0     # obtained from the ultrasonic sensor value
    # those lists are only used for ploting the graph of the PID output
    feedback_listX = []
    time_listX = []
    setpoint_listX = []

    feedback_listY = []
    time_listY = []
    setpoint_listY = []

    calibrate()  # we first calibrate the ESC

    for i in range(1, END):
        pidX.update(feedbackX)
        pidY.update(feedbackY)
        pidF.update(feedbackF)
        outputX = pidX.output
        outputY = pidY.output
        outputF = pidF.output
        # reading the angles from IMU
        gyroskop_xout = read_word_2c(0x43)
        gyroskop_yout = read_word_2c(0x45)
        gyroskop_zout = read_word_2c(0x47)
        beschleunigung_xout = read_word_2c(0x3b)
        beschleunigung_yout = read_word_2c(0x3d)
        beschleunigung_zout = read_word_2c(0x3f)
        beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
        beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
        beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
        xangle=get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert) # print "X Rotation: "$
        yangle=get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

        # reading the height from ultrasonic
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

       #print ("Distance:",distance,"cm")


        feedbackF=distance
        feedbackX=xangle
        feedbackY=yangle


        # commanding the motors depending on our PID value
        pi1.set_servo_pulsewidth(ESC1, 1200+outputF+(outputY/2)+(outputX/2))
        pi2.set_servo_pulsewidth(ESC2, 1200+outputF-(outputY/2)+(outputX/2))
        pi3.set_servo_pulsewidth(ESC3, 1200+outputF-(outputY/2)-(outputX/2))
        pi4.set_servo_pulsewidth(ESC4, 1200+outputF+(outputY/2)-(outputX/2))
        print("one ")
        print(1200+outputF+(outputY/2)+(outputX/2))
        print("two ")
        print(1200+outputF-(outputY/2)+(outputX/2))

# print("three ")
        print(1200+outputF-(outputY/2)-(outputX/2))

        print(1200+outputF+outputY-outputX)
       # time.sleep(1)
       # feedback= feedback + output
        '''if pid.SetPoint > 0:
            feedback += (output - (1/i))'''
        '''if i>9:
            pid.SetPoint = 1'''
       # time.sleep(0.02)

        '''feedback_listX.append(feedbackX)
        setpoint_listX.append(pid.SetPoint)
        time_listX.append(i)

        feedback_listY.append(feedbackY)
        setpoint_listY.append(pid.SetPoint)
        time_listY.append(i)'''
    stop()
    '''time_smX = np.array(time_listX)
    time_smoothX = np.linspace(time_smX.min(), time_smX.max(), 300)
    feedback_smoothX = spline(time_listX, feedback_listX, time_smoothX)

    plt.plot(time_smoothX, feedback_smoothX)
    plt.plot(time_listX, setpoint_listX)
    plt.xlim((0, L))
    plt.ylim((min(feedback_listX)-0.5, max(feedback_listX)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PIDX')

    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()


  time_smY = np.array(time_listY)
    time_smoothY= np.linspace(time_smY.min(), time_smY.max(), 300)
    feedback_smoothY = spline(time_listY, feedback_listY, time_smoothY)

    plt.plot(time_smoothY, feedback_smoothY)
    plt.plot(time_listY, setpoint_listY)
    plt.xlim((0, L))
    plt.ylim((min(feedback_listY)-0.5, max(feedback_listY)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PIDY')

    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()'''

if __name__ == "__main__":
    test_pid(1.2, 5, 0.001, L=500)
#pi.set_servo_pulsewidth(ESC, speed)
