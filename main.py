import argparse
import atexit
import matplotlib.pyplot as plt
import pandas as pd
import random as rand

from libs.check_intersect import intersects

def main(args):

    def exit_handler():

        axis = {'X-axis': x, 'Y-axis': y}
        df = pd.DataFrame(axis, columns= ['X-axis', 'Y-axis'])
        df.to_csv("waypoints.csv", index = False)

    try:
        map_size = 100
        line_colour = '#F0A39A'
        point_colour = '#383831'

        fig = plt.figure()
        ax = plt.axes()
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-map_size, map_size)
        ax.set_ylim(-map_size, map_size)

        if args.random:
            x, y = rand_gen(ax, fig, args.random, map_size, line_colour, point_colour)

        elif args.click:
            click_gen(ax, fig, map_size, line_colour, point_colour)

        else:
            raise Exception("Invalid argument.")

        plt.grid()
        plt.show()
        atexit.register(exit_handler)

    except KeyboardInterrupt:
        atexit.register(exit_handler)

def click_gen(ax, fig, map_size, line_colour, point_colour):
    
    x = []
    y = []

    def onclick(event):

        x.append(event.xdata)
        y.append(event.ydata)

        ax.plot(x, y, '-', color=line_colour)
        ax.plot(x, y, '.', color=point_colour)

        fig.canvas.draw()

    def onpress(event):

        if event.key == 'z':
            try:
                x.pop()
                y.pop()

            except:
                pass
        
        elif event.key == 'x':
            del x[:]
            del y[:]

        elif event.key == 'c':
            try:
                x.append(x[0])
                y.append(y[0])

            except:
                pass
    
        else:
            pass
    
        ax.cla()
        plt.grid()
        ax.set_xlim(-map_size, map_size)
        ax.set_ylim(-map_size, map_size)
        ax.plot(x, y, '-', color=line_colour)
        ax.plot(x, y, '.', color=point_colour)
        fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', onpress)

    return x, y

def rand_gen(ax, fig, n, map_size, line_colour, point_colour):

    x = []
    y = []
    stored = []

    padding = 0.1 * map_size

    for dots in range(1, n+1):
        if dots < 3:
            x.append(rand.uniform(-map_size + padding, map_size - padding))
            y.append(rand.uniform(-map_size + padding, map_size - padding))

        else:
            x.append(rand.uniform(-map_size + padding, map_size - padding))
            y.append(rand.uniform(-map_size + padding, map_size - padding))
            
            c = 0
            while c != dots-2:
                c += 1
                while True:
                    seg1 = ((x[-1], y[-1]), (x[-2], y[-2]))
                    seg2 = ((x[-1 - c], y[-1 - c]), (x[-2 - c], y[-2 - c]))

                    if intersects(seg1, seg2) == True:
                        x.pop()
                        y.pop()
                        x.append(rand.uniform(-map_size + padding, map_size - padding))
                        y.append(rand.uniform(-map_size + padding, map_size - padding))
                        c = 1

                    else:
                        break

    ax.plot(x, y, '-', color=line_colour)
    ax.plot(x, y, '.', color=point_colour)

    stored.append([x.copy(), y.copy()])
  
    def onpress(event):

        if event.key == 'z':
            try:
                del x[:]
                del y[:]
                stored.pop()
                x.extend(stored[-1][0])
                y.extend(stored[-1][1])

            except:
                return

        elif event.key == 'x':
            del x[:]
            del y[:]

            for dots in range(1, n+1):
                if dots < 3:
                    x.append(rand.uniform(-map_size + padding, map_size - padding))
                    y.append(rand.uniform(-map_size + padding, map_size - padding))

                else:
                    x.append(rand.uniform(-map_size + padding, map_size - padding))
                    y.append(rand.uniform(-map_size + padding, map_size - padding))
                    
                    c = 0
                    while c != dots-2:
                        c += 1
                        while True:
                            seg1 = ((x[-1], y[-1]), (x[-2], y[-2]))
                            seg2 = ((x[-1 - c], y[-1 - c]), (x[-2 - c], y[-2 - c]))

                            if intersects(seg1, seg2) == True:
                                x.pop()
                                y.pop()
                                x.append(rand.uniform(-map_size + padding, map_size - padding))
                                y.append(rand.uniform(-map_size + padding, map_size - padding))
                                c = 1

                            else:
                                break

            stored.append([x.copy(), y.copy()])

        elif event.key == 'c':
            try:
                x.append(x[0])
                y.append(y[0])

            except:
                return

        else:
            return
        
        ax.cla()
        plt.grid()
        ax.set_xlim(-map_size, map_size)
        ax.set_ylim(-map_size, map_size)
        ax.plot(x, y, '-', color=line_colour)
        ax.plot(x, y, '.', color=point_colour)
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', onpress)

    return x, y

def parse_args():

    parser = argparse.ArgumentParser(description='Generator type')
    parser.add_argument('-r', '--random', type=int, metavar='', help='Generates a user-selected amount of random waypoints')
    parser.add_argument('-c', '--click', action='store_true', help='Generates user-selected waypoint positions')

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)