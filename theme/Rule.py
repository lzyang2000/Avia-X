from .constants import *

class Rule():
    # Rules are not modifiable for now
    allow_modify = False

    # Returns the output state after applying the rule
    def get_state_update(state):
        print()

    # Modify the rule. 
    def modify(modification):
        raise NotImplementedError('Rule modification currently not supported')

class StateToTargetThemeMapping(Rule):

    name = 'stateToTheme'

    def get_state_update(state):
        pass

class SafetyBeltWarning(Rule):

    name = 'safetyBelt'

    def get_state_update(state):
        pass


rules = [StateToTargetThemeMapping, SafetyBeltWarning]
name_to_rule = { rule.name: rule for rule in rules }
