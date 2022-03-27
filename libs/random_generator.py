from random import uniform
from matplotlib import pyplot as plt
from libs.waypoint_generator import WaypointGenerator
from libs.check_intersect import intersects

class RandomGenerator(WaypointGenerator):

    def __init__(self, ax, fig, num_of_points, map_size, line_colour, point_colour):
        
        super().__init__(ax, fig, map_size, line_colour, point_colour)

        padding = 0.1 * self.map_size
        self.num_of_points = num_of_points
        self.spawn_area = (-self.map_size + padding, self.map_size - padding)
        self.stored = []

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

        self.x.append(uniform(*self.spawn_area))
        self.y.append(uniform(*self.spawn_area))
        
    def generate_segments(self):

        for dots in range(1, self.num_of_points + 1):
            if dots < 3:
                self.spawn_new_point()

            else:
                # Spawn third and subsequent points
                self.spawn_new_point()
                
                # Deletes and generates a new point if the segment intersects with any other segment
                self.search_for_intersects(dots)

    def search_for_intersects(self, dots):

        c = 0
        while c != dots - 2:
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
