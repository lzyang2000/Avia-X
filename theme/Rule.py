from .constants import *

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
