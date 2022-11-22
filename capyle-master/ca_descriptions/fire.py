import inspect
import math
import random
import sys

import numpy as np

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')


import capyle.utils as utils
from capyle.ca import Grid2D, Neighbourhood, randomise2d


CHAPARRAL, DENSE_FORREST, LAKE, CANYON, FIRE, BURNT = range(6)

initial_grid = np.zeros((200, 200), dtype=int)
initial_grid[20:70, 60:100] = 1  # top part of the forest
initial_grid[80:140, 0:100] = 1  # bottom part of the forest
initial_grid[70:80, 20:100] = 2  # lake
initial_grid[20:160, 120:130] = 3  # canyon
initial_grid[0:1, 0:1] = 4  # initial fire


def transition_func(grid, neighbourstates, neighbourcounts):
    neighbourstates = np.array(neighbourstates)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            #state = probability(cell, neighbourstates[:, i, j])
            if cell == 4:
                state = end_burn(i, j, cell)
            else:
                state = probability(cell, neighbourstates[:, i, j])
            grid[i, j] = state

    return grid


def end_burn(i, j, cell):
    fire_end_prob = 0
    state = cell

    # chaparal
    if initial_grid[i, j] == 0:
        fire_end_prob = 0.005
    # dense forest
    elif initial_grid[i, j] == 1:
        fire_end_prob = 0.009
    # canyon
    elif initial_grid[i, j] == 3:
        fire_end_prob = 0.4

    if fire_end_prob > random.uniform(0, 1):
        state = 5
    return state


def probability(cell, neighbourstates):
    fire_prob = 0
    state = cell

    for i in neighbourstates:
        # chaparal
        if i == 4 and cell == 0:
            fire_prob = 0.2
        # dense forest
        elif i == 4 and cell == 1:
            fire_prob = 0.05
        elif i == 4 and cell == 2:
            fire_prob = 0.0
        # canyon
        elif i == 4 and cell == 3:
            fire_prob = 0.7
        elif i == 4 and cell == 5:
            fire_prob = 0.0
    if fire_prob > random.uniform(0, 1):
        state = 4
    return state


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5)

    config.num_generations = 500
    config.grid_dims = (200, 200)
    config.wrap = False

    config.state_colors = \
        [
            (0.6, 0.6, 0),  # chaparral
            (0, 0.4, 0),  # dense forrest
            (0, 0.5, 1),  # lake
            (1, 1, 0),  # canyon
            (1, 0, 0),  # fire
            (0.4, 0.2, 0.1)  # burnt
        ]

    config.set_initial_grid(initial_grid)

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    # this is where we need to insitialise the states and values
    # takes GRid2d class
    # tranision_func is passed onto the class
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    # this is where we will save all the chaging value in each run
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
