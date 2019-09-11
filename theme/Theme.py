from .constants import *

class Theme:
    name = None

class CustomizedTheme(Theme):

    @staticmethod
    def create(theme_dict, name):
        if is_global_theme_name(name):
            return CustomizedGlobalTheme(theme_dict, name)
        return CustomizedPersonalTheme(theme_dict, name)

class GlobalTheme(Theme):
    name = normal
    image = None
    light = (255, 250, 229)
    music = None

    def to_dict(self):
        return { image: self.image, light: self.light, music: self.music }

class CustomizedGlobalTheme(CustomizedTheme, GlobalTheme):

    def __init__(self, theme_dict, name):
        self.image = theme_dict[image]
        self.light = theme_dict[light]
        self.music = theme_dict[music]
        self.name = name

class Warm(GlobalTheme):
    name = warm
    image = None
    light = (255, 231, 211)
    music = 'warm_theme/music_playlist'

class Quiet(GlobalTheme):
    name = quiet
    image = ['quiet_theme/photos/1.png', 'quite_theme/photos/2.png']
    light = (99, 200, 242)
    music = 'quiet_theme/music_playlist'

class Engaged(GlobalTheme):
    name = engaged
    image = ['engaged_theme/photos/1.png', 'engaged_theme/photos/2.png']
    light = (70, 70, 255)
    music = 'engaged_theme/music_playlist'

class Romantic(GlobalTheme):
    name = romantic
    image = ['romantic_theme/photos/r1.png', 'romantic_theme/photos/r2.png']
    light = (216, 141, 188)
    music = 'romantic_theme/music_playlist'

class PersonalTheme(Theme):
    seat_angle = None
    entertainment_recommendation = None
    reading_light = None

    def to_dict(self):
        return { seat_angle: self.seat_angle, entertainment_recommendation: self.entertainment_recommendation, reading_light: self.reading_light }

class CustomizedPersonalTheme(CustomizedTheme, PersonalTheme):

    def __init__(self, dict, name):
        self.seat_angle = dict[seat_angle]
        self.entertainment_recommendation = dict[entertainment_recommendation]
        self.reading_light = dict[reading_light]
        self.name = name

class Cozy(PersonalTheme):
    name = cozy
    seat_angle = 25
    reading_light = 0

class Reading(PersonalTheme):
    name = reading
    seat_angle = 80
    reading_light = 40

class Sleep(PersonalTheme):
    name = sleep
    seat_angle = 5
    reading_light = 0

global_themes = [GlobalTheme, Quiet, Engaged, Romantic, Warm]
name_to_global_theme = { theme.name: theme for theme in global_themes }

personal_themes = [Cozy, Reading, Sleep]
name_to_personal_theme = { theme.name: theme for theme in personal_themes }

name_to_theme = { **name_to_global_theme, **name_to_personal_theme }

def is_global_theme_name(theme_name):
    return theme_name in name_to_global_theme
