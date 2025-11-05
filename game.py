import sweeperlib
import random
import math
import time

WIN_WIDTH = 1280
WIN_HEIGHT = 720
GRAVITATION_ACCEL = 1.5     # y_velocity modifier
BOUNCE_MODIFIER = 0.4       # Higher number == higher bounce.

sling_x = 300
sling_y = 115       

# region Backgrounds
main_menu_bg = sweeperlib.load_background_image("sprites", "background_0.jpg")
map_1_bg = sweeperlib.load_background_image("sprites", "background_1.png")
map_2_bg = sweeperlib.load_background_image("sprites", "background_1.png")
map_3_bg = sweeperlib.load_background_image("sprites", "background_1.png")
# endregion

# region Dictionaries for game data
map_status = {
    "targets": [],
    "objects": [],
    "ducks": 3,
    "menu": 0,     # 0 = mainmenu,  1 = map1,  2 = map2,  3 = random,  4 = choose maps
    "bg": main_menu_bg

}
duck = {
    "start_x": sling_x + 22,
    "start_y": sling_y + 110,
    "x": sling_x + 22,
    "y": sling_y + 110,
    "angle": 0,
    "force": 0,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,        # Tells if duck is flying
    "dragging": False,      # Tells if user is dragging the duck
    
}
#endregion

# region Duck
def initial_state():
    """
    Puts the duck back into the sling and stop its movement. Reset force and angle.
    Also tells the game that the duck isn't flying anymore.
    """
    duck["x"] = sling_x + 22
    duck["y"] = sling_y + 110
    duck["angle"] = 0
    duck["force"] = 0
    duck["x_velocity"] = 0
    duck["y_velocity"] = 0
    duck["flight"] = False


def launch():
    """
    Launches a duck and calculates its starting velocity. Stores x and y velocity
    components to the game dictionary.
    """
    duck["x_velocity"] = duck["force"] * math.cos((duck["angle"]))
    duck["y_velocity"] = duck["force"] * math.sin((duck["angle"]))
    duck["flight"] = True

def flight(elapsed):
    """
    Updates duck's x and y coordinates based on corresponding velocity vectors.
    If the duck hits the ground or another object it reacts to it here
    """
    if duck["flight"]:
        duck["x"] += duck["x_velocity"]
        duck["y"] += duck["y_velocity"]
        duck["y_velocity"] -= GRAVITATION_ACCEL
        if duck["y"] < 100:
            duck["y"] = 100
            duck["x_velocity"] /= 1.8
            duck["y_velocity"] = -BOUNCE_MODIFIER * duck["y_velocity"]
            if duck["x_velocity"] + duck["y_velocity"] < 4:
                time.sleep(1/4)
                initial_state()
        #if duck hits target:
        #   duck explode? Fall down? idk
        #if duck hits object:
        #   Bounce away?

    #for target in targets:
    #   Check if collision with duck:
    #       drop the box
# endregion

# region Inputs

def drag_duck(x, y, dy, dx, MOUSE_LEFT, modifiers):
    """
    This function oversees where the user is dragging the mouse and when it can drag. 
    The game's only drag function is to drag the chicken so dragging only does stuff when user is
    in a map. It's also only allowed when the bird isn't flying. (Please don't disturb birds in the air)
    Basically here the game calculates how fast to send the bird flying based on
    how far it is from its starting point (the sling)

    """
    for i in range(1,4):
        if map_status["menu"] == i and not duck["flight"]:
            if abs(x - duck["x"]) < 25 and abs(y - duck["y"]) < 25:
                duck["x"] = x - 10
                duck["y"] = y - 10
                x_difference = duck["start_x"] - duck["x"]
                y_difference = duck["start_y"] - duck["y"]
                duck["force"] = math.sqrt((x_difference)**2 + (y_difference)**2) / 4
                duck["angle"] = math.atan2(y_difference, x_difference)
                duck["dragging"] = True


def mouse_handler(x, y, MOUSE_LEFT, modifiers):
    """
    This function's only job is to click menus etc.
    It checks where the user is currently (main menu, map1, map2...) and lets the user click
    on boxes and text only related to that page.
    The function also updates the map_status dictionary so that the game knows where the user actually
    is at all times.
    """
    if map_status["menu"] == 0: # Checks to see if in main menu

        if 470 < x < 820 and 410 < y < 560: # If press on Choose Map
            map_status["menu"] = 4

        if 470 < x < 820 and 95 < y < 245: # If press on quit
            sweeperlib.close() # Quits the game

    elif map_status["menu"] == 4: # Checks to see if in choose map menu
        if 510 < x < 770 and 450 < y < 560: # If press on Map 1
            map_status["menu"] = 1
            map_status["bg"] = map_1_bg
            get_map("map_1.txt")
            

        if 510 < x < 770 and 330 < y < 440: # If press on Map 2
            map_status["menu"] = 2
            map_status["bg"] = map_2_bg
            get_map("map_2.txt")
            

        if 510 < x < 770 and 210 < y < 320: # If press on Random Map
            map_status["menu"] = 3
            map_status["bg"] = map_3_bg

        if 510 < x < 770 and 90 < y < 200: # If press on back
            map_status["menu"] = 0
            map_status["bg"] = main_menu_bg
    
    else:   # every other case, in a map
        pass


def release_duck(x, y, MOUSE_LEFT, modifiers):
        """
        When the user releases the dragging of the duck, it goes flying in the air. 
        Also sets the angle and force to their respective initial states.
        """
        if duck["dragging"]:
            launch()
            duck["dragging"] = False
            duck["angle"] = 0
            duck["force"] = 0


# endregion

# region Map thingies
def get_map(filename):
    """
    Gets the wanted map data (target pos, object pos, duck amount) and stores it in map_status
    """
    with open(filename, encoding="UTF-8") as source:
        lista = source.read().split("\n")
        map_status["targets"] = lista[0].split(":")
        map_status["objects"] = lista[1].split(":")
        map_status["ducks"] = lista[2]
    
def create_targets(targets, min_y):
    """
    Creates a speficied number of targets with random positions inside the specified
    area, used for the random map mode. 
    Targets are represented as dictionaries with the following keys:
    x: x coordinate of the bottom left corner
    y: y coordinate of the bottom left corner
    w: target width
    h: target height
    vy: falling velocity of the box
    """
    targetlist = []
    for target in range(targets):
        targetlist.append({
            "x": random.randint(0, 1160),
            "y": random.randint(min_y, 560),
            "w": 40,
            "h": 40,
            "vy": 0
        })
    return target

#endregion

# region grafik draw
def draw():
    """
    This function handles interface's and objects drawing.
    """
    if map_status["menu"] == 0:       # Displays main menu
        prepare_mainmenu()

    elif map_status["menu"] == 4:     # Displays Choose Map Menu
        prepare_choosemaps()
    
    else:       # Displays one of the maps
        prepare_map()

def prepare_mainmenu():
    sweeperlib.clear_window()
    sweeperlib.prepare_sprite("choose_map", 470, 340)
    sweeperlib.prepare_sprite("quit", 470, 165)
    sweeperlib.draw_sprites()

def prepare_choosemaps():
    sweeperlib.clear_window()
    sweeperlib.prepare_sprite("map_1", 510, 450)
    sweeperlib.prepare_sprite("map_2", 510, 330)
    sweeperlib.prepare_sprite("random_map", 510, 210)
    sweeperlib.prepare_sprite("back", 510, 90)
    sweeperlib.draw_sprites()

def prepare_map():
    sweeperlib.clear_window()
    sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_status["bg"])
    sweeperlib.prepare_sprite("sling", sling_x, sling_y)
    sweeperlib.prepare_sprite("duck", duck["x"], duck["y"])
    sweeperlib.draw_sprites()
    sweeperlib.draw_text("Aim: {}°".format(round(math.degrees(duck["angle"]))), 10, 600)
    sweeperlib.draw_text("Powah!: {}".format(round(duck["force"])), 10, 660)

#endregion

def main():
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_status["bg"])
    sweeperlib.set_draw_handler(draw)
    sweeperlib.set_interval_handler(flight)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_drag_handler(drag_duck)
    sweeperlib.set_release_handler(release_duck)
    sweeperlib.start()


if __name__ == "__main__":
    main()
