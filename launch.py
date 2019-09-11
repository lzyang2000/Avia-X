from emotion_recognition.src.image_emotion_demo import *
from mock_agent import Agent
from user import *
from theme import *
from guizero import *
import time

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
        return { turbulence: 85, luminence: 3, emotion:"neutral" }

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

    state = { turbulence: 1 , luminence : 3, theme: None }
    warm_color = (255, 231, 211)
    bright_color = (255, 250, 229)
    def __init__(self):
        super().__init__()
        self.app = App()

        def turbulence_capture(slider_value):
            slider_value = int(slider_value)
            self.state[turbulence] = slider_value
            self.turbulence_textbox.value = slider_value

        def lumi_capture(slider_value):
            slider_value = int(slider_value)
            self.state[luminence] = slider_value
            self.luminence_textbox.value = slider_value

        def customize_light(customized_light):
            prev_theme = self.agents[0].retrieve_theme(self.state[theme])
            new_light = name_to_theme[self.state[theme]].light
            if not customized_light == RESET:
                new_light = color_dict[customized_light]
            self.agents[0].customize_theme(prev_theme, { light: new_light })

        # ui elements
        self.agent_box = Text(self.app, align = "top", width = "fill")
        self.trigger_box = Text(self.app, text = "Belt:Safe. Theme:Normal", align = "top", width = "fill")

        self.turbulence = Slider(self.app, command=turbulence_capture, horizontal=False, align = "left", start = 1, end = 100)
        self.text_turbulence = Text(self.app, text="Turbulence", align="left")
        self.turbulence_textbox = TextBox(self.app, align = "left")

        self.lumience = Slider(self.app, command=lumi_capture, horizontal = False, align = "left", start = 2, end = 10)
        self.text_lumi = Text(self.app, text="Luminance", align="left")
        self.luminence_textbox = TextBox(self.app, align = "left")

        # do we keep the color attribute in the final prototype?
        # if so, need a "custom" option to allow any color selected by user
        color_dict = { 'red': (243,115,54), 'yellow': (247,204,59) }

        # adding a temporary "reset" option as proof of concept
        self.customize_light_menu = Combo(self.app, command=customize_light, options=list(color_dict.keys()) + [RESET], align="bottom",width="fill")
        self.text_customize_light = Text(self.app, text="Customize Light for this theme", align="bottom", width = "fill")
        # Define picture capture
        self.output_bar = Text(self.app, text = "Getting Output...", align = "left")

    def new_agent_login(self, agent):
        self.agents.append(agent)
        self.state[theme] = normal
        self.agent_box.value = ''.join([agent.user.username for agent in self.agents])

    def handle_global_triggers(self, triggers):
        print(triggers)
        belt_warning = triggers["TurbulenceRuleGlobal"]["Safety Belt Warning"]
        theme_name = triggers["TurbulenceRuleGlobal"]["Theme"]

        # anything that uses #self.agents[0] should consider multiple agents
        if theme_name:
            updated_theme = self.agents[0].retrieve_theme(theme_name)
            self.change_color(updated_theme.light)
            self.trigger_box.value = "Theme:" + updated_theme.name
            self.state[theme] = updated_theme.name

        if belt_warning:
            self.trigger_box.value = "Please Fasten your Belt"

    def change_color(self,color):
            self.app.bg = color

    def run(self):

        def respond_to_state():
            out_put = main_predict()
            if out_put == None:
                self.state[emotion] = "neutral"
            self.state[emotion] = out_put
            self.handle_state(self.state)

        self.output_bar.repeat(1000, respond_to_state)
        self.app.display()

    def gather_state(self):
        return self.state

def main():
    session = GUISession()
    agent = Agent()
    session.new_agent_login(agent)
    session.run()

if __name__ == '__main__':
    main()
