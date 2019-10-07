import datetime
from .constants import *
from . import user_database as database

class User:

    class Info:
        birthday = 'Not Provided'
        preference = { global_theme: None, personal_theme: None, disabled_default_reactions: {} }
        history = []

        def __init__(self, info_dict={}):
            if birthday in info_dict:
                self.birthday = info_dict[birthday]
            if preference in info_dict:
                self.preference = info_dict[preference]
            if history in info_dict:
                self.history = info_dict[history]
        
        def __str__(self):
            return 'birthday: {}, preference: {}, history: {}'.format(self.birthday, self.preference, self.history)

    def __init__(self, agent, name, info=Info()):
        self.username = name
        self.info = info
        self.agent = agent # AGENT should not be saved as a part of database; assigned to user for convenience

    @staticmethod
    def create_new_user(agent, username, info):
        all_user_names = database.find().keys()
        if username in all_user_names:
            return (None, 'User with username {} already exists. Please try a different one.'.format(username))
        user = User(agent, username, info)
        database.save(user)
        return (user, None)

    @staticmethod
    def login(agent, name):
        user_info = database.find(name)
        user_info_obj = User.Info(user_info)
        return User(agent, name, user_info_obj)

    def get_preference(self):
        return self.info.preference

    # Most commonly used
    def get_global_theme_preference(self):
        return self.info.preference[global_theme]

    def set_preference(self, updated_preference):
        for (theme, setting) in updated_preference.items():
            if not setting == self.info.preference[theme]:
                self.info.preference[theme] = setting
                self.log_history(set_preference, (theme, setting))
        database.save(self)

    def accepts_rule(self, rule_name):
        return rule_name not in self.info.preference[disabled_default_reactions]

    # We could implement more sophisticated override setting in the future. We can only turn it off for now
    def manual_override(self, updating_reaction):
        rule_name = updating_reaction[0]
        self.log_history(manual_override, updating_reaction)
        self.info.preference[disabled_default_reactions][rule_name] = True
        database.save(self)

    # We could implement 'add default reaction' in the future. We're sticking to existing ones for now
    def revert_manual_override(self, updating_reaction):
        rule_name = updating_reaction[0]
        self.log_history(revert_manual_override, updating_reaction)
        del self.info.preference[disabled_default_reactions][rule_name]
        database.save(self)

    def log_history(self, history_type, type_specific_info):
        log_string = str(datetime.datetime.now()) + ' '
        if history_type == set_preference:
            theme, setting = type_specific_info
            log_string += 'Set preference: {} to {}.'.format(theme, setting)
        elif history_type == manual_override:
            rule_name, context = type_specific_info
            log_string += 'Manual Override: {} is disabled. Context: {}.'.format(rule_name, context)
        elif history_type == revert_manual_override:
            rule_name = type_specific_info
            log_string += 'Revert Override: {} is enabled.'.format(rule_name)
        else:
            log_string += 'Unknown operation'
        self.info.history.append(log_string)
