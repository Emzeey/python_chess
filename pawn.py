class Pawn:
    short_name = "  "
    moved = False

    def __init__(self, name=None, color=None):
        if name is not None:
            self.short_name = name[:2]
        self.name = name
        self.color = color

        if color is None:
            self.color_text = "\033[0m"
        elif color == "Black":
            self.color_text = "\033[90m"
        elif color == "White":
            self.color_text = "\033[37m"

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.set_short_name(name)

    def get_short_name(self):
        return self.short_name

    def set_short_name(self, name):
        self.short_name = name[:2]

    def set_moved(self, moved):
        self.moved = moved

    def get_moved(self):
        return self.moved
