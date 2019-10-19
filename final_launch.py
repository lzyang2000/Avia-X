from emotion_recognition.src.image_emotion_demo import *
from mock_agent import *
from user import *
from theme import *
from guizero import *
# from playsound import playsound
import pygame
import time
import os
import board
import busio
import adafruit_tsl2591
import csv
import RPi.GPIO as GPIO
import ledout

RESET = "reset"
GPIO_pin = 4 #Pressure Pin


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(GPIO_pin,GPIO.IN)
        

class Session:

    def __init__(self):
        self.agents = []

class GUISession(Session):

    state = { turbulence: 1 , luminance : 3, 'prev_turbulences': None, theme: None }
    idx = 0

    def __init__(self):

        pygame.mixer.init()
        self.curr_music = None
        app = App(title="Avia-X is running")
        self.app = app
        self.agent = GUIAgent(self)

        # self.agent_name = Text(app, align = "top", width = "fill")
        # self.trigger_box = Text(app, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")
        # self.text_turbulence = Text(self.app, text="Getting Turbulence", align="left")
        # self.text_lumi = Text(self.app, text="Getting Luminance", align="left")
 
        # # Info Window
        # self.info = Window(self.app, title="Avia-X is running", visible = False)
        # # Display Environment Info
        # self.agent_name = Text(self.info, align = "top", width = "fill")
        # self.trigger_box = Text(self.info, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")
        # self.text_turbulence = Text(self.info, text="Getting Turbulence", align="left")
        # self.text_lumi = Text(self.info, text="Getting Luminance", align="left")

        # # Display Theme Info
        # self.light_cond = Text(self.info, align = "left", width = "fill")

        self.app.display()

    def on_login_complete(self):
        app = self.app
        welcome_box = Box(app, height=40, width='fill')
        Text(welcome_box, text='Welcome Aboard!', align='bottom')
        self.agent.create_interface()
        self.display_theme(self.agent.retrieve_theme(self.agent.user.get_global_theme_preference()))
        self.run()

    # Main functions
    def run(self):
        def respond_to_state():
            self.update_state()
            self.handle_state(self.state)

        self.app.repeat(1000, respond_to_state)

    def display_theme(self, displayed_theme):
        self.set_theme_light(displayed_theme.light)
        self.play_music(displayed_theme.music)
        # self.trigger_box.value = "Theme:" + displayed_theme.name
        self.state[theme] = displayed_theme.name

    def display_state(self):
        self.text_emotion = "Emotion:" + self.state[emotion]
        self.text_lumi = "Luminance:" + self.state[luminance]
        self.text_pressure = "Pressure:" + self.state[pressure]
        self.text_turbulence = "Turbulence:" + "High" if self.state[turbulence] else "Low"

    def set_theme_light(self, light):
        self.app.bg = light
        self.agent.control_panel.bg = None

    def set_music_volume(self, vol):
        pygame.mixer.music.set_volume(int(vol) * 1.00 / 100)

    def play_music(self, path):
        if not path:
            pygame.mixer.music.stop()
            return 
        path_to_album = './theme/assets/' + path
        if self.curr_music == path_to_album:
            return
        music_files = os.listdir(path_to_album)
        if music_files:
            music_file = path_to_album + '/' + music_files[0]
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            self.curr_music = path_to_album

    # Maps a state to a theme
    def handle_state(self, state):
        pass

    def handle_global_triggers(self, triggers):
        print(self.state)
        print(triggers)
        pass

    def update_state(self):
        self.idx += 1
        if hasattr(self, 'prev_turbulences'):
            self.all_infos = Infos(self.idx, self.prev_turbulences)
        else:
            self.all_infos = Infos(self.idx)
        self.state[turbulence] = self.all_infos.turbulence
        self.state[luminance] = self.all_infos.light
        self.state[emotion] = self.all_infos.emotion
        self.state[pressure] = self.all_infos.pressure
        self.prev_turbulences = self.all_infos.prev_turbulences

        # Light up the Rasp Pi
        self.all_infos.lightPi(self.state[theme])


class Infos:
    # Attributes : self.light, self.emotion, self.turbulence
    def __init__(self, time_idx, prev_turbulences=None):
        # Read in light data
        # Initialize the I2C bus.
        i2c = busio.I2C(board.SCL, board.SDA)
        # Initialize the sensor.
        sensor = adafruit_tsl2591.TSL2591(i2c)
        self.light = sensor.lux
        self.prev_turbulences = prev_turbulences
        
        # Facial Expression
        facial_expr = main_predict()
        if facial_expr == None:
            self.emotion = "neutral"
        self.emotion = facial_expr

        # Pressure (from verify.py)
        #take a reading
        input = GPIO.input(GPIO_pin)
        if input:
            self.pressure = True
        else:
            self.pressure = False
        
        # Turbulence
        with open('Daher_Turbulence_data.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            row = [line for idx, line in enumerate(readCSV) if idx == time_idx]
            row = row[0]
            # print(row)
            row[1] = int(row[1])
            row[2] = float(row[2])
            row[3] = float(row[3])
            # row = readCSV[time_idx]
            if self.prev_turbulences:
                if len(self.prev_turbulences) == 5: # TODO could edit for more effects
                    self.prev_turbulences.pop(0)
                self.prev_turbulences.append(abs(row[1]))
                if sum(self.prev_turbulences) / len(self.prev_turbulences) < 1000:
                # all([True if abs(t) > 500 else False for t in self.prev_turbulences]):
                    self.turbulence = False
                else:
                    self.turbulence = True
            else:
                self.prev_turbulences = [row[1]]
                self.turbulence = abs(row[1]) > 1000
                # print(self.turbulence)
        self.prev_turbulences = prev_turbulences

    def lightPi(self, theme):
        ledout.change_color(theme)

def main():
    session = GUISession()

if __name__ == '__main__':
    main()
