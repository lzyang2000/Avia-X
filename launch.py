from emotion_recognition.src.image_emotion_demo import *
from mock_agent import *
from user import *
from theme import *
from guizero import *
# from playsound import playsound
import pygame
import time
import os

RESET = "reset"

class Session:

    def __init__(self):
        self.agents = []

    def run(self):
        while(True):
            time.sleep(5)
            state = self.gather_state()
            self.handle_state(state)

    def new_agent_login(self, agent):
        self.agents.append(agent)

    # Get emotion and bar input from GUI
    def gather_state(self):
        return { turbulence: 85, luminance: 3, emotion:"neutral" }

    def handle_state(self, state):
        global_triggers = {}
        personal_triggers = {}
        for rule in adjustment_rules:
            trigger_result = rule.trigger(state)
            if trigger_result:
                if rule.is_global:
                    global_triggers.update({ rule.name: trigger_result })
                # else:
                #     personal_triggers.update({ rule.name: trigger_result })
        self.handle_global_triggers(global_triggers)

        # print('Following personal adjustments triggered: {}'.format(personal_triggers.keys()))
        # for agent in self.agents:
        #     agent.handle_automatic_adjustments(personal_triggers, state)

    # TODO: discuss how to override a global rule trigger
    def handle_global_triggers(self, triggers):
        pass

class GUISession(Session):

    state = {turbulence: 1 , luminance : 3, theme: None}
    warm_color = (255, 231, 211)
    bright_color = (255, 250, 229)
    def __init__(self):
        super().__init__()
        
        pygame.mixer.init()

        def turbulence_capture(slider_value):
            slider_value = int(slider_value)
            self.state[turbulence] = slider_value
            self.turbulence_textbox.value = slider_value

        def lumi_capture(slider_value):
            slider_value = int(slider_value)
            self.state[luminance] = slider_value
            self.luminance_textbox.value = slider_value

        def customize_light(customized_light):
            prev_theme = self.agents[0].retrieve_theme(self.state[theme])
            new_light = name_to_theme[self.state[theme]].light
            if not customized_light == RESET:
                new_light = color_dict[customized_light]
            self.agents[0].customize_theme(prev_theme, { light: new_light })
            self.change_color(new_light)

        def ask_theme():
            self.theme_text.visible = True
            self.all_themes.visible = True

        def custom_theme(custom_theme):
            print(1)
            self.chosen_theme = custom_theme

        self.app = App(title="Central System")
        
        
        
        # surname = TextBox(app, grid=[1,1])
        # dob_label = Text(app, text="Date of Birth", grid=[0,2], align="left")
        # dob = TextBox(app, grid=[1,2])
        # create ui elements for central system
        self.agent_name = Text(self.app, align = "top", width = "fill")
        self.trigger_box = Text(self.app, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")

        self.turbulence = Slider(self.app, command=turbulence_capture, horizontal=False, align = "left", start = 1, end = 100)
        self.text_turbulence = Text(self.app, text="Turbulence", align="left")
        self.turbulence_textbox = TextBox(self.app, align = "left")

        self.lumience = Slider(self.app, command=lumi_capture, horizontal = False, align = "left", start = 2, end = 10)
        self.text_lumi = Text(self.app, text="Luminance", align="left")
        self.luminance_textbox = TextBox(self.app, align = "left")

        # do we keep the color attribute in the final prototype?
        # if so, need a "custom" option to allow any color selected by user
        color_dict = { 'red': (243,115,54), 'yellow': (247,204,59) }

        # adding a temporary "reset" option as proof of concept
        self.customize_light_menu = Combo(self.app, command=customize_light, options=list(color_dict.keys()) + [RESET], align="bottom",width="fill")
        self.text_customize_light = Text(self.app, text="Customize Light for this theme", align="bottom", width = "fill")
        # Define picture capture
        self.output_bar = Text(self.app, text = "Getting Output...", align = "left")
        
        self.customer = Window(self.app, title="Customer", layout="grid")
        # create customer elements
        Text(self.customer, text="Username", grid=[0,0], align="left")
        self.username = TextBox(self.customer, grid=[1,0])
        self.theme_text = Text(self.customer, text = "Select your favorite cabinet theme.", grid=[1,2], visible=False)
        self.all_themes = Combo(self.customer, command=custom_theme, options=name_to_global_theme.keys(), grid=[0,2], align="left", visible = False)
        PushButton(self.customer, command=ask_theme, text = "Choose your theme", grid=[0,1], align="left")
        self.execute = PushButton(self.customer, command = self.run, text = "Apply", grid=[0,3], align="left")

        self.app.display()

    def new_agent_login(self, agent):
        self.agents.append(agent)
        preferred_theme = agent.user.info.preference['global_theme']

        theme_to_display = agent.retrieve_theme(preferred_theme)
        self.display_theme(theme_to_display)

        self.agent_name.value = ''.join([agent.user.username for agent in self.agents])

    def display_theme(self, displayed_theme):  
        self.change_color(displayed_theme.light)
        self.play_album(displayed_theme.music)
        self.trigger_box.value = "Theme:" + displayed_theme.name
        self.state[theme] = displayed_theme.name

    def handle_global_triggers(self, triggers):
        print(self.state)
        print(triggers)

        if not triggers:
            return

        all_updates = {}
        for val in triggers.values():
            all_updates.update(val)

        # anything that uses #self.agents[0] should consider multiple agents
        if safety_belt_warning in all_updates:
            self.trigger_box.value = "Please Fasten your Belt"
        if theme in all_updates:
            theme_name = all_updates[theme]
            if theme_name == 'preference':
                theme_name = self.agents[0].user.info.preference['global_theme']
            updated_theme = self.agents[0].retrieve_theme(theme_name)
            self.display_theme(updated_theme)




    def change_color(self,color):
        self.app.bg = color

    def play_album(self, path):
        if not path:
            return
        path_to_album = './theme/assets/' + path
        music_files = os.listdir(path_to_album)
        if music_files:
            music_file = path_to_album + '/' + music_files[0]
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            # playsound(path_to_album + '/' + music_files[0], False)

    def run(self):
        new_agent = GUIAgent(self.username.value, self.chosen_theme)
        self.new_agent_login(new_agent)
        def respond_to_state():
            out_put = main_predict()
            if out_put == None:
                self.state[emotion] = "neutral"
            self.state[emotion] = out_put
            self.handle_state(self.state)

        self.output_bar.repeat(1000, respond_to_state)
        

    def gather_state(self):
        return self.state

def main():
    session = GUISession()
    # agent = Agent()
    # session.new_agent_login(agent)
    # session.run()

if __name__ == '__main__':
    main()
