from gpiozero import LED, Button
from time import sleep
from random import uniform
left_name = input("Left player name is ")
right_name = input ("Right player name is ")
right_button = Button(15)
left_button = Button(14)
led = LED(4)
left_score = 0
right_score = 0

def pressed(button):
    global right_score, left_score
    if button.pin.number == 14:
        left_score +=1
    else:
        right_score +=1
        
for i in range (5):
    led.on()
    sleep(uniform(5, 10))
    led.off()
    right_button.when_pressed = pressed
    left_button.when_pressed = pressed
    sleep(0.5)
if left_score > right_score:
    print (left_name, 'has won the game')
if right_score>left_score:
    print(right_name, 'has won the game')
