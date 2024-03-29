import numpy as np
from matplotlib import pyplot as plt
import time
import math
import random

# Define the environment size
GRID_SIZE = 16

# Define the costs for reaching the goal state and obstacles
OBSTACLE_COST = 1000
GOAL_COST = 0

# Define the number of episodes
NUM_EPISODES = 160000

# Define the maximum number of steps per episode
MAX_STEPS = 100

# Define the agent's starting position
START_POSITION = (4, 12, 0)

# Define the goal state
GOAL_STATE = (13, 11, 0)

# Define the obstacle positions
OBSTACLES = []
for j in range(2):
    for i in range(16):
        # Left and right row
        OBSTACLES.append((0, i, j))
        OBSTACLES.append((15, i, j))
    for i in range(1, 15):
        # Top and bottom row
        OBSTACLES.append((i, 0, j))
        OBSTACLES.append((i, 15, j))
    for i in range(7, 15):
        # Bottom rectangle from (7, 13) til (14, 14)
        OBSTACLES.append((i, 13, j))
        OBSTACLES.append((i, 14, j))
    for i in range(7, 11):
        # mid rectangle from (7, 8) til (10, 12)
        OBSTACLES.append((i, 12, j))
        OBSTACLES.append((i, 11, j))
        OBSTACLES.append((i, 10, j))
        OBSTACLES.append((i, 9, j))
        OBSTACLES.append((i, 8, j))
    for i in range (7, 10):
        # Top rectangle from (7, 6) til (9, 7)
        OBSTACLES.append((i, 7, j))
        OBSTACLES.append((i, 6, j))
    

# Define the possible actions
ACTIONS = ['N', 'S', 'W', 'O', 'H', 'R']

# Initialize the Q-table with zeros
q_table = np.zeros((GRID_SIZE * GRID_SIZE * 2, len(ACTIONS)))
q_table_back = np.zeros((GRID_SIZE * GRID_SIZE * 2, len(ACTIONS)))

# Create an np-array of same size to track how often the q-value was updated
update_counts = np.zeros((GRID_SIZE * GRID_SIZE * 2, len(ACTIONS)))
update_counts_back = np.zeros((GRID_SIZE * GRID_SIZE * 2, len(ACTIONS)))

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
    learning_rate = 1 / (update_counts[idx_state][idx_action] + 1) ** (10/19)
    # learning_rate = 0.3 # Wegen deterministischer Umgebung?

    new_q_value = (1 - learning_rate) * current_q + learning_rate * (cost + min_next_q)
    # Assign new q-value
    q_table_loc[idx_state][idx_action] = new_q_value

# Map state to a unique index, corresponding to it's x and y value
def map_state_to_index(state):
    x, y, z = state
    index = y * GRID_SIZE + x + (z * GRID_SIZE * GRID_SIZE)
    # print("state: ", state, "index: ", index)
    return index

def is_converged(q_values, prev_q_values):
    threshold = 0.2
    max_diff = 0.0000
    for idx_state in range(len(q_values)):
        for idx_action in range(len(q_values[idx_state])):
            diff = abs(q_values[idx_state][idx_action] - prev_q_values[idx_state][idx_action])
            if diff > max_diff:
                max_diff = diff
    if max_diff < threshold:
        pass
    print(max_diff)

    return max_diff < threshold


# plt.ion()
fig, ax = plt.subplots(2, 1, figsize=(12, 9))
fig2, ax2 = plt.subplots(2, 1, figsize=(12, 9))
prev_q_table_back = np.zeros((GRID_SIZE * GRID_SIZE * 2, len(ACTIONS)))
# animate_q_values(q_table, 1)
convCounter = 0

# Run Q-learning algorithm
for episode in range(NUM_EPISODES):
    state = START_POSITION
    total_cost = 0
    
    for step in range(MAX_STEPS):
        epsilon = (1 / math.sqrt((episode + 1)))  # Decrease exploration rate over time
        
        action = choose_action(state, epsilon, q_table)

        air_layer_coef = state[2] + 1
        
        # Perform the chosen action and observe the next state and cost
        if action == 'N':
            next_state = (state[0], state[1] - 1 * air_layer_coef, state[2]) if (state[1] >= 1 * air_layer_coef) else state
        elif action == 'S':
            next_state = (state[0], state[1] + 1 * air_layer_coef, state[2]) if (state[1] < GRID_SIZE - 1 * air_layer_coef) else state
        elif action == 'W':
            next_state = (state[0] - 1 * air_layer_coef, state[1], state[2]) if (state[0] >= 1 * air_layer_coef) else state
        elif action == 'O':
            next_state = (state[0] + 1 * air_layer_coef, state[1], state[2]) if (state[0] < GRID_SIZE - 1 * air_layer_coef) else state
        elif action == 'H':
            next_state = (state[0], state[1], state[2] + 1) if state[2] == 0 else state
        elif action == 'R':
            next_state = (state[0], state[1], state[2] - 1) if state[2] == 1 else state

        wind_dir = random.randint(1, 4)
        if (wind_dir == 1):
            # N
            next_state = (next_state[0], next_state[1] - 1, next_state[2]) if next_state[1] > 0 else next_state
        elif (wind_dir == 2):
            # S
            next_state = (next_state[0], next_state[1] + 1, next_state[2]) if next_state[1] < GRID_SIZE - 1 else next_state
        elif (wind_dir == 3):
            # W
            next_state = (next_state[0] - 1, next_state[1], next_state[2]) if next_state[0] > 0 else next_state
        elif (wind_dir == 4):
            # O
            next_state = (next_state[0] + 1, next_state[1], next_state[2]) if next_state[0] < GRID_SIZE - 1 else next_state

        prev_q_table = q_table.copy()

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

                air_layer_coef = state[2] + 1
                
                if action == 'N':
                    next_state = (state[0], state[1] - 1 * air_layer_coef, state[2]) if (state[1] >= 1 * air_layer_coef) else state
                elif action == 'S':
                    next_state = (state[0], state[1] + 1 * air_layer_coef, state[2]) if (state[1] < GRID_SIZE - 1 * air_layer_coef) else state
                elif action == 'W':
                    next_state = (state[0] - 1 * air_layer_coef, state[1], state[2]) if (state[0] >= 1 * air_layer_coef) else state
                elif action == 'O':
                    next_state = (state[0] + 1 * air_layer_coef, state[1], state[2]) if (state[0] < GRID_SIZE - 1 * air_layer_coef) else state
                elif action == 'H':
                    next_state = (state[0], state[1], state[2] + 1) if state[2] == 0 else state
                elif action == 'R':
                    next_state = (state[0], state[1], state[2] - 1) if state[2] == 1 else state

                wind_dir = random.randint(1, 4)
                if (wind_dir == 1):
                    # N
                    next_state = (next_state[0], next_state[1] - 1, next_state[2]) if next_state[1] > 0 else next_state
                elif (wind_dir == 2):
                    # S
                    next_state = (next_state[0], next_state[1] + 1, next_state[2]) if next_state[1] < GRID_SIZE - 1 else next_state
                elif (wind_dir == 3):
                    # W
                    next_state = (next_state[0] - 1, next_state[1], next_state[2]) if next_state[0] > 0 else next_state
                elif (wind_dir == 4):
                    # O
                    next_state = (next_state[0] + 1, next_state[1], next_state[2]) if next_state[0] < GRID_SIZE - 1 else next_state
                
                prev_q_table_back = q_table_back.copy()

                if next_state == START_POSITION:
                    cost = GOAL_COST
                elif next_state in OBSTACLES:
                    # If drone hits obstacle, cost of 1000 and end of episode
                    cost = OBSTACLE_COST
                    total_cost += cost
                    update_q_table(state, action, cost, next_state, q_table_back, update_counts_back)
                    break
                else:
                    cost = 1
                
                update_q_table(state, action, cost, next_state, q_table_back, update_counts_back)
                total_cost += cost
                state = next_state
                
                if state == START_POSITION:
                    break
            # Continue episode if drone did not crash (state != GOAL_STATE e.g.)
            else:
                continue
            # If break was triggered for way back, stop the whole episode
            break
        
    # animate_q_values(q_table, 1)
    # animate_q_values(q_table_back, 2)

    if(is_converged(q_table, prev_q_table) and is_converged(q_table_back, prev_q_table_back)):
        convCounter += 1
        if convCounter >= 10:
            break
    else:
        convCounter = 0

    # Print the total cost for the episode
    print(f"Episode {episode + 1}: Total cost = {total_cost}")


# Evaluate the learned policy
state = START_POSITION
path = [state]
while state != GOAL_STATE:
    idx_state = map_state_to_index(state)
    action = ACTIONS[np.argmin(q_table[idx_state])]
    current_state = q_table[idx_state],
    print(q_table[idx_state], "chosen: ", q_table[idx_state][np.argmin(q_table[idx_state])])

    air_layer_coef = state[2] + 1
    
    if action == 'N':
        next_state = (state[0], state[1] - 1 * air_layer_coef, state[2]) if (state[1] >= 1 * air_layer_coef) else state
    elif action == 'S':
        next_state = (state[0], state[1] + 1 * air_layer_coef, state[2]) if (state[1] < GRID_SIZE - 1 * air_layer_coef) else state
    elif action == 'W':
        next_state = (state[0] - 1 * air_layer_coef, state[1], state[2]) if (state[0] >= 1 * air_layer_coef) else state
    elif action == 'O':
        next_state = (state[0] + 1 * air_layer_coef, state[1], state[2]) if (state[0] < GRID_SIZE - 1 * air_layer_coef) else state
    elif action == 'H':
        next_state = (state[0], state[1], state[2] + 1) if state[2] == 0 else state
    elif action == 'R':
        next_state = (state[0], state[1], state[2] - 1) if state[2] == 1 else state

    if next_state in path:
        path.append(next_state)
        break

    state = next_state
    path.append(state)

state = GOAL_STATE
path_back = [state]
while state != START_POSITION:
    idx_state = map_state_to_index(state)
    action = ACTIONS[np.argmin(q_table_back[idx_state])]
    
    air_layer_coef = state[2] + 1
    
    if action == 'N':
        next_state = (state[0], state[1] - 1 * air_layer_coef, state[2]) if (state[1] >= 1 * air_layer_coef) else state
    elif action == 'S':
        next_state = (state[0], state[1] + 1 * air_layer_coef, state[2]) if (state[1] < GRID_SIZE - 1 * air_layer_coef) else state
    elif action == 'W':
        next_state = (state[0] - 1 * air_layer_coef, state[1], state[2]) if (state[0] >= 1 * air_layer_coef) else state
    elif action == 'O':
        next_state = (state[0] + 1 * air_layer_coef, state[1], state[2]) if (state[0] < GRID_SIZE - 1 * air_layer_coef) else state
    elif action == 'H':
        next_state = (state[0], state[1], state[2] + 1) if state[2] == 0 else state
    elif action == 'R':
        next_state = (state[0], state[1], state[2] - 1) if state[2] == 1 else state

    if next_state in path_back:
        path_back.append(next_state)
        break
    
    state = next_state
    path_back.append(state)

# Print the optimal path
print("Optimal Path:")
for position in path:
    print(position)

print("Optimal Path back:")
for position in path_back:
    print(position)

"""
Hinweg R
"""
q_table = np.ma.masked_greater(q_table, 50)
q_table_back = np.ma.masked_greater(q_table_back, 50)

q_values = np.reshape(q_table[:256], (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values = np.min(q_values, axis=2)

norm = plt.Normalize(np.round(min_q_values, 2).min()-10, np.round(min_q_values, 2).max()+1)
colours = plt.cm.hot(norm(np.round(min_q_values, 2)))

table = ax[0].table(cellText=np.round(min_q_values, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours
                )

ax[0].axis('off')
fig.suptitle('Minimum Q-values')
ax[0].set_title('Hinweg R')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table[start_y, start_x]
goal_cell = table[goal_y, goal_x]
for cell in path:
    if cell[2] == 0:
        table[cell[1] +1, cell[0]].set_facecolor("green")
# start_cell.set_facecolor("lightblue")
# goal_cell.set_facecolor("lightblue")
start_cell.set_edgecolor("purple")
goal_cell.set_edgecolor("purple")
start_cell.set_linewidth(3)
goal_cell.set_linewidth(3)


"""
Rückweg R
"""
q_values_back = np.reshape(q_table_back[:256], (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values_back = np.min(q_values_back, axis=2)

norm_back = plt.Normalize(np.round(min_q_values_back, 2).min()-10, np.round(min_q_values_back, 2).max()+1)
colours_back = plt.cm.hot(norm_back(np.round(min_q_values_back, 2)))

table_back = ax2[0].table(cellText=np.round(min_q_values_back, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours_back)

ax2[0].axis('off')
ax2[0].set_title('Rückweg R')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table_back[start_y, start_x]
goal_cell = table_back[goal_y, goal_x]
for cell in path_back:
    if cell[2] == 0:
        table_back[cell[1] +1, cell[0]].set_facecolor("green")
# start_cell.set_facecolor("lightblue")
# goal_cell.set_facecolor("lightblue")
start_cell.set_edgecolor("purple")
goal_cell.set_edgecolor("purple")
start_cell.set_linewidth(3)
goal_cell.set_linewidth(3)



"""
Hinweg H
"""
q_values_H = np.reshape(q_table[256:], (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values_H = np.min(q_values_H, axis=2)

norm_H = plt.Normalize(np.round(min_q_values_H, 2).min()-10, np.round(min_q_values_H, 2).max()+1)
colours_H = plt.cm.hot(norm_H(np.round(min_q_values_H, 2)))

table_H = ax[1].table(cellText=np.round(min_q_values_H, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours_H)

ax[1].axis('off')
fig2.suptitle('Minimum Q-values')
ax[1].set_title('Hinweg H')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table_H[start_y, start_x]
goal_cell = table_H[goal_y, goal_x]
for cell in path:
    if cell[2] == 1:
        table_H[cell[1] +1, cell[0]].set_facecolor("green")
# start_cell.set_facecolor("lightblue")
# goal_cell.set_facecolor("lightblue")
start_cell.set_edgecolor("purple")
goal_cell.set_edgecolor("purple")
start_cell.set_linewidth(3)
goal_cell.set_linewidth(3)


"""
Rückweg H
"""
q_values_back_H = np.reshape(q_table_back[256:], (GRID_SIZE, GRID_SIZE, len(ACTIONS)))
min_q_values_back_H = np.min(q_values_back_H, axis=2)

norm_back_H = plt.Normalize(np.round(min_q_values_back_H, 2).min()-10, np.round(min_q_values_back_H, 2).max()+1)
colours_back_H = plt.cm.hot(norm_back_H(np.round(min_q_values_back_H, 2)))

table_back_H = ax2[1].table(cellText=np.round(min_q_values_back_H, 2),
                cellLoc='center',
                loc='center',
                colLabels=[str(i) for i in range(GRID_SIZE)],
                rowLabels=[str(i) for i in range(GRID_SIZE)],
                cellColours=colours_back_H)

ax2[1].axis('off')
ax2[1].set_title('Rückweg H')
start_x = 4
# For whatever reason this has to be +1
start_y = 13
goal_x = 13
# For whatever reason this has to be +1
goal_y = 12
start_cell = table_back_H[start_y, start_x]
goal_cell = table_back_H[goal_y, goal_x]
for cell in path_back:
    if cell[2] == 1:
        table_back_H[cell[1] +1, cell[0]].set_facecolor("green")
# start_cell.set_facecolor("lightblue")
# goal_cell.set_facecolor("lightblue")
start_cell.set_edgecolor("purple")
goal_cell.set_edgecolor("purple")
start_cell.set_linewidth(3)
goal_cell.set_linewidth(3)

plt.draw()
plt.show()