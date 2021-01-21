from src.agent import *

def main():
    """ Main method """
    env = Environment()
    agent = Agent(env)
    window = Window(agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
