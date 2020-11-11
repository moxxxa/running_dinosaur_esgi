class Agent:
    def __init__(self, environment):
        self.environment = environment
        # self.policy = Policy(environment.states.keys(), ACTIONS)
        self.reset()

    def reset(self):
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.score = 0