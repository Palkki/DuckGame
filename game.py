import sweeperlib
import random
import math

WIN_WIDTH = 1280
WIN_HEIGHT = 720
GRAVITY = 0.1
GRAVITATION_ACCEL = 1.5

bg_1 = sweeperlib.load_background_image("sprites", "background.png")

game = {
    "start_x": 120,
    "start_y": 220,
    "x": 120,
    "y": 220,
    "angle": 0,
    "force": 0,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,
    "dragging": False,
    "ducks": 3,
    "boxes": []
}

# region Duck
def initial_state():
    """
    Puts the game back into its initial state: the duck is put back into the
    launch position, its speed to zero, and its flight state to False.
    """
    game["x"] = 120
    game["y"] = 220
    game["angle"]: 0
    game["force"]: 0
    game["x_velocity"] = 0
    game["y_velocity"] = 0
    game["flight"] = False


def launch():
    """
    Launches a duck and calculates its starting velocity. Stores x and y velocity
    components to the game dictionary.
    """
    game["x_velocity"] = game["force"] * math.cos((game["angle"]))
    game["y_velocity"] = game["force"] * math.sin((game["angle"]))
    game["flight"] = True

def flight(elapsed):
    """
    Updates duck's x and y coordinates based on corresponding velocity vectors.
    """
    if game["flight"]:
        game["x"] += game["x_velocity"]
        game["y"] += game["y_velocity"]
        game["y_velocity"] -= GRAVITATION_ACCEL
        if game["y"] <= 0:
            initial_state()

# endregion

# region Inputs
def keypress(sym, mods):
    """
    This function handles keyboard inputs.
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

def mouse_handler(x, y, button, modifiers):
    pass


def drag_duck(x, y, dy, dx, MOUSE_LEFT, modifiers):
    if abs(x - game["x"] - 10) < 15 and abs(y - game["y"] - 10) < 15:
        game["x"] = x - 10
        game["y"] = y - 10
        x_difference = game["start_x"] - game["x"] + 30
        y_difference = game["start_y"] - game["y"] + 80
        game["force"] = math.sqrt((x_difference)**2 + (y_difference)**2) / 5
        game["angle"] = math.atan2(y_difference, x_difference)
        game["dragging"] = True


def release_duck(x, y, MOUSE_LEFT, modifiers):
        if game["dragging"]:
            launch()
            game["dragging"] = False


# endregion
   

    

def draw():
    """
    This function handles interface's and objects drawing.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    sweeperlib.prepare_sprite("sling", 100, 115)
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
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = bg_1)
    sweeperlib.set_draw_handler(draw)
    sweeperlib.set_keyboard_handler(keypress)
    sweeperlib.set_interval_handler(flight)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_drag_handler(drag_duck)
    sweeperlib.set_release_handler(release_duck)
    sweeperlib.start()


if __name__ == "__main__":
    main()
