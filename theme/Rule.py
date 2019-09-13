from .constants import *

# Automatic adjustment rules are hardcoded as python classes
# because we don't yet plan to allow customized rules
class Rule:

    name = ''
    overridable = True
    triggered = False

    @staticmethod
    def trigger(state):
        return False


class TurbulenceRuleGlobal(Rule):

    name = 'TurbulenceRuleGlobal'
    is_global = True
    safety_belt_threshold = 60
    safety_belt_response = { safety_belt_warning: True }
    warm_theme_threshold = 70
    warm_theme_response = { theme: warm }
    quiet_theme_threshold = 80
    quiet_theme_response = { theme: quiet }

    def trigger(state):
        if TurbulenceRuleGlobal.triggered:
            return
        # return_dic = {safety_belt_warning: False, theme: normal}
        return_dic = {}
        if state[turbulence] > TurbulenceRuleGlobal.safety_belt_threshold:
            return_dic.update(TurbulenceRuleGlobal.safety_belt_response)
        if state[luminence] > TurbulenceRuleGlobal.warm_theme_threshold or state[emotion] in ["sad", "angry", "fear"]:
            return_dic.update(TurbulenceRuleGlobal.warm_theme_response)
        if state[turbulence] > TurbulenceRuleGlobal.quiet_theme_threshold:
            return_dic.update(TurbulenceRuleGlobal.quiet_theme_response)
        if return_dic:
            TurbulenceRuleGlobal.triggered = True
            TurbulenceRuleGlobalRemove.triggered = False
        return return_dic

class TurbulenceRuleGlobalRemove(TurbulenceRuleGlobal):

    name = 'TurbulenceRuleGlobalRemove'
    triggered = True
    safety_belt_response = { safety_belt_warning: False }
    normal_theme_response = { theme: normal }

    def trigger(state):
        if TurbulenceRuleGlobalRemove.triggered:
            return
        return_dic = {}
        if state[turbulence] < TurbulenceRuleGlobalRemove.safety_belt_threshold:
            return_dic.update(TurbulenceRuleGlobalRemove.safety_belt_response)
            if not state[theme] == normal:
                return_dic.update(TurbulenceRuleGlobalRemove.normal_theme_response)
            
            TurbulenceRuleGlobal.triggered = False
            TurbulenceRuleGlobalRemove.triggered = True
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

adjustment_rules = [TurbulenceRuleGlobal, TurbulenceRuleGlobalRemove, TurbulenceRulePersonal]
name_to_rule = { rule.name: rule for rule in adjustment_rules }
