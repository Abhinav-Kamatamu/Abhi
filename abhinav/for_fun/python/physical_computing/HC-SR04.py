import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer
GPIO.setmode(GPIO.BOARD)
trig = 18
echo = 16
n = 0
ext = 0
buzzer = Buzzer(15)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
while ext < 15:
    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end-pulse_start
    distance = round((pulse_duration*34000)/2,2)
    if distance < 15:
        buzzer.on()
    else:
        buzzer.off()
    #print(distance
    n +=1
    if n == 1000:
        ext +=1
        n =0
buzzer.off()