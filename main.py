import argparse
import atexit
import matplotlib.pyplot as plt
import pandas as pd
import random as rand

def main(args):

    def exit_handler():

        axis = {'X-axis': x, 'Y-axis': y}
        df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
        df.to_csv("data/waypoints.csv", index = False)

    try:
        map_size = 100

        fig = plt.figure()
        ax = plt.axes()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-map_size, map_size)
        ax.set_ylim(-map_size, map_size)

        if args.random:
            x, y = rand_gen(ax, fig, args.random, map_size)

        elif args.click:
            x, y = click_gen(ax, fig)

        else:
            raise Exception("Invalid argument.")

        plt.show()
        atexit.register(exit_handler)

    except KeyboardInterrupt:
        atexit.register(exit_handler)

def click_gen(ax, fig):
    
    x = []
    y = []

    def onclick(event):

        x.append(event.xdata)
        y.append(event.ydata)

        ax.plot(x, y, '-r')
        ax.plot(x, y, 'bo')

        fig.canvas.draw()
        
    fig.canvas.mpl_connect('button_press_event', onclick)

    return x, y

def rand_gen(ax, fig, n, map_size):

    x = []
    y = []
    
    for _ in range(0, n):
        x.append(rand.uniform(-map_size + 10, map_size - 10))
        y.append(rand.uniform(-map_size + 10, map_size - 10))

    ax.plot(x, y, '-r')
    ax.plot(x, y, 'bo')   

    return x, y

def parse_args():

    parser = argparse.ArgumentParser(description='Generator type')
    parser.add_argument('-r', '--random', type=int, metavar='', help='Generates a user-selected amount of random waypoints')
    parser.add_argument('-c', '--click', action='store_true', help='Generates user-selected waypoint positions')

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)