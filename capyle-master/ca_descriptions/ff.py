# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
import math 
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
from tile import Tile


# this sets the states of the transion 
# where we wil set all out states and parametes 
def transition_func(grid, neighbourstates, neighbourcounts):
    # # dead = state == 0, live = state == 1
    # # unpack state counts for state 0 and state 1
    # dead_neighbours, live_neighbours = neighbourcounts
    # # create boolean arrays for the birth & survival rules
    # # if 3 live neighbours and is dead -> cell born
    # birth = (live_neighbours == 3) & (grid == 0)
    # # if 2 or 3 live neighbours and is alive -> survives
    # survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # # Set all cells to 0 (dead)
    # #grid[50:, :] = 1
    # tiles = np.zeros([len(grid),len(grid)], dtype=Tile)
    # print(len(grid))
    # for i in range(len(grid) -1):
    #     for j in range (len(grid-1)):
    #         tiles[i, j] = Tile
    #         if i < 100:
    #             grid[i, j] = 1
    #         else:
    # #             grid[i,j] = 0

    # # Set cells to 1 where either cell is born or survives
    # grid[birth | survive] = 1
    return grid

# def prob_fire():
#     # set these for later 
#     prob_gradient
#     prob_wind
#     catch_fire

#     return prob_gradient * prob_wind * catch_fire

def get_prob_gradient(gradient):

    prob_gradient = 1 / 1 + math.e ** -gradient

    return prob_gradient



def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    # 2 = lake, 3 = dence forest, 4= canyon, 5 = chaporal, 6 = fire
    config.states = (0, 1, 2, 3, 4, 5, 6)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    #config.state_colors = [(1,0,1),(1,1,1)]
    # config.num_generations = 150
    # config.grid_dims = (200,200)

    # ----------------------------------------------------------------------

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
