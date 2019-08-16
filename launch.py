
from mock_agent import Agent
from user import *
import os

# We should look into running multiple agents at once using python subprocesses
def main():
    agent = Agent()
    print(agent.user.info)

if __name__ == '__main__':
    main()
