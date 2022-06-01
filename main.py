import csv

from argparse import ArgumentParser
from atexit import register
from matplotlib import pyplot as plt
from libs.click_generator import ClickGenerator
from libs.random_generator import RandomGenerator

def exit_handler(x, y, z):

    with open("waypoints.csv", "w", newline='') as f:
        writer = csv.writer(f)

        if z:
            writer.writerow(['x', 'y', 'z'])
            writer.writerows(zip(x, y, z))

        else:
            writer.writerow(['x', 'y'])
            writer.writerows(zip(x, y))

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
        z = None

        if args.random:
            rand_gen = RandomGenerator(ax, fig, args.random, map_size, line_colour, point_colour)
            x, y = rand_gen.generate()

        elif args.click:
            use_z = args.three_dimension
            scroll_sensitivity = args.scroll_sensitivity
            click_gen = ClickGenerator(ax, fig, map_size, line_colour, point_colour, use_z, scroll_sensitivity)
            x, y, z = click_gen.generate()

        else:
            raise Exception("Invalid argument.")

        plt.grid()
        plt.show()
        register(exit_handler, x, y, z)

    except KeyboardInterrupt:
        register(exit_handler, x, y, z)

def parse_args():

    parser = ArgumentParser(description='Generator type')
    parser.add_argument('-r', '--random', type=int, metavar='', help='Generates a user-selected amount of random waypoints')
    parser.add_argument('-c', '--click', action='store_true', help='Generates user-selected waypoint positions')
    parser.add_argument('-3d', '--three-dimension', action='store_true', help='Allows user to change the z-axis of a created waypoint')
    parser.add_argument('--scroll-sensitivity', type=float, metavar='', help='Sets the scroll sensitivity of the mouse when setting the z-axis')

    return parser.parse_known_args()

if __name__ == '__main__':
    main()
