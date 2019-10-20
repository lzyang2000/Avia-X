
from user import *
from theme import *
from guizero import *
import time

NEW_USER_COMMAND = 'NEW USER'
SKIP_COMMAND = 'SKIP'
NO_MUSIC = 'No Music'

'''
The agent User uses to interact with the system.
This is a terminal agent for test purpose.
'''
class Agent:

    user = None

    def customize_theme(self, theme, change):
        new_theme_dic = dict(theme.to_dict())
        new_theme_dic.update(change)
        original_theme_dic = name_to_theme[theme.name]().to_dict()
        if new_theme_dic == original_theme_dic:
            self.reset_theme(theme.name)
        else:
            customized_theme = CustomizedTheme.create(new_theme_dic, theme.name)
            theme_database.save(self.user.username, customized_theme)

    # theme retrieval is done by agent because theme is user specific
    def retrieve_theme(self, theme_name):
        customized_theme_dict = theme_database.find(self.user.username, theme_name)
        if customized_theme_dict:
            return CustomizedTheme.create(customized_theme_dict, theme_name)
        return name_to_theme[theme_name]()

    def reset_theme(self, theme_name):
        theme_database.remove(self.user.username, theme_name)


class GUIAgent(Agent):

    color_dict = { 'red': (243,115,54), 'yellow': (247,204,59) }

    def __init__(self, session):
        self.app = session.app
        self.session = session
        self.window = self.wait_for_user_session()

    def user_login(self):
        if self.pending_user:
            user = self.pending_user
        else:
            user = self.login_username.value
            if not user:
                return
        self.await_session_window.destroy()
        self.user = User.login(self, user)
        self.session.on_login_complete()

    def create_new_user(self):
        pending_new_user = self.username_input.value
        if pending_new_user:
            user_created, _ = User.create_new_user(self, pending_new_user, User.Info({ preference: { global_theme: self.pending_theme if self.pending_theme else normal } }))
            if user_created:
                self.user = user_created
                self.new_user_window.destroy()
                self.session.on_login_complete()
            else:
                self.duplicate_user_err.visible = True

    def new_user_page(self):
        self.await_session_window.destroy()
        window = Window(self.app, title='Create New Avia-X User', height = 200, width = 400)
        Box(window, height=25, width='fill')

        # Username input
        title_box = Box(window, height=30, width=235)
        Text(title_box, text='Enter Your Username', align='left')
        self.username_input = TextBox(title_box, align='right')

        # Duplicate user error
        err_box = Box(window, height=20, width='fill')
        self.duplicate_user_err = Text(err_box, text='Username Used', color='red', size=9, align='bottom', visible=False)

        # Theme selection
        Box(window, height=10, width='fill')
        self.pending_theme = None
        def set_pending_theme(theme_name):
            self.pending_theme = theme_name

        theme_box = Box(window, height=20, width=235)
        Text(theme_box, text = 'Pick a Theme', align='left')
        Combo(theme_box, command=set_pending_theme, options=name_to_global_theme.keys(), align='right')

        Box(window, height=20, width='fill')

        # Confirm button
        PushButton(window, command=self.create_new_user, text='Create and Login')

        self.new_user_window = window

    def wait_for_user_session(self):
        current_user_data = user_database.find()
        existing_users = []
        if current_user_data:
            existing_users = [username for (username, data) in current_user_data.items()]

        self.pending_user = None
        def set_pending_user(username):
            self.pending_user = username

        window = Window(self.app, title='User System', height=200, width=400, bg='black')

        # Title
        title_box = Box(window, height=40, width='fill')
        Text(title_box, text="Who's Flying?", align='bottom', color = 'white')

        Box(window, height=30, width='fill')

        # Username input
        username_box = Box(window, height=40, width=235)
        Text(username_box, text='Username', color = 'white', align='left')
        self.login_username = Combo(username_box, command=set_pending_user, options=existing_users, align='right')
        self.login_username.text_color = 'white'

        Box(window, height=20, width='fill')

        # Login button
        button_box = Box(window, height=40, width=160)
        login = PushButton(button_box, pady=0, padx=0, command = self.user_login, text = 'Login', align='left')
        login.text_color = 'white'

        # New user button
        newuser = PushButton(button_box, pady=0, padx=0, command = self.new_user_page, text = 'create new user', align='right')
        newuser.text_color = 'white'

        self.await_session_window = window

    def customize_light_from_command(self, command):
        theme_name = self.current_theme_obj.name
        if command == RESET:
            new_light = name_to_theme[theme_name].light
        else:
            new_light = self.color_dict[command]
        self.customize_theme(self.current_theme_obj, { light: new_light })
        self.current_theme_obj = self.retrieve_theme(theme_name)
        self.update_light_sliders()
        self.session.display_theme(self.current_theme_obj)

    def customize_light_from_rgb(self):
        theme_name = self.current_theme_obj.name
        self.customize_theme(self.current_theme_obj, { light: (self.R, self.G, self.B) })
        self.current_theme_obj = self.retrieve_theme(theme_name)
        self.update_light_sliders()
        self.session.display_theme(self.current_theme_obj)

    def customize_music(self, command):
        if command == NO_MUSIC:
            theme_name = self.current_theme_obj.name
            self.customize_theme(self.current_theme_obj, { music: None })
        else:
            theme_name = command.replace('Music', 'Theme')
            theme_music = name_to_global_theme[theme_name].music
            self.customize_theme(self.current_theme_obj, { music: theme_music })
        self.current_theme_obj = self.retrieve_theme(self.current_theme_obj.name)
        self.session.display_theme(self.current_theme_obj)

    def update_light_sliders(self):
        self.R, self.G, self.B = self.current_theme_obj.light
        self.R_slider.value, self.G_slider.value, self.B_slider.value = str(self.R), str(self.G), str(self.B)

    def update_preferred_theme(self, new_theme_name):
        self.user.set_preference({ global_theme: new_theme_name })
        self.current_theme_obj = self.retrieve_theme(new_theme_name)
        self.display_theme(self.current_theme_obj)
        self.session.display_theme(self.current_theme_obj)

    def display_theme(self, theme_obj):
        self.update_light_sliders()
        self.current_theme_text.value = get_current_theme_string(theme_obj.name)
        self.music_combo.value = self.get_music_text(theme_obj)
        self.light_combo.value = RESET

    def display_theme_from_name(self, theme_name):
        theme_obj = self.retrieve_theme(theme_name)
        self.current_theme_obj = theme_obj
        self.display_theme(theme_obj)

    def create_interface(self):
        width, height = 600, 400
        window = Window(self.app, title='Avia-X Mock Control', height=height, width=width, layout='grid')
        self.control_panel = window

        # Welcome title
        welcome_box = Box(window, height=50, width=width, grid=[0,0,12,1])
        Text(welcome_box, text='Welcome Aboard, {}!'.format(self.user.username), size=16, align='bottom')

        Box(window, height=35, width=width, grid=[0,1,12,1])

        # Customize theme section title
        customize_theme_title_box = Box(window, height=50, width=width // 2, grid=[0,2,6,1])
        Text(customize_theme_title_box, text='Customize Theme', size=14, align='top')
        current_theme_name = self.user.get_global_theme_preference()
        self.current_theme_text = Text(customize_theme_title_box, text=get_current_theme_string(current_theme_name), size=9, align='top')

        # Customize light from dictionary
        theme_light_box = Box(window, height=60, width=width // 3, grid=[1,3,4,1]) # x = 1,2,3,4
        Text(theme_light_box, text='Theme Light   ', align='left')
        self.light_combo = Combo(theme_light_box, command=self.customize_light_from_command, options=list(self.color_dict.keys()) + [RESET], align='right')

        # Customize light from RGB
        theme_light_custom_title_box = Box(window, height=40, width=width // 2, grid=[0,4,6,1])
        Text(theme_light_custom_title_box, text='Custom Light')
        
        def set_R(r_val):
            self.R = int(r_val)
            self.customize_light_from_rgb()

        def set_G(g_val):
            self.G = int(g_val)
            self.customize_light_from_rgb()

        def set_B(b_val):
            self.B = int(b_val)
            self.customize_light_from_rgb()

        self.current_theme_obj = self.retrieve_theme(current_theme_name)

        R_box = Box(window, height=120, width=width // 6, grid=[1,5,1,2])
        self.R_slider = Slider(R_box, start=0, end=255, command=set_R, horizontal=False, width=20, height=100, align='top')
        Text(R_box, text='     R', align='bottom')

        self.G = 0
        G_box = Box(window, height=120, width=width // 6, grid=[2,5,2,2])
        self.G_slider = Slider(G_box, start=0, end=255, command=set_G, horizontal=False, width=20, height=100, align='top')
        Text(G_box, text='     G', align='bottom')

        self.B = 0
        B_box = Box(window, height=120, width=width // 6, grid=[4,5,1,2])
        self.B_slider = Slider(B_box, start=0, end=255, command=set_B, horizontal=False, width=20, height=100, align='top')
        Text(B_box, text='     B', align='bottom')

        self.update_light_sliders()

        # Set preference title
        set_preference_title_box = Box(window, height=50, width=width // 2, grid=[6,2,6,1])
        Text(set_preference_title_box, text='Set Preference', size=14, align='top')

        # Switch theme preference
        switch_theme_box = Box(window, height=60, width=width // 2, grid=[6,3,6,1]) # x = 6,7,8,9,10,11
        Text(switch_theme_box, text='      Switch Theme', align='left')
        Text(switch_theme_box, text='      ', align='right')
        theme_combo = Combo(switch_theme_box, command=self.update_preferred_theme, options=name_to_global_theme.keys(), align='right')
        theme_combo.value = current_theme_name

        # Customize music
        theme_music_title_box = Box(window, height=40, width=width // 2, grid=[6,4,6,1])
        Text(theme_music_title_box, text='Music')

        music_menu_text_box = Box(window, height=60, width=width // 4, grid=[6,5,3,1])
        Text(music_menu_text_box, text='      Switch Music      ')
        music_menu_box = Box(window, height=60, width=width // 4, grid=[6,6,3,1])
        self.music_options = [theme_name.replace('Theme', 'Music') for theme_name in name_to_global_theme.keys() if theme_name != normal] + [NO_MUSIC]
        self.music_combo = Combo(music_menu_box, command=self.customize_music, options=self.music_options, align='top')

        # Change music volume
        music_volume_box = Box(window, height=120, width=width // 6, grid=[9,5,3,2])
        self.volume_slider = Slider(music_volume_box, start=0, end=100, command=self.session.set_music_volume, width=width // 4, height=20, align='top')
        self.volume_slider.value = 30
        Text(music_volume_box, text='  Volume')
        self.display_theme(self.current_theme_obj)
        self.session.display_theme(self.current_theme_obj)

    def get_music_text(self, theme_obj):
        text = [theme.name.replace('Theme', 'Music') for theme in global_themes if theme.music == theme_obj.music][0]
        if text in self.music_options:
            return text
        return NO_MUSIC

def get_current_theme_string(theme_name):
    return 'Current Theme: {}'.format(theme_name)
