
theme = 'Theme'

quiet = 'Quiet Theme'
engaged = 'Engaged Theme'
romantic = 'Romantic Theme'

cozy = 'Cozy'
reading = 'Concentrated'
sleep = 'Sleep'

image = 'Image'
light = 'Light'
music = 'Music'
seat_angle = 'Seat Angle'
reading_light = 'Reading Light'
entertainment_recommendation = 'Entertainment Recommendation'

turbulance = 'Turbulance'
ambiant_light = 'Ambiant Light'
safety_belt_warning = 'Safety Belt Warning'
entertainment_pause = 'Entertainment Pause'

# All paths could be handled more elegantly. More on this later
preset_global_themes = {
    quiet: { image: ['./quiet_theme/photos/q1.png', './quite_theme/photos/q2.png'], light: 20, music: './quite_theme/music_playlist' },
    engaged: { image: ['./engaged_theme/photos/e1.png', './engaged_theme/photos/e2.png'], light: 70, music: './engaged_theme/music_playlist' },
    romantic: {image: ['./romantic_theme/photos/r1.png', './romantic_theme/photos/r2.png'], light: 30, music: './romantic_theme/music_playlist' }
}

preset_personal_themes = {
    cozy: { seat_angle: 25, entertainment_recommendation: [], reading_light: 0 },
    reading: { seat_angle: 80, entertainment_recommendation: [], reading_light: 40 }
    sleep: { seat_angle: 5, entertainment_recommendation: [], reading_light: 0 }
}

action = 'action'
policy = 'policy'
context = 'context'

# Automatic adjustment rules are hardcoded as python classes
# because we don't yet plan to allow customized rules
class Rule:

    name = ''
    overridable = True

    @staticmethod
    def trigger(state):
        return False

class TurbulanceRuleGlobal(Rule):

    name = 'TurbulanceRuleGlobal'
    is_global = True
    safety_belt_threshold = 60
    safety_belt_response = { safety_belt_warning: True }
    quiet_theme_threshold = 80
    quiet_theme_response = { theme: quiet }

    def trigger(state):
        return_dic = {}
        if state[turbulance] > 60:
            return_dic.update(TurbulanceRuleGlobal.safety_belt_response)
        if state[turbulance] > 80:
            return_dic.update(TurbulanceRuleGlobal.quiet_theme_response)
        return return_dic


# This one should not be overridable. We let it be for test purposes
class TurbulanceRulePersonal(Rule):

    name = 'TurbulanceRulePersonal'
    is_global = False
    personal_entertainment_threshold = 80
    personal_entertainment_response = { entertainment_pause: True }

    override_text = 'Personal Entertainment System will be disabled due to high turbulance. ' + \
    'This is overridable only for test purposes'
    override_relevant_fields = [turbulance]

    def trigger(state):
        if state[turbulance] > TurbulanceRulePersonal.personal_entertainment_threshold:
            return TurbulanceRulePersonal.personal_entertainment_response
        return {}

adjustment_rules = [TurbulanceRuleGlobal, TurbulanceRulePersonal]
name_to_rule = { rule.name: rule for rule in adjustment_rules }
