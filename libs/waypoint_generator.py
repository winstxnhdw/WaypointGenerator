class WaypointGenerator:

    def __init__(self, ax, fig, map_size, line_colour, point_colour):

        self.ax = ax
        self.fig = fig
        self.map_size = map_size
        self.line_colour = line_colour
        self.point_colour = point_colour

        self.x = []
        self.y = []