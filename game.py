import sweeperlib
import random
import math

WIN_WIDTH = 1200
WIN_HEIGHT = 600
GRAVITY = 0.1

game = {
    "x": 100,
    "y": 120,
    "angle": 0,
    "force": 0,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,
    "ducks": 3,
    "boxes": []
}

# region Duck
def initial_state():
        """
        Puts the game back into its initial state: the duck is put back into the
        launch position, its speed to zero, and its flight state to False.
        """
        game["x"] = 40
        game["y"] = 40
        game["x_velocity"] = 0
        game["y_velocity"] = 0
        game["flight"] = False


def launch():
        """
        Launches a duck and calculates its starting velocity. Stores x and y velocity
        components to the game dictionary.
        """
        game["x_velocity"] = game["force"] * math.cos(math.radians(game["angle"]))
        game["y_velocity"] = game["force"] * math.sin(math.radians(game["angle"]))
        game["flight"] = True

def flight(elapsed):
    """
    Updates duck's x and y coordinates based on corresponding velocity vectors.
    """
    if game["flight"]:
        game["x"] += game["x_velocity"]
        game["y"] += game["y_velocity"]
        game["y_velocity"] -= GRAVITATIONAL_ACCEL
        if game["y"] <= 0:
            initial_state()

# endregion

# region Inputs
    def keypress(sym, mods):
        """
        This function handles keyboard input.
        You do NOT need to modify this.
        """
        key = sweeperlib.pyglet.window.key

        if sym == key.Q:
            sweeperlib.close()

        if sym == key.R:
            initial_state()

        if sym == key.RIGHT:
            game["angle"] -= 10
            if game["angle"] < 0:
                game["angle"] = 350
        elif sym == key.LEFT:
            game["angle"] += 10
            if game["angle"] > 350:
                game["angle"] = 0

        if sym == key.UP:
            if game["force"] < 50:
                game["force"] += 5
        elif sym == key.DOWN:
            if game["force"] >= 5:
                game["force"] -= 5
            else:
                game["force"] = 0

        if sym == key.SPACE:
            launch()


# endregion


def draw():
    """
    This function handles interface's and objects drawing.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    sweeperlib.prepare_sprite("sling", 80, 20)
    sweeperlib.prepare_sprite("duck", game["x"], game["y"])
    sweeperlib.draw_sprites()
    sweeperlib.draw_text("{}°\tforce: {}".format(game["angle"], game["force"]), 10, 505)
    sweeperlib.draw_text(
        "Q: Quit  | "
        "R: Reset |  "
        "←/→: Set angle |  "
        "↑/↓: Set Force  |  "
        "Space: Launch",
        10, 560,
        size=20)




def main():
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT)
    sweeperlib.set_draw_handler(draw)
    sweeperlib.set_keyboard_handler(keypress)
    sweeperlib.set_interval_handler(flight)
    sweeperlib.start()


if __name__ == "__main__":
    main()
