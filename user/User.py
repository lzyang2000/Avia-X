import datetime
from . import utils
from . import mock_database as database

class User:

    class Info:
        username = 'Default User'
        birthday = 'Not Provided'
        preference = { 'global_theme': None, 'personal_theme': None, 'disabled_default_reactions': {} }
        history = []

        def __init__(self, info_dict={}):
            if 'username' in info_dict:
                self.username = info_dict['username']
            if 'birthday' in info_dict:
                self.birthday = info_dict['birthday']
            if 'preference' in info_dict:
                self.preference = info_dict['preference']
            if 'history' in info_dict:
                self.history = info_dict['history']
        
        def __str__(self):
            return 'username: {}, birthday: {}, preference: {}, history: {}'.format(self.username, self.birthday, self.preference, self.history)

    def __init__(self, agent, info=Info(), id=''):
        self.info = info
        self.agent = agent # AGENT should not be saved as a part of database; assigned to user for convenience
        if id:
            self.id = id

    @staticmethod
    def create_new_user(agent, info):
        all_user_names = database.find().keys()
        if info.username in all_user_names:
            return (None, 'User with username {} already exists. Please try a different one.').format(info.name)
        user = User(agent, info)
        user.id = utils.random_id()
        agent.complete_onboarding_process(user)
        return (user, None)

    @staticmethod
    def login(agent, id):
        user_info = database.find(id)
        user_info_obj = User.Info(user_info)
        return User(agent, user_info_obj, id)

    def get_preference(self):
        return self.info.preference

    def set_preference(self, updated_preference):
        for (theme, setting) in updated_preference.items():
            if not setting == self.info.preference[theme]:
                self.info.preference[theme] = setting
                self.log_history('set_preference', (theme, setting))
        database.save(self)

    # We could implement more sophisticated override setting in the future. We can only turn it off for now
    def manual_override(self, updating_reaction):
        action = updating_reaction[0]
        self.log_history('manual_override', updating_reaction)
        self.info.preference['disabled_default_reactions'][action] = True

    # We could implement 'add default reaction' in the future. We're sticking to existing ones for now
    def revert_manual_override(self, updating_reaction):
        action = updating_reaction[0]
        self.log_history('revert_manual_override', updating_reaction)
        del self.info.preference['disabled_default_reactions'][action]

    def log_history(self, history_type, type_specific_info):
        log_string = str(datetime.datetime.now()) + ' '
        if history_type == 'set_preference':
            theme, setting = type_specific_info
            log_string += 'Set preference: {} to {}.'.format(theme, setting)
        elif history_type == 'manual_override':
            action, policy, context = type_specific_info
            log_string += 'Manual Override: {} when {} is disabled. Context: {}.'.format(action, policy, context)
        elif history_type == 'revert_manual_override':
            action, policy = type_specific_info
            log_string += 'Revert Override: {} when {} is enabled.'.format(action, policy)
        else:
            log_string += 'Unknown operation'
        self.info.history.append(log_string)
