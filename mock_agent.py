
from user import *
from theme import *
import time

NEW_USER_COMMAND = 'NEW USER'
SKIP_COMMAND = 'SKIP'

"""
The agent User uses to interact with the system.
This is a terminal agent for test purpose.
"""
class Agent:

    user = None

    def __init__(self):
        self.wait_for_user_session()

    def wait_for_user_session(self):
        current_user_data = user_database.find()
        existing_users = []
        if current_user_data:
            existing_users = [username for (username, data) in current_user_data.items()]
            self.display_current_users(existing_users)

        user_input = self.ask_and_expect_typed_response("Please type your username to log in. Type '{}' to create a new user.".format(NEW_USER_COMMAND))

        if user_input.upper() == NEW_USER_COMMAND:
            username, user_info = self.capture_new_user_info()
            user_created, error_msg = User.create_new_user(self, username, user_info)
            if user_created:
                self.user = user_created
            else:
                display_error_msg(error_msg)
        else:
            matched_username = self.login_command(user_input, existing_users)
            if matched_username:
                self.user = User.login(self, matched_username)
            else:
                print('User {} not found.'.format(user_input))
                print()
                self.wait_for_user_session()

        print('User {} login successful.'.format(self.user.username))

    def complete_onboarding_process(self, user):
        print(2)
        updated_preference = {}
        # These should have graphic display in the UI, so optimization on type recognition is not necessary
        updated_preference['global_theme'] = self.ask_and_expect_typed_response('Select your favorite cabinet theme. ', name_to_global_theme.keys())
        updated_preference['personal_theme'] = self.ask_and_expect_typed_response('Select your favorite personal theme. ', name_to_personal_theme.keys())
        user.set_preference(updated_preference)

    # TODO: settle on a way to implement delayed override
    # This is a "creative" solution. I know. But it's much simpler than many other solutions
    def wait_for_override_input(self, text):
        sleep_time = 8
        print(text)
        try:
            for t in range(sleep_time, 0, -1):
                print('Please press Ctrl-C in {} seconds to override this change.'.format(t))
                time.sleep(1)
        except KeyboardInterrupt:
            print('Change overrided')
            return True

    def handle_automatic_adjustments(self, trigger_results, state):
        effective_results = {}
        for rule_name in trigger_results:
            if self.user.accepts_rule(rule_name):
                effective_results[rule_name] = trigger_results[rule_name]
            else:
                print('{} has disabled rule {}'.format(self.user.username, rule_name))

        overrided_rules = []

        # The console agent can only handle overrides sequentially
        for rule_name in effective_results:
            rule = name_to_rule[rule_name]
            if rule.overridable:
                overrided = self.wait_for_override_input(rule.override_text)
                if overrided:
                    context_info = ', '.join(['{}={}'.format(param, value) for param, value in state.items() if param in rule.override_relevant_fields])
                    self.user.manual_override((rule_name, context_info))
                    overrided_rules.append(rule_name)

        for rule_name in overrided_rules:
            del effective_results[rule_name]

        print(effective_results)

    def customize_theme(self, theme, change):
        new_theme_dic = dict(theme.to_dict())
        new_theme_dic.update(change)
        original_theme_dic = name_to_theme[theme.name]().to_dict()
        if new_theme_dic == original_theme_dic:
            self.reset_theme(theme.name)
        else:
            customized_theme = CustomizedTheme.create(new_theme_dic, theme.name)
            theme_database.save(self.user.username, customized_theme)

    # theme retrieval is done by agent because theme is user specific
    def retrieve_theme(self, theme_name):
        customized_theme_dict = theme_database.find(self.user.username, theme_name)
        if customized_theme_dict:
            return CustomizedTheme.create(customized_theme_dict, theme_name)
        return name_to_theme[theme_name]()

    def reset_theme(self, theme_name):
        theme_database.remove(self.user.username, theme_name)

    def display_current_users(self, displayed_user_info):
        print('Current Users:')
        for username in displayed_user_info:
            print('Username: {}'.format(username))

    def ask_and_expect_typed_response(self, question, options=[]):
        if options:
            print(question + 'Please choose from: {}. Type {} to skip.'.format(options, SKIP_COMMAND))
            while True:
                answer = input()
                if answer in options:
                    return answer
                if answer.upper() == SKIP_COMMAND:
                    return None
                print('{} is not a valid choice.'.format(answer))
        print(question)
        return input()

    def capture_new_user_info(self):
        _username = self.ask_and_expect_typed_response("Please type your username.")
        # UI should use smarter birthday input, so we don't waste time on implementing birthday check here
        _birthday = self.ask_and_expect_typed_response("Please type your birthday.")
        return _username, User.Info({ birthday: _birthday })

    def display_error_msg(self, msg):
        print(msg)

    # Just name for now
    def login_command(self, user_input, existing_users):
        for username in existing_users:
            if username == user_input:
                return username

    def log_out(self):
        self.user = None
        current_user_data = user_database.find()
        self.wait_for_user_session(current_user_data)


class GUIAgent(Agent):
    def __init__(self, username, theme):
        user_created, error_msg = User.create_new_user(self, username, User.Info())
        self.user = user_created
        self.user.set_preference({'global_theme':theme})