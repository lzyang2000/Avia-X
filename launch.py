
from mock_agent import Agent
from user import *
from theme import *
import time

class Session:

    def __init__(self):
        self.agents = []

    def run(self):
        while(True):
            time.sleep(5)
            state = self.gather_state()
            self.handle_state(state)

    def new_agent_login(self, agent):
        self.agents.append(agent)

    def gather_state(self):
        return { turbulance: 85 }

    def handle_state(self, state):
        global_triggers = {}
        personal_triggers = {}
        for rule in adjustment_rules:
            trigger_result = rule.trigger(state)
            if trigger_result:
                if rule.is_global:
                    global_triggers.update({ rule.name: trigger_result })
                else:
                    personal_triggers.update({ rule.name: trigger_result })
        self.handle_global_triggers(global_triggers)

        print('Following personal adjustments triggered: {}'.format(personal_triggers.keys()))
        for agent in self.agents:
            agent.handle_automatic_adjustments(personal_triggers, state)

    # TODO: discuss how to override a global rule trigger
    def handle_global_triggers(self, triggers):
        pass

# We should look into running multiple agents at once using python subprocesses
def main():
    session = Session()
    agent = Agent()
    # print(agent.user.info)

    session.new_agent_login(agent)
    session.run()

if __name__ == '__main__':
    main()
