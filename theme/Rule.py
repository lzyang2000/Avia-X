from .constants import *

# Automatic adjustment rules are hardcoded as python classes
# because we don't yet plan to allow customized rules
class Rule:

    name = ''
    overridable = True

    @staticmethod
    def trigger(state):
        return False


class TurbulenceRuleGlobal(Rule):

    name = 'TurbulenceRuleGlobal'
    is_global = True
    safety_belt_threshold = 60
    safety_belt_response = { safety_belt_warning: True }
    quiet_theme_threshold = 80
    quiet_theme_response = { theme: quiet }


    def trigger(state):
        return_dic = {safety_belt_warning: False, theme: normal, light:"bright",emotion:"neutral"}
        if state[turbulence] > 60:
            return_dic.update(TurbulenceRuleGlobal.safety_belt_response)
        if state[luminence] > 7:
            return_dic.update(TurbulenceRuleGlobal.light_response)
        if state[turbulence] > 80:
            return_dic.update(TurbulenceRuleGlobal.quiet_theme_response)
        if state[emotion] in ["sad", "angry", "fear"]:
            return_dic.update({emotion:state[emotion]})
        return return_dic


# This one should not be overridable. We let it be for test purposes
class TurbulenceRulePersonal(Rule):

    name = 'TurbulenceRulePersonal'
    is_global = False
    personal_entertainment_threshold = 80
    personal_entertainment_response = { entertainment_pause: True }

    override_text = 'Personal Entertainment System will be disabled due to high turbulence. ' + \
    'This is overridable only for test purposes'
    override_relevant_fields = [turbulence]

    def trigger(state):
        if state[turbulence] > TurbulenceRulePersonal.personal_entertainment_threshold:
            return TurbulenceRulePersonal.personal_entertainment_response
        return {}

adjustment_rules = [TurbulenceRuleGlobal, TurbulenceRulePersonal]
name_to_rule = { rule.name: rule for rule in adjustment_rules }