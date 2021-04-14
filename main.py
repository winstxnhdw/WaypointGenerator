import argparse
import atexit
import matplotlib.pyplot as plt
import pandas as pd
import random as rand

from libs.check_intersect import intersects

class ClickGenerator:

    def __init__(self, ax, fig, map_size, line_colour, point_colour):
        
        self.x = []
        self.y = []

        self.ax = ax
        self.fig = fig
        self.map_size = map_size
        self.line_colour = line_colour
        self.point_colour = point_colour

    def generate(self):

        def onclick(event):

            self.x.append(event.xdata)
            self.y.append(event.ydata)

            self.ax.plot(self.x, self.y, '-', color=self.line_colour)
            self.ax.plot(self.x, self.y, '.', color=self.point_colour)

            self.fig.canvas.draw()

        def onpress(event):

            # Undo last point
            if event.key == 'z':
                try:
                    self.x.pop()
                    self.y.pop()

                except IndexError:
                    pass
            
            # Clear all the points
            elif event.key == 'x':
                del self.x[:]
                del self.y[:]

            # Connect the first and last points
            elif event.key == 'c':
                try:
                    self.x.append(self.x[0])
                    self.y.append(self.y[0])

                except IndexError:
                    pass
        
            else:
                pass
        
            plt.cla()
            plt.grid()
            self.ax.set_xlim(-self.map_size, self.map_size)
            self.ax.set_ylim(-self.map_size, self.map_size)
            self.ax.plot(self.x, self.y, '-', color=self.line_colour)
            self.ax.plot(self.x, self.y, '.', color=self.point_colour)
            self.fig.canvas.draw()

        self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.fig.canvas.mpl_connect('key_press_event', onpress)

        return self.x, self.y

class RandomGenerator:

    def __init__(self, ax, fig, n, map_size, line_colour, point_colour):
        
        self.x = []
        self.y = []
        self.stored = []

        self.ax = ax
        self.fig = fig
        self.n = n
        self.map_size = map_size
        self.line_colour = line_colour
        self.point_colour = point_colour

    def generate(self):
    
        self.generate_segments()
        self.stored.append([self.x.copy(), self.y.copy()])

        self.ax.plot(self.x, self.y, '-', color=self.line_colour)
        self.ax.plot(self.x, self.y, '.', color=self.point_colour)

        def onpress(event):

            # Delete current points and return to a previously generated set of points
            if event.key == 'z':
                if len(self.stored) > 1:
                    del self.x[:]
                    del self.y[:]
                    self.stored.pop()
                    self.x.extend(self.stored[-1][0])
                    self.y.extend(self.stored[-1][1])

                else:
                    return

            # Generate a new set of points
            elif event.key == 'x':
                del self.x[:]
                del self.y[:]

                self.generate_segments()
                self.stored.append([self.x.copy(), self.y.copy()])

            # Connect the first and last points
            elif event.key == 'c':
                try:
                    self.x.append(self.x[0])
                    self.y.append(self.y[0])

                except IndexError:
                    return

            else:
                return
            
            plt.cla()
            plt.grid()
            self.ax.set_xlim(-self.map_size, self.map_size)
            self.ax.set_ylim(-self.map_size, self.map_size)
            self.ax.plot(self.x, self.y, '-', color=self.line_colour)
            self.ax.plot(self.x, self.y, '.', color=self.point_colour)
            self.fig.canvas.draw()

        self.fig.canvas.mpl_connect('key_press_event', onpress)

        return self.x, self.y

    def spawn_new_point(self):

        padding = 0.1 * self.map_size
        self.x.append(rand.uniform(-self.map_size + padding, self.map_size - padding))
        self.y.append(rand.uniform(-self.map_size + padding, self.map_size - padding))
        
    def generate_segments(self):

        for dots in range(1, self.n+1):
            if dots < 3:
                self.spawn_new_point()

            else:
                # Spawn third and subsequent points
                self.spawn_new_point()
                
                # Deletes and generates a new point if the segment intersects with any other segment
                self.search_for_intersects(dots)

    def search_for_intersects(self, dots):

        c = 0
        while c != dots-2:
            c += 1
            while True:
                seg1 = ((self.x[-1], self.y[-1]), (self.x[-2], self.y[-2]))
                seg2 = ((self.x[-1 - c], self.y[-1 - c]), (self.x[-2 - c], self.y[-2 - c]))

                # Checks if the segments intersect
                if intersects(seg1, seg2) == True:
                    self.x.pop()
                    self.y.pop()
                    self.spawn_new_point()
                    c = 1

                else:
                    break

def main(args):

    def exit_handler():

        axis = {'X-axis': x, 'Y-axis': y}
        df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
        df.to_csv("waypoints.csv", index = False)

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
        atexit.register(exit_handler)

    except KeyboardInterrupt:
        atexit.register(exit_handler)

def parse_args():

    parser = argparse.ArgumentParser(description='Generator type')
    parser.add_argument('-r', '--random', type=int, metavar='', help='Generates a user-selected amount of random waypoints')
    parser.add_argument('-c', '--click', action='store_true', help='Generates user-selected waypoint positions')

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)