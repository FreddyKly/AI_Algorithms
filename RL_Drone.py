ACTIONS = {'N', 'O', 'W', 'S'}

done = False

while not done:
    pass


def step(action):
    new_state = None
    rewar = None
    return new_state, reward, done




import numpy as np

class Grid:
    def __init__ (self):
        self.height = 16
        self.width = 16
        self.grid = np.zeros((self.height, self.width)) + 1

        self.start = (4, 12)
        self.goal = (13, 11)

        self.grid[0] = 1000
        self.grid[15] = 1000
        self.grid[:,0] = 1000
        self.grid[15,:] = 1000