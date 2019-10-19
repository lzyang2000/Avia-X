from emotion_recognition.src.image_emotion_demo import *
from mock_agent import *
from user import *
from theme import *
from guizero import *
import time
import os
import board
import busio
import adafruit_tsl2591
import csv
import RPi.GPIO as GPIO
import ledout
import vlc

RESET = "reset"

GPIO_pin = 4 #Pressure Pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_pin,GPIO.IN)
        

class Session:

    def __init__(self):
        self.agents = []

class GUISession(Session):

    state = { turbulence: 1 , luminance : 3, pressure: 1, emotion: neutral }
    output_state = { theme: None, safety_belt_warning: False }
    idx = 0
    theme_obj = None

    def __init__(self):
        self.music_players = { quiet : vlc.MediaPlayer("/home/pi/Avia-X/theme/assets/quiet_theme/music_playlist/quiet.mp3"),
                            engaged : vlc.MediaPlayer("/home/pi/Avia-X/theme/assets/engaged_theme/music_playlist/music1.mp3"),
                            warm : vlc.MediaPlayer("/home/pi/Avia-X/theme/assets/warm_theme/music_playlist/warm.mp3") }

        self.curr_music = None
        app = App(title="Avia-X is running")
        self.app = app
        self.agent = GUIAgent(self)

        # self.agent_name = Text(self.app, align = "top", width = "fill")
        # self.trigger_box = Text(self.app, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")
        # self.text_turbulence = Text(self.app, text="Getting Turbulence", align="left")
        # self.text_lumi = Text(self.app, text="Getting Luminance", align="left")

        # Display Theme Info
        # self.light_cond = Text(self.app, align = "left", width = "fill")
        # self.music_play = Text(self.app, align = "left", width = "fill")
        self.app.display()

    def on_login_complete(self):
        app = self.app
        welcome_box = Box(app, height=40, width='fill')
        Text(welcome_box, text='Welcome Aboard!', align='bottom')
        self.agent.create_interface()
        self.run()

    # Main functions
    def run(self):
        def respond_to_state():
            self.update_state()
            self.handle_state(self.state)

        self.app.repeat(1000, respond_to_state)

    def display_theme(self, displayed_theme_obj):
        prev_state = self.output_state[theme]
        self.output_state[theme] = displayed_theme_obj.name
        if not self.theme_obj or displayed_theme_obj.light != self.theme_obj.light:
            self.set_theme_light(displayed_theme_obj.light)
        # self.play_music(displayed_theme_obj.music)
        self.play_music(prev_state, self.output_state[theme])
        self.theme_obj = displayed_theme_obj
        # self.trigger_box.value = "Theme:" + displayed_theme.name + "Please Fasten your belt" \
        #     if self.output_state[safety_belt_warning] else ""

    def display_state(self):
        # self.text_emotion.value = "Emotion:" + self.state[emotion]
        # self.text_lumi.value = "Luminance:" + self.state[luminance]
        # self.text_pressure.value = "Pressure:" + self.state[pressure]
        # self.text_turbulence.value = "Turbulence:" + "High" if self.state[turbulence] else "Low"
        if self.theme_obj.name != self.output_state[theme]:
            self.agent.display_theme_from_name(self.output_state[theme])

    def set_theme_light(self, light):
        self.app.bg = light
        self.agent.control_panel.bg = None
        if hasattr(self, 'all_infos'):
            self.all_infos.lightPi(self.output_state[theme])

    def set_music_volume(self, vol):
        pass
        # self.music_players[quiet].audio_set_volume(int(vol))
        # self.music_players[engaged].audio_set_volume(int(vol))
        # self.music_players[warm].audio_set_volume(int(vol))
        
    def play_music(self, prev_theme, new_theme):
        if prev_theme == None:
            if new_theme == normal:
                pass
            else:
                self.music_players[new_theme].play()
        elif prev_theme == new_theme:
            pass
        elif prev_theme == normal:
            self.music_players[new_theme].play()
        elif new_theme == normal:
            self.music_players[prev_theme].pause()
        else:
            self.music_players[prev_theme].pause()
            self.music_players[new_theme].play()
        return

    # Updates the output state
    def handle_state(self, state):
        cur_theme = self.output_state[theme]
        for rule in rules:
            update = rule.get_state_update(state)
            if update:
                self.output_state.update(update)
        self.display_state()

    # def handle_global_triggers(self, triggers):
    #     print(self.state)
    #     print(triggers)
    #     pass

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
            print("Under Pressure")
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
