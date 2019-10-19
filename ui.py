from guizero import *

from emotion_recognition.src.image_emotion_demo import *
import time
from mock_agent import Agent
from user import *
from theme import *

def lumi_change(slider_value):
    textbox_lumi.value = "1e+"+slider_value

def turbulence_change(slider_value):
    textbox_turbulence.value = slider_value

def pressure_change(slider_value):
    textbox_pressure.value = slider_value


def display_output():
	# threading.Timer(5.0, display_output).start()
	out_put = main_predict()
	if out_put == None:
		return
	output_bar.value = out_put
	if out_put in ["sad", "angry"]:
		change_color("warm")
	elif int(lumi.value) > 7:
		change_color("warm")
	else:
		change_color("bright") 

def change_color(ctype):
	if ctype == "warm":
		app.bg = warm_color
	elif ctype == "bright":
		app.bg = bright_color

warm_color = (243, 231, 211)
bright_color = (255, 250, 229)

app = App()

# Define lumi input
lumi = Slider(app, command=lumi_change, horizontal = False, align = "left", start = 2, end = 10)
text_lumi = Text(app, text="Luminance", align="left")
textbox_lumi = TextBox(app, align = "left")

# Define pressure input
turbulence = Slider(app, command=turbulence_change, horizontal = False, align = "left", start = 10, end = 90)
text_turbulence = Text(app, text="Turbulence", align="left")
textbox_turbulence = TextBox(app, align = "left")

# Define picture capture
output_button = PushButton(app, text="Predict", align = "left", command = display_output)
output_bar = Text(app, text = "Getting Output...", align = "left")
output_bar.repeat(5000, display_output)

app.display()







# create customer elements


self.app.display()