import sweeperlib
import random
import math

WIN_WIDTH = 1280
WIN_HEIGHT = 720
GRAVITY = 0.1
GRAVITATION_ACCEL = 1.5

menu = sweeperlib.load_background_image("sprites", "background_0.jpg")
map_1 = sweeperlib.load_background_image("sprites", "background_1.png")

game = {
    "start_x": 120,
    "start_y": 220,
    "x": 120,
    "y": 220,
    "angle": 0,
    "force": 0,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,        # Tells if duck is flying
    "dragging": False,      # Tells if user is dragging the duck
    "ducks": 3,     # Remaining amount of ducks
    "menu": 0,      # 0 = mainmenu,  1 = map1,  2 = map2,  3 = random,  4 = choose maps,  5 = score
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

def drag_duck(x, y, dy, dx, MOUSE_LEFT, modifiers):
    for i in range(1,4):
        if game["menu"] == i:
            if abs(x - game["x"] - 10) < 15 and abs(y - game["y"] - 10) < 15:
                game["x"] = x - 10
                game["y"] = y - 10
                x_difference = game["start_x"] - game["x"] + 10
                y_difference = game["start_y"] - game["y"] + 20
                game["force"] = math.sqrt((x_difference)**2 + (y_difference)**2) / 4
                game["angle"] = math.atan2(y_difference, x_difference)
                game["dragging"] = True


def mouse_handler(x, y, MOUSE_LEFT, modifiers):
    if game["menu"] == 0: # Checks to see if in main menu

        if 470 < x < 820 and 410 < y < 560: # If press on Choose Map
            sweeperlib.clear_window()
            game["menu"] = 4

        if 470 < x < 820 and 255 < y < 405: # If press on Score
            sweeperlib.clear_window()
            game["menu"] = 5

        if 470 < x < 820 and 95 < y < 245: # If press on quit
            sweeperlib.close() # Quits the game


    elif game["menu"] == 4: # Checks to see if in choose map menu
        if 510 < x < 770 and 450 < y < 560: # If press on Map 1
            sweeperlib.clear_window()
            game["menu"] = 1

        if 510 < x < 770 and 330 < y < 440: # If press on Map 2
            sweeperlib.clear_window()
            game["menu"] = 2

        if 510 < x < 770 and 210 < y < 320: # If press on Random Map
            sweeperlib.clear_window()
            game["menu"] = 3

        if 510 < x < 770 and 90 < y < 200: # If press on back
            sweeperlib.clear_window()
            game["menu"] = 0
    


    if game["menu"] == 5: # Checks to see if in score menu
        pass

    else:   # every other case, in a map
        pass


def release_duck(x, y, MOUSE_LEFT, modifiers):
        if game["dragging"]:
            launch()
            game["dragging"] = False


# endregion
   

    

def draw():
    """
    This function handles interface's and objects drawing.
    """
    if game["menu"] == 0:       # Displays main menu
        sweeperlib.clear_window()
        sweeperlib.draw_background()
        prepare_mainmenu()
        sweeperlib.draw_sprites()
    
    elif game["menu"] == 4:     # Displays Choose Map Menu
        sweeperlib.draw_background()
        prepare_choosemaps()
        sweeperlib.draw_sprites()
    
    elif game["menu"] == 5:     # Displays Score menu
        sweeperlib.draw_background()
        prepare_choosemaps()
        sweeperlib.draw_sprites()
    
    else:       # Displays one of the maps
        sweeperlib.clear_window()
        sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_1)
        sweeperlib.draw_background()
        sweeperlib.prepare_sprite("sling", 100, 115)
        sweeperlib.prepare_sprite("duck", game["x"], game["y"])
        sweeperlib.draw_sprites()
        sweeperlib.draw_text("Aim: {}°".format(round(math.degrees(game["angle"]))), 10, 600)
        sweeperlib.draw_text("Powah!: {}".format(round(game["force"])), 10, 660)

def prepare_mainmenu():
    sweeperlib.prepare_sprite("choose_map", 470, 410)
    sweeperlib.prepare_sprite("score", 470, 255)
    sweeperlib.prepare_sprite("quit", 470, 95)

def prepare_choosemaps():
    sweeperlib.prepare_sprite("map_1", 510, 450)
    sweeperlib.prepare_sprite("map_2", 510, 330)
    sweeperlib.prepare_sprite("random_map", 510, 210)
    sweeperlib.prepare_sprite("back", 510, 90)


def main():
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = menu)
    sweeperlib.set_draw_handler(draw)
    sweeperlib.set_interval_handler(flight)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_drag_handler(drag_duck)
    sweeperlib.set_release_handler(release_duck)
    sweeperlib.start()


if __name__ == "__main__":
    main()
