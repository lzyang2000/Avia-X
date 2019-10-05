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
        return {turbulence: 85, luminance: 3, emotion:"neutral" }

    def handle_state(self, state):
        global_triggers = {}
        personal_triggers = {}
        for rule in adjustment_rules:
            trigger_result = rule.trigger(state)
            if trigger_result:
                if rule.is_global:
                    global_triggers.update({rule.name: trigger_result })
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
    color_dict = {'red': (243,115,54), 'yellow': (247,204,59) }
    def __init__(self):
        super().__init__()
        
        pygame.mixer.init()

        def customize_light(customized_light):
            prev_theme = self.agents[0].retrieve_theme(self.state[theme])
            new_light = name_to_theme[self.state[theme]].light
            if not customized_light == RESET:
                new_light = self.color_dict[customized_light]
            self.agents[0].customize_theme(prev_theme, { light: new_light })
            self.change_color(new_light)

        def ask_theme():
            self.theme_text.visible = True
            self.all_themes.visible = True

        def custom_theme(custom_theme):
            self.chosen_theme = custom_theme

        def user_login():
            self.info.visible = True
            return

        def user_create():
            self.create_new.visible = True
            self.app.hide()
            return

        self.app = App(title = "User System", height = 150, width = 300, layout="grid", bg = "black")
        Text(self.app, text="Who's Flying?", grid=[3,0], color = "white")
        Text(self.app, text="Username", grid=[3,2], color = "white")
        self.username = TextBox(self.app, grid=[5,2], width="fill")
        self.username.text_color = "white"
        Text(self.app, text="", grid=[3,3])
        Text(self.app, text="", grid=[3,6])
        self.login = PushButton(self.app, pady=0, padx=0,command = user_login, text = "Login", grid=[3,6])
        self.login.text_color = "white"
        self.newuser = PushButton(self.app, pady=0,padx=0,command = user_create, text = "create new user", grid=[5,6])
        self.newuser.text_color = "white"

        # Create new user
        self.create_new = Window(self.app, title="Create New Avia-X User", height = 150, width = 500, visible=False, layout = "grid")
        Text(self.create_new, text="Enter Your Username", grid=[0,0], align="left")
        self.new_username = TextBox(self.create_new, grid=[1,0], align = "left")
        self.theme_text = Text(self.create_new, text = "Select your favorite cabinet theme.", grid=[1,2], visible=False)
        self.all_themes = Combo(self.create_new, command=custom_theme, options=name_to_global_theme.keys(), grid=[0,2], align="left", visible = False)
        PushButton(self.create_new, command=ask_theme, text = "Choose your theme", grid=[0,1], align="left")
        self.execute = PushButton(self.create_new, command = self.run, text = "Create and Login", grid=[0,3], align="left")
        
        # Info Window
        self.info = Window(self.app, title="Avia-X is running", visible = False)
        # Display Environment Info
        self.agent_name = Text(self.info, align = "top", width = "fill")
        self.trigger_box = Text(self.info, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")
        self.text_turbulence = Text(self.info, text="Getting Turbulence", align="left")
        self.text_lumi = Text(self.info, text="Getting Luminance", align="left")

        # Display Theme Info
        self.light_cond = Text(self.info, align = "left", width = "fill")
        

        # adding a temporary "reset" option as proof of concept
        self.customize_light_menu = Combo(self.info, command=customize_light, options=list(self.color_dict.keys()) + [RESET], align="bottom",width="fill")
        self.text_customize_light = Text(self.info, text="Customize Light for this theme", align="bottom", width = "fill")

        self.app.display()
    # Main functions
    def run(self):
        self.info.visible=True
        new_agent = GUIAgent(self.username.value, self.chosen_theme)
        self.new_agent_login(new_agent)
        
        
        def respond_to_state():
            self.update_state()
            self.handle_state(self.state)

        self.output_bar.repeat(1000, respond_to_state)

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


    # Helper Functions
    def new_agent_login(self, agent):
        self.agents.append(agent)
        preferred_theme = agent.user.info.preference['global_theme']

        theme_to_display = agent.retrieve_theme(preferred_theme)
        self.display_theme(theme_to_display)

        self.agent_name.value = ''.join([agent.user.username for agent in self.agents])

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
        

    def gather_state(self):
        return self.state

def main():
    session = GUISession()
    # agent = Agent()
    # session.new_agent_login(agent)
    # session.run()

if __name__ == '__main__':
    main()