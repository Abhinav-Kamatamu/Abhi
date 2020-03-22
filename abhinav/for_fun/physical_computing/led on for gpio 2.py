from gpiozero import LED
from time import sleep
led=LED(2)

for i in range (5):
    led.on()
    sleep(2)
    led.off()
    sleep(1)
