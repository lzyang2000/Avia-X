import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
from user import *
from theme import *
import time                            #calling time to provide delays in program

quite_color = [47, 40, 0]   
engaged_color = [47, 42, 0]
normal_color = [10, 14, 50]
warm_color = [1, 1, 49]
predefined_themes = {quiet:quite_color, engaged:engaged_color, normal:normal_color,warm:warm_color}
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

# setup all blue
IO.setup(13,IO.OUT)
IO.setup(16,IO.OUT)
IO.setup(18,IO.OUT)

# setup all green
IO.setup(19,IO.OUT)
IO.setup(20,IO.OUT)
IO.setup(23,IO.OUT)

# setup all red
IO.setup(21,IO.OUT)
IO.setup(24,IO.OUT)
IO.setup(26,IO.OUT)

blue_1 = IO.PWM(13,100)
blue_2 = IO.PWM(16,100)
blue_3 = IO.PWM(18,100)

green_1 = IO.PWM(19,100)
green_2 = IO.PWM(20,100)      #generate PWM signal with 0% duty cycle
green_3 = IO.PWM(23,100)

red_1 = IO.PWM(21,100)
red_2 = IO.PWM(24,100)
red_3 = IO.PWM(26,100)
def change_color(theme):
    ## B, G, R for themes
    color_space = predefined_themes[theme]
    b,g,r = color_space
    
    blue_1.start(b)
    blue_2.start(b)
    blue_3.start(b)
    green_1.start(g)
    green_2.start(g)
    green_3.start(g)
    red_1.start(r)
    red_2.start(r)
    red_3.start(r)

change_color(quiet)