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

class SafetyBeltRule(Rule):
    name = 'SafetyBeltRule'
    is_global = True
    threshold = 60
    response = { safety_belt_warning: True }
    
    def trigger(state):
        if SafetyBeltRule.triggered:
            return
        if state[turbulence] > SafetyBeltRule.threshold:
            SafetyBeltRule.triggered = True
            SafetyBeltRuleRemove.triggered = False
            return SafetyBeltRule.response

class SafetyBeltRuleRemove(SafetyBeltRule):
    name = 'SafetyBeltRuleRemove'
    triggered = True
    response = { safety_belt_warning: False }

    def trigger(state):
        if SafetyBeltRuleRemove.triggered:
            return
        if state[turbulence] < SafetyBeltRuleRemove.threshold:
            SafetyBeltRule.triggered = False
            SafetyBeltRuleRemove.triggered = True
            return SafetyBeltRuleRemove.response

class QuietOnTurbulenceRule(Rule):
    name = 'QuietOnTurbulenceRule'
    is_global = True
    threshold = 80
    response = { theme: quiet }

    def trigger(state):
        if QuietOnTurbulenceRule.triggered:
            return
        if state[turbulence] > QuietOnTurbulenceRule.threshold:
            QuietOnTurbulenceRule.triggered = True
            QuietOnTurbulenceRuleRemove.triggered = False
            return QuietOnTurbulenceRule.response

class QuietOnTurbulenceRuleRemove(QuietOnTurbulenceRule):
    name = 'QuietOnTurbulenceRuleRemove'
    triggered = True
    response = { theme: 'preference' }

    def trigger(state):
        if QuietOnTurbulenceRuleRemove.triggered:
            return
        if state[turbulence] < QuietOnTurbulenceRuleRemove.threshold:
            QuietOnTurbulenceRule.triggered = False
            QuietOnTurbulenceRuleRemove.triggered = True
            return QuietOnTurbulenceRuleRemove.response

class WarmOnLuminanceRule(Rule):
    name = 'WarmOnLuminanceRule'
    response = { theme: warm }
    is_global = True
    threshold = 7

    def trigger(state):
        if WarmOnLuminanceRule.triggered:
            return
        if state[luminance] > WarmOnLuminanceRule.threshold:
            WarmOnLuminanceRule.triggered = True
            WarmOnLuminanceRuleRemove.triggered = False
            return WarmOnLuminanceRule.response

class WarmOnLuminanceRuleRemove(WarmOnLuminanceRule):
    name = 'WarmOnLuminanceRuleRemove'
    triggered = True
    response = { theme: 'preference' }

    def trigger(state):
        if WarmOnLuminanceRuleRemove.triggered:
            return
        if state[luminance] < WarmOnLuminanceRule.threshold:
            WarmOnLuminanceRule.triggered = False
            WarmOnLuminanceRuleRemove.triggered = True
            return WarmOnLuminanceRuleRemove.response


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

adjustment_rules = [WarmOnLuminanceRule, WarmOnLuminanceRuleRemove, QuietOnTurbulenceRule, QuietOnTurbulenceRuleRemove, SafetyBeltRule, SafetyBeltRuleRemove, TurbulenceRulePersonal]
name_to_rule = { rule.name: rule for rule in adjustment_rules }
