import numpy as np

# Define the environment size
GRID_SIZE = 16

# Define the rewards for reaching the goal state and obstacles
OBSTACLE_COST = 1000
GOAL_REWARD = 100

# Define the learning rate
LEARNING_RATE = 0.1

# Define the number of episodes
NUM_EPISODES = 1000

# Define the maximum number of steps per episode
MAX_STEPS = 100

# Define the agent's starting position
START_POSITION = (4, 12)

# Define the goal state
GOAL_STATE = (13, 11)

# Define the obstacle positions
OBSTACLES = []
for i in range(16):
    # Top and bottom row
    OBSTACLES.append((0, i))
    OBSTACLES.append((15, i))
for i in range(1, 15):
    # Left and right row
    OBSTACLES.append((i, 0))
    OBSTACLES.append((0, i))
for i in range(7, 15):
    # Bottom rectangle from (7, 13) til (14, 14)
    OBSTACLES.append((i, 13))
    OBSTACLES.append((i, 14))
for i in range(7, 11):
    # mid rectangle from (7, 8) til (10, 12)
    OBSTACLES.append((i, 12))
    OBSTACLES.append((i, 11))
    OBSTACLES.append((i, 10))
    OBSTACLES.append((i, 9))
    OBSTACLES.append((i, 8))
for i in range (7, 10):
    # Top rectangle from (7, 6) til (9, 7)
    OBSTACLES.append((i, 7))
    OBSTACLES.append((i, 6))
    

# Define the possible actions
ACTIONS = ['N', 'S', 'W', 'O']

# Initialize the Q-table with zeros
q_table = np.zeros((GRID_SIZE * GRID_SIZE, len(ACTIONS)))

# Function to choose an action based on the Q-values
def choose_action(state, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        action = np.random.choice(ACTIONS)
    else:
        # Exploit: choose the action with the lowest Q-value
        action = ACTIONS[np.argmin(q_table[state])]
    return action

# Function to update the Q-values
def update_q_table(state, action, reward, next_state):
    min_next_q = np.min(q_table[next_state])
    current_q = q_table[state[0]][state[1]][action] 
    q_table[state][action] = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward * min_next_q)

# Map state to a unique index, corresponding to it's x and y value
def map_state_to_index(state):
    x, y = state
    index = y * GRID_SIZE + x
    return index

# Run Q-learning algorithm
for episode in range(NUM_EPISODES):
    state = START_POSITION
    total_reward = 0
    
    for step in range(MAX_STEPS):
        epsilon = (1 / (episode + 1))  # Decrease exploration rate over time
        
        action = choose_action(state, epsilon)
        
        # Perform the chosen action and observe the next state and reward
        if action == 'N':
            next_state = (state[0], state[1] - 1) if state[1] > 0 else state
        elif action == 'S':
            next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
        elif action == 'W':
            next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
        elif action == 'O':
            next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state
        print(next_state)
        
        # Assign a reward based on the next state
        if next_state == GOAL_STATE:
            reward = GOAL_REWARD
        elif next_state in OBSTACLES:
            reward = OBSTACLE_COST
        else:
            reward = 1
        
        # Update the Q-values
        update_q_table(state, action, reward, next_state)
        
        total_reward += reward
        state = next_state
        
        if state == GOAL_STATE:
            # Agent has reached the goal, update Q-values for returning to the start
            for _ in range(MAX_STEPS):
                action = choose_action(state, epsilon)
                
                if action == 'up':
                    next_state = (state[0], state[1] - 1) if state[1] > 0 else state
                elif action == 'down':
                    next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
                elif action == 'left':
                    next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
                elif action == 'right':
                    next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state
                
                if next_state == START_POSITION:
                    reward = GOAL_REWARD
                else:
                    reward = -1
                
                update_q_table(state, action, reward, next_state)
                total_reward += reward
                state = next_state
                
                if state == START_POSITION:
                    break
        
        if state == START_POSITION:
            break
    
    # Print the total reward for the episode
    print(f"Episode {episode + 1}: Total Reward = {total_reward}")

# Evaluate the learned policy
state = START_POSITION
path = [state]
while state != GOAL_STATE:
    action = ACTIONS[np.argmax(q_table[state])]
    
    if action == 'up':
        next_state = (state[0], state[1] - 1) if state[1] > 0 else state
    elif action == 'down':
        next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
    elif action == 'left':
        next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
    elif action == 'right':
        next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state
    
    state = next_state
    path.append(state)

# Print the optimal path
print("Optimal Path:")
for position in path:
    print(position)