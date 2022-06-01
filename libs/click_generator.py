from matplotlib import pyplot as plt
from libs.waypoint_generator import WaypointGenerator

class ClickGenerator(WaypointGenerator):

    def __init__(self, ax, fig, map_size, line_colour, point_colour, use_z, scroll_sensitivity):
        
        super().__init__(ax, fig, map_size, line_colour, point_colour)

        self.use_z = use_z
        self.scroll_sensitivity = scroll_sensitivity if scroll_sensitivity else 1
        self.z = []

    def generate(self):

        def update_plot():

            plt.cla()
            plt.grid()
            self.ax.plot(self.x, self.y, '-', color=self.line_colour)
            self.ax.plot(self.x, self.y, '.', color=self.point_colour)
            self.ax.set_xlim(-self.map_size, self.map_size)
            self.ax.set_ylim(-self.map_size, self.map_size)

            if self.use_z:
                for x, y, z in zip(self.x, self. y, self.z):
                    # Use round() instead of :2f to avoid decimal places if unnecessary
                    self.ax.annotate(f"{round(z, 3)} m", xy=(x, y + 5), color='black', annotation_clip=False)

            self.fig.canvas.draw()

        def onclick(event):
            
            self.x.append(event.xdata)
            self.y.append(event.ydata)
            self.z.append(self.z[-1] if self.z else 0)

            update_plot()

        def onpress(event):
            
            if not self.z:
                return

            # Undo last point
            if event.key == 'z':
                self.x.pop()
                self.y.pop()
                self.z.pop()
                
            # Clear all the points
            elif event.key == 'x':
                del self.x[:]
                del self.y[:]
                del self.z[:]

            # Connect the first and last points
            elif event.key == 'c':
                self.x.append(self.x[0])
                self.y.append(self.y[0])
                self.z.append(self.z[0])

            else:
                pass

            update_plot()

        def onscroll(event):

            if not self.z:
                return

            if event.button == 'up':
                self.z[-1] += self.scroll_sensitivity

            elif event.button == 'down':
                self.z[-1] -= self.scroll_sensitivity

            update_plot()

        self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.fig.canvas.mpl_connect('key_press_event', onpress)

        if self.use_z:
            self.fig.canvas.mpl_connect('scroll_event', onscroll)

        return self.x, self.y, self.z