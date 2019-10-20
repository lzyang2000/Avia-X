from . import *

class Rule():
    # Rules are not modifiable for now
    allow_modify = False

    # Returns the output state after applying the rule
    def get_state_update(state):
        pass

    # Modify the rule. 
    def modify(modification):
        raise NotImplementedError('Rule modification currently not supported')

class StateToTargetThemeMapping(Rule):

    name = 'stateToTheme'

    def get_state_update(state):
        if state[emotion] == happy:
            return { theme: engaged }
        if state[emotion] in [sad, fear, angry]:
            return { theme: warm }
        if state[turbulence] or state[pressure]:
            return { theme: quiet }
        if state[luminance] > 200:
            return { theme: warm }
        return { theme: RESET }

class SafetyBeltWarning(Rule):

    name = 'safetyBelt'

    def get_state_update(state):
        return { safety_belt_warning: state[turbulence] }


rules = [StateToTargetThemeMapping, SafetyBeltWarning]
name_to_rule = { rule.name: rule for rule in rules }
