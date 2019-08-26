
from user import *
from theme import *
<<<<<<< HEAD
from user import mock_database as database
=======
import time
>>>>>>> fbf0ee61db78fcdf23b844859d085b2136886b59

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
        current_user_data = database.find()
        user_credentials = []
        if current_user_data:
            user_credentials = [(data['username'], user_id) for (user_id, data) in current_user_data.items()]
            displayable_user_info = [data['username'] for data in current_user_data.values()] # Could do an image? Just username for now
            self.display_current_users(displayable_user_info)

        user_input = self.ask_and_expect_typed_response("Please type your username to log in. Type '{}' to create a new user.".format(NEW_USER_COMMAND))

        if user_input.upper() == NEW_USER_COMMAND:
            user_info = self.capture_new_user_info()
            user_created, error_msg = User.create_new_user(self, user_info)
            if user_created:
                self.user = user_created
            else:
                display_error_msg(error_msg)
        else:
            matched_user_id = self.login_command(user_input, user_credentials)
            if matched_user_id:
                self.user = User.login(self, matched_user_id)
            else:
                print('User {} not found.'.format(user_input))
                self.wait_for_user_session()
<<<<<<< HEAD
=======

>>>>>>> fbf0ee61db78fcdf23b844859d085b2136886b59
        print('User {} login successful.'.format(self.user.info.username))
        

        # if not hasattr(self.user.info, 'on_board') or not self.user.info.on_board:
        if not self.user.info.on_board:
            print("You haven't set your initial prefereces yet...")
            self.complete_onboarding_process(self.user)
            self.user.info.on_board = True
            database.save(self.user)
            print("A???")
        else:
            print("HIIII")
            print("Waiting for further #TODO")
            # pass

        self.wait_for_user_session()

    def complete_onboarding_process(self, user):
        updated_preference = {}
        # These should have graphic display in the UI, so optimization on type recognition is not necessary
        updated_preference['global_theme'] = self.ask_and_expect_typed_response('Select your favorite cabinet theme. ', preset_global_themes.keys())
        updated_preference['personal_theme'] = self.ask_and_expect_typed_response('Select your favorite personal theme. ', preset_personal_themes.keys())
        user.set_preference(updated_preference)
        print('Onboard successful')
        # self.wait_for_user_session()

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
                print('{} has disabled rule {}'.format(self.user.info.username, rule_name))

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
        username = self.ask_and_expect_typed_response("Please type your username.")
        # UI should use smarter birthday input, so we don't waste time on implementing birthday check here
        birthday = self.ask_and_expect_typed_response("Please type your birthday.")
        return User.Info({ 'username': username, 'birthday': birthday })

    def display_error_msg(self, msg):
        print(msg)

    # Just name for now
    def login_command(self, user_input, user_credentials):
        for (username, user_id) in user_credentials:
            if username == user_input:
                return user_id

    def log_out(self):
        self.user = None
        current_user_data = database.find()
        self.wait_for_user_session(current_user_data)
