import atexit
import matplotlib.pyplot as plt
import pandas as pd
import random as rand

from argparse import ArgumentParser
from libs.click_generator import ClickGenerator
from libs.random_generator import RandomGenerator

def exit_handler(x, y):

    axis = {'X-axis': x, 'Y-axis': y}
    df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
    df.to_csv("waypoints.csv", index=False)

def main():

    args, _ = parse_args()

    try:
        # Parameters
        map_size = 100
        line_colour = '#F0A39A'
        point_colour = '#383831'

        fig = plt.figure()
        ax = plt.axes()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-map_size, map_size)
        ax.set_ylim(-map_size, map_size)

        if args.random:
            rand_gen = RandomGenerator(ax, fig, args.random, map_size, line_colour, point_colour)
            x, y = rand_gen.generate()

        elif args.click:
            click_gen = ClickGenerator(ax, fig, map_size, line_colour, point_colour)
            x, y = click_gen.generate()

        else:
            raise Exception("Invalid argument.")

        plt.grid()
        plt.show()
        atexit.register(exit_handler, x, y)

    except KeyboardInterrupt:
        atexit.register(exit_handler, x, y)

def parse_args():

    parser = ArgumentParser(description='Generator type')
    parser.add_argument('-r', '--random', type=int, metavar='', help='Generates a user-selected amount of random waypoints')
    parser.add_argument('-c', '--click', action='store_true', help='Generates user-selected waypoint positions')

    return parser.parse_known_args()

if __name__ == '__main__':
    main()
