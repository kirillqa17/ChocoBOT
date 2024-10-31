import random

def get_random_user_agent():
    with open('userAgents.txt', 'r') as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()

