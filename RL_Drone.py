import numpy as np
from matplotlib import pyplot as plt
import time

# Define the environment size
GRID_SIZE = 16

# Define the costs for reaching the goal state and obstacles
OBSTACLE_COST = 1000
GOAL_COST = 0

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
    # Left and right row
    OBSTACLES.append((0, i))
    OBSTACLES.append((15, i))
for i in range(1, 15):
    # Top and bottom row
    OBSTACLES.append((i, 0))
    OBSTACLES.append((i, 15))
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
q_table_back = np.zeros((GRID_SIZE * GRID_SIZE, len(ACTIONS)))

# Create an np-array of same size to track how often the q-value was updated
update_counts = np.zeros((GRID_SIZE * GRID_SIZE, len(ACTIONS)))
update_counts_back = np.zeros((GRID_SIZE * GRID_SIZE, len(ACTIONS)))

# Function to choose an action based on the Q-values
def choose_action(state, epsilon, q_table_loc):
    if np.random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        action = np.random.choice(ACTIONS)
    else:
        # Exploit: choose the action with the lowest Q-value
        idx_state = map_state_to_index(state)
        action = ACTIONS[np.argmin(q_table_loc[idx_state])]
    return action

# Function to update the Q-values
def update_q_table(state, action, cost, next_state, q_table_loc, update_counts_loc):
    # Get indeces
    idx_state = map_state_to_index(state)
    idx_next_state = map_state_to_index(next_state)
    idx_action = ACTIONS.index(action)
    # Get minimal q-value for the next state
    min_next_q = np.min(q_table_loc[idx_next_state])
    # Get the q-value of the current state
    current_q = q_table_loc[idx_state][idx_action]

    # Update learning rate
    update_counts_loc[idx_state][idx_action] += 1
    # learning_rate = 1 / update_counts[idx_state][idx_action]
    learning_rate = 0.7 # Wegen deterministischer Umgebung?

    new_q_value = (1 - learning_rate) * current_q + learning_rate * (cost + min_next_q)
    # Assign new q-value
    q_table_loc[idx_state][idx_action] = new_q_value

# Map state to a unique index, corresponding to it's x and y value
def map_state_to_index(state):
    x, y = state
    index = y * GRID_SIZE + x
    # print("state: ", state, "index: ", index)
    return index


def animate_q_values(q_table_loc, way_idx):
    q_values = np.reshape(q_table_loc, (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
    min_q_values = np.min(q_values, axis=2)

    norm = plt.Normalize(np.round(min_q_values, 2).min()-10, np.round(min_q_values, 2).max()+1)
    colours = plt.cm.hot(norm(np.round(min_q_values, 2)))
  
    table = plt.table(cellText=np.round(min_q_values, 2),
                    cellLoc='center',
                    loc='center',
                    colLabels=[str(i) for i in range(GRID_SIZE)],
                    rowLabels=[str(i) for i in range(GRID_SIZE)],
                    cellColours=colours)
    if (way_idx == 2):
        table_back = plt.table(cellText=np.round(min_q_values, 2),
                    cellLoc='center',
                    loc='center',
                    colLabels=[str(i) for i in range(GRID_SIZE)],
                    rowLabels=[str(i) for i in range(GRID_SIZE)],
                    cellColours=colours)
        ax[1].clear()
        ax[1].add_table(table_back)
        ax[1].axis('off')

    ax[0].clear()
    ax[0].add_table(table)
    ax[0].axis('off')
    fig.suptitle('Minimum Q-values')
    start_x = 4
    # For whatever reason this has to be +1
    start_y = 13
    goal_x = 13
    # For whatever reason this has to be +1
    goal_y = 12
    start_cell = table[start_y, start_x]
    goal_cell = table[goal_y, goal_x]
    start_cell.set_facecolor("lightblue")
    goal_cell.set_facecolor("lightblue")
    fig.canvas.flush_events()
    # time.sleep(0.01)

# plt.ion()
fig, ax = plt.subplots(2, 1, figsize=(12, 9))
# animate_q_values(q_table, 1)

# Run Q-learning algorithm
for episode in range(NUM_EPISODES):
    state = START_POSITION
    total_cost = 0
    
    for step in range(MAX_STEPS):
        epsilon = (1 / (episode + 1))  # Decrease exploration rate over time
        
        action = choose_action(state, epsilon, q_table)
        
        # Perform the chosen action and observe the next state and cost
        if action == 'N':
            next_state = (state[0], state[1] - 1) if state[1] > 0 else state
        elif action == 'S':
            next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
        elif action == 'W':
            next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
        elif action == 'O':
            next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state


        # Assign a cost based on the next state
        if next_state == GOAL_STATE:
            cost = GOAL_COST
        elif next_state in OBSTACLES:
            # If drone hits obstacle, cost of 1000 and end of episode
            cost = OBSTACLE_COST
            total_cost += cost
            update_q_table(state, action, cost, next_state, q_table, update_counts)
            break
        else:
            cost = 1
        
        # Update the Q-values
        update_q_table(state, action, cost, next_state, q_table, update_counts)
        
        total_cost += cost
        state = next_state

        
        if state == GOAL_STATE:
            # Agent has reached the goal, update Q-values for returning to the start
            for _ in range(MAX_STEPS):
                action = choose_action(state, epsilon, q_table_back)
                
                if action == 'N':
                    next_state = (state[0], state[1] - 1) if state[1] > 0 else state
                elif action == 'S':
                    next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
                elif action == 'W':
                    next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
                elif action == 'O':
                    next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state
                
                if next_state == START_POSITION:
                    cost = GOAL_COST
                elif next_state in OBSTACLES:
                    # If drone hits obstacle, cost of 1000 and end of episode
                    cost = OBSTACLE_COST
                    total_cost += cost
                    update_q_table(state, action, cost, next_state, q_table, update_counts)
                    break
                else:
                    cost = 1
                
                update_q_table(state, action, cost, next_state, q_table_back, update_counts_back)
                total_cost += cost
                state = next_state
                
                if state == START_POSITION:
                    break
        
    # animate_q_values(q_table, 1)
    # animate_q_values(q_table_back, 2)

    # Print the total cost for the episode
    print(f"Episode {episode + 1}: Total cost = {total_cost}")
with np.printoptions(threshold=np.inf):
    print(q_table)

q_values = np.reshape(q_table, (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values = np.min(q_values, axis=2)

norm = plt.Normalize(np.round(min_q_values, 2).min()-10, np.round(min_q_values, 2).max()+1)
colours = plt.cm.hot(norm(np.round(min_q_values, 2)))

table = ax[0].table(cellText=np.round(min_q_values, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours)

ax[0].axis('off')
fig.suptitle('Minimum Q-values')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table[start_y, start_x]
goal_cell = table[goal_y, goal_x]
start_cell.set_facecolor("lightblue")
goal_cell.set_facecolor("lightblue")



q_values_back = np.reshape(q_table_back, (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values_back = np.min(q_values_back, axis=2)

norm_back = plt.Normalize(np.round(min_q_values_back, 2).min()-10, np.round(min_q_values_back, 2).max()+1)
colours_back = plt.cm.hot(norm(np.round(min_q_values_back, 2)))

table_back = ax[1].table(cellText=np.round(min_q_values_back, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours_back)

ax[1].axis('off')
fig.suptitle('Minimum Q-values')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table_back[start_y, start_x]
goal_cell = table_back[goal_y, goal_x]
start_cell.set_facecolor("lightblue")
goal_cell.set_facecolor("lightblue")

plt.draw()
plt.show()


# # Evaluate the learned policy
# state = START_POSITION
# path = [state]
# while state != GOAL_STATE:
#     idx_state = map_state_to_index(state)
#     action = ACTIONS[np.argmax(q_table[idx_state])]
    
#     if action == 'up':
#         next_state = (state[0], state[1] - 1) if state[1] > 0 else state
#     elif action == 'down':
#         next_state = (state[0], state[1] + 1) if state[1] < GRID_SIZE - 1 else state
#     elif action == 'left':
#         next_state = (state[0] - 1, state[1]) if state[0] > 0 else state
#     elif action == 'right':
#         next_state = (state[0] + 1, state[1]) if state[0] < GRID_SIZE - 1 else state
    
#     state = next_state
#     path.append(state)

# # Print the optimal path
# print("Optimal Path:")
# for position in path:
#     print(position)