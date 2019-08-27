from .constants import *

class Theme:
    name = None

class GlobalTheme(Theme):
    image = None
    light = None
    music = None

class Quiet(GlobalTheme):
    image = ['./quiet_theme/photos/1.png', './quite_theme/photos/2.png']
    light = 70
    music = './quite_theme/music_playlist'

class Engaged(GlobalTheme):
    image = ['./engaged_theme/photos/1.png', './engaged_theme/photos/2.png']
    light = 70
    music = './engaged_theme/music_playlist'

class Romantic(GlobalTheme):
    image = ['./romantic_theme/photos/r1.png', './romantic_theme/photos/r2.png']
    light = 30
    music = './romantic_theme/music_playlist'

class PersonalTheme(Theme):
    seat_angle = None
    entertainment_recommendation = None
    reading_light = None

class Cozy(PersonalTheme):
    seat_angle = 25
    reading_light = 0

class Reading(PersonalTheme):
    seat_angle = 80
    reading_light = 40

class Sleep(PersonalTheme):
    seat_angle = 5
    reading_light = 0


preset_global_themes = [Quiet, Engaged, Romantic]
preset_personal_themes = [Cozy, Reading, Sleep]
