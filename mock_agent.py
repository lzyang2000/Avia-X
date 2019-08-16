
from user import *
from theme import *

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
        self.run()

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
                print()
                self.wait_for_user_session()
        
        print('User {} login successful.'.format(self.user.info.username))

    def complete_onboarding_process(self, user):
        updated_preference = {}
        # These should have graphic display in the UI, so optimization on type recognition is not necessary
        updated_preference['global_theme'] = self.ask_and_expect_typed_response('Select your favorite cabinet theme. ', preset_global_themes.keys())
        updated_preference['personal_theme'] = self.ask_and_expect_typed_response('Select your favorite personal theme. ', preset_personal_themes.keys())
        user.set_preference(updated_preference)

    # Loop for emotion detection and all other stuff should go here
    def run(self):
        # Could run other tests here
        while True:
            pass

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
