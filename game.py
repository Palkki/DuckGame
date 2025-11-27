import sweeperlib
import random
import math
import time
from sweeperlib import KEYS

WIN_WIDTH = 1280
WIN_HEIGHT = 720
GRAVITY = 20
GRAVITATION_ACCEL = 1.5     # y_velocity modifier
BOUNCE_MODIFIER = 0.4       # Higher number == higher bounce.
X_LAUNCH_VEL = 1
Y_LAUNCH_VEL = 1.25



# region Backgrounds
main_menu_bg = sweeperlib.load_background_image("sprites", "background_0.jpg")
map_1_bg = sweeperlib.load_background_image("sprites", "background_1.png")
map_2_bg = sweeperlib.load_background_image("sprites", "background_2.png")
map_3_bg = sweeperlib.load_background_image("sprites", "background_3.png")
# endregion

# region Dictionaries for game data
map_status = {
    "targets": [],
    "falling_targets": [],
    "fallen_targets": [],
    "ducks": 5,
    "sling_x": 220,
    "sling_y": 90,     
    "ceiling": 340,
    "floor": 35,
    "l_wall": 0,
    "r_wall": 330,  
    "menu": 0,     # 0 = mainmenu,  1 = map1,  2 = map2,  3 = map3, 4 = random, 5 = loser, 6 = winner
    "bg": main_menu_bg,

}
duck = {
    "start_x": map_status["sling_x"] + 22,
    "start_y": map_status["sling_y"] + 110,
    "x": map_status["sling_x"] + 22,
    "y": map_status["sling_y"] + 110,
    "angle": 0,
    "force": 0,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,        # Tells if duck is flying
    "dragging": False,      # Tells if user is dragging the duck
    "collision": False
    
}
#endregion

# region Duck
def initial_state():
    """
    Puts the duck back into the sling and stop its movement. Reset force and angle.
    Also tells the game that the duck isn't flying anymore.
    """
    duck["x"] = map_status["sling_x"] + 22
    duck["y"] = map_status["sling_y"] + 110
    duck["angle"] = 0
    duck["force"] = 0
    duck["x_velocity"] = 0
    duck["y_velocity"] = 0
    duck["flight"] = False
    duck["collision"] = False
    print("Fallen: ", map_status["fallen_targets"])
    print("Targets left: ", len(map_status["targets"]), "\n")

def initial_map_state():
    map_status["targets"] = []
    map_status["falling_targets"] = []
    map_status["fallen_targets"] = []
    map_status["ducks"] = 5

def launch():
    """
    Launches a duck and calculates its starting velocity. Stores x and y velocity
    components to the game dictionary.
    """
    duck["x_velocity"] = X_LAUNCH_VEL * (duck["force"] * math.cos((duck["angle"])))
    duck["y_velocity"] = Y_LAUNCH_VEL * (duck["force"] * math.sin((duck["angle"])))
    duck["flight"] = True

def flight(elapsed):
    """
    Updates duck's x and y coordinates based on corresponding velocity vectors.
    If the duck hits the ground or another object it reacts to it here
    """
    drop(map_status["targets"])

    for i in range(1,5):
        if map_status["menu"] == i:
            if len(map_status["targets"]) == 0 and len(map_status["falling_targets"]) == 0:
                print("yay")
                try:
                    initial_map_state()
                    get_map(map_status["next_map"])
                except FileNotFoundError:
                    map_status["menu"] = 6  
                except KeyError:
                    initial_map_state()
                    prepare_random() 
                    draw_random()        
    if map_status["ducks"] <= 0 and len(map_status["falling_targets"]) == 0:
        time.sleep(0.5)
        map_status["menu"] = 5                   

    if duck["flight"]:
        duck["x"] += duck["x_velocity"]
        duck["y"] += duck["y_velocity"]
        duck["y_velocity"] -= GRAVITATION_ACCEL
        if duck["y"] < 40:
            duck["y"] = 40
            duck["x_velocity"] /= 1.8
            duck["y_velocity"] = -BOUNCE_MODIFIER * duck["y_velocity"]
            if duck["x_velocity"] + duck["y_velocity"] < 4 and map_status["ducks"] > 0:
                time.sleep(1/4)
                initial_state()
                map_status["ducks"] -= 1
        if duck["x"] > 1400 or duck["x"] < -100 and map_status["ducks"] > 0:
            initial_state()
            map_status["ducks"] -= 1

def calculate_distance(x_start, y_start, x_end, y_end):
    """
    Calculates the distance between two points and returns it.
    """
    return math.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)

def check_collision(object_1, object_2):
    """
    Calculates the distance between two objects and returns True if the objects hit
    each other, False if they do not.
    """
    distance = calculate_distance(object_1["x"], object_1["y"], object_2["x"], object_2["y"])
    if  distance <= 60:
        return True
    return False

def drop(targets):
    """
    Drops targets that are given as a list. Each object is to be
    defined as a dictionary with x and y coordinates, width, height, and falling
    velocity. Drops boxes for one time unit.  
    """
    
    for target in targets:
        if check_collision(duck, target):
            print("Osui")    
            initial_state()
            map_status["ducks"] -= 1
            target["vy"] += GRAVITY
            map_status["falling_targets"].append(target)
            map_status["targets"].remove(target)

    for falling_target in map_status["falling_targets"]:
        falling_target["y"] -= falling_target["vy"]
        for fallen_target in map_status["fallen_targets"]:
            if not (falling_target["x"] < fallen_target["x"] + 60 and fallen_target["x"] < falling_target["x"] + 60):
                continue
            fallen_target_top = fallen_target["y"] + 60
            if falling_target["y"] < fallen_target_top:
                falling_target["y"] = fallen_target_top
                falling_target["vy"] = 0
                duck["collision"] = True
                break
        if falling_target["y"] <= 40:
            falling_target["y"] = 40
            falling_target["vy"] = 0
        if falling_target not in map_status["fallen_targets"] and falling_target["vy"] == 0:
                map_status["fallen_targets"].append(falling_target)   
                map_status["falling_targets"].remove(falling_target)   
        
                

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
    for i in range(1,5):
        if map_status["menu"] == i and not duck["flight"]:
            if abs(x - duck["x"]) < 60 and abs(y - duck["y"]) < 60:
                if (map_status["l_wall"] < x < map_status["r_wall"]) and (map_status["floor"] < y < map_status["ceiling"]): 
                    duck["x"] = x - 10
                    duck["y"] = y - 10
                    x_difference = duck["start_x"] - duck["x"]
                    y_difference = duck["start_y"] - duck["y"]
                    duck["force"] = math.sqrt((x_difference)**2 + (y_difference)**2) / 5.2
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

        if 515 < x < 788 and 277 < y < 327: # If press on Play Campaign
            get_map("map_1.txt")
            map_status["menu"] = 1
            map_status["bg"] = map_1_bg

        if 528 < x < 766 and 210 < y < 260: # If press on Random map
            prepare_random()
            map_status["menu"] = 4
            map_status["bg"] = map_3_bg
            

        if 587 < x < 695 and 145 < y < 193: # If press on quit
            sweeperlib.close() # Quits the game

    if map_status["menu"] == 5: # Checks to see if loser menu
        if 525 < x < 754 and 148 < y < 202: # If press on main menu
            initial_state()
            initial_map_state()
            sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = main_menu_bg)
            sweeperlib.clear_window()
            map_status["menu"] = 0
            map_status["bg"] = main_menu_bg
            map_status.pop("next_map")
        if 525 < x < 754 and 225 < y < 280: # If press on try again
            try:
                if map_status["next_map"] == "map_2.txt":
                    initial_map_state()
                    map_status["menu"] = 1
                    get_map("map_1.txt")
                elif map_status["next_map"] == "map_3.txt":
                    initial_map_state()
                    map_status["menu"] = 2
                    get_map("map_2.txt")
                elif map_status["next_map"] == "None":
                    initial_map_state()
                    map_status["menu"] = 3
                    get_map("map_3.txt")
            except KeyError:
                map_status["menu"] = 4
                initial_map_state()
                prepare_random()
            
    
    if map_status["menu"] == 6: # Checks to see if winner menu
        if 502 < x < 773 and 120 < y < 186: # If press on main menu
            initial_state()
            sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = main_menu_bg)
            sweeperlib.clear_window()
            map_status["menu"] = 0
            map_status["bg"] = main_menu_bg
            map_status.pop("next_map")
        if 502 < x < 773 and 206 < y < 275: # If press on try again
            map_status["menu"] = 1
            get_map("map_1.txt")
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

def keyboard_handler(sym, mod):
    key = sweeperlib.pyglet.window.key
    for i in range(1,7):
        if map_status["menu"] == i:
            if sym == key.ESCAPE:
                sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = main_menu_bg)
                sweeperlib.clear_window()
                map_status["menu"] = 0
                map_status["bg"] = main_menu_bg
                initial_state()
                initial_map_state()
                map_status.pop("next_map")

# endregion

# region Map thingies
def get_map(filename):
    """
    Gets the wanted map data (target pos, object pos, duck amount) and stores it in map_status
    """
    with open(filename, encoding="UTF-8") as source:
        lista = source.read().split("\n")
        map_status["targets"] = []
        map_status["objects"] = []
        targets = lista[0].split(":")
        objects = lista[1].split(":")
        for target in targets:
            target_x, target_y, vy = target.split(",")
            map_status["targets"].append({
                "x": int(target_x),
                "y": int(target_y),
                "vy": int(vy)
            })
        for object in objects:
            object_x, object_y = object.split(",")
            map_status["objects"].append({
                "x": int(object_x),
                "y": int(object_y)
            })
        status_keys = ["ducks", "sling_x", "sling_y", "ceiling", "floor", "l_wall", "r_wall", "next_map"]
        for i, key in enumerate(status_keys):
            if key == "next_map":
                map_status[key] = lista[i+2]
            else:
                map_status[key] = int(lista[i+2])

        duck["start_x"] = map_status["sling_x"] + 22
        duck["start_y"] = map_status["sling_y"] + 110
        initial_state()



def prepare_random():
    target_amount = random.randint(3, 6)
    map_status["ducks"] = target_amount + 2
    map_status["targets"] = create_targets(target_amount, 150)


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
    for i in range(targets):
            new_target = {
                        "x": random.randint(500, 1160),
                        "y": random.randint(min_y, 500),
                        "w": 60,
                        "h": 60,
                        "vy": 0
                        }
            for target in targetlist:
                while check_collision(target, new_target):
                    print("Collision")
                    new_target = {
                        "x": random.randint(500, 1160),
                        "y": random.randint(min_y, 500),
                        "w": 60,
                        "h": 60,
                        "vy": 0
                        }
            targetlist.append(new_target)
                    
    return targetlist

#endregion

# region grafik draw
def draw():
    """
    This function handles interface's and objects drawing.
    """
    if map_status["menu"] == 0:       # Displays main menu
        draw_mainmenu()
    elif map_status["menu"] == 4:     # Displays a random map
        draw_random()
    elif map_status["menu"] == 5:      # Displays loser screen
        draw_loser()
    elif map_status["menu"] == 6:      # Displays loser screen
        draw_winner()
    else:                             # Displays one of the maps
        draw_map()

def draw_mainmenu():
    """
    Changes to mainmenu view
    """
    sweeperlib.clear_window()
    sweeperlib.draw_sprites()
    initial_state()
    map_status["ducks"] = 3

def draw_loser():
    """
    Changes to choose maps view
    """
    sweeperlib.prepare_sprite("blur", 0, 0)
    sweeperlib.prepare_sprite("loser", 0, 0)
    sweeperlib.draw_sprites()

def draw_winner():
    """
    Changes to choose maps view
    """
    sweeperlib.prepare_sprite("blur", 0, 0)
    sweeperlib.prepare_sprite("winner", 0, 0)
    sweeperlib.draw_sprites()

def draw_random():
    for target in map_status["targets"]:
        sweeperlib.prepare_sprite("target", target["x"], target["y"])
    for fallen_target in map_status["fallen_targets"]:
        sweeperlib.prepare_sprite("target", int(fallen_target["x"]), int(fallen_target["y"]))
    for falling_target in map_status["falling_targets"]:
        sweeperlib.prepare_sprite("target", int(falling_target["x"]), int(falling_target["y"]))
    sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_status["bg"])
    sweeperlib.prepare_sprite("sling", map_status["sling_x"], map_status["sling_y"])
    sweeperlib.prepare_sprite("duck", duck["x"], duck["y"])
    sweeperlib.draw_sprites()
    sweeperlib.draw_text("Aim: {}°".format(round(math.degrees(duck["angle"]))), 10, 600)
    sweeperlib.draw_text("Powah!: {}".format(round(duck["force"])), 10, 660)
    sweeperlib.draw_text("Ducks: {}".format(map_status["ducks"]), 10, 540)

def draw_map():
    """
    Changes to map view
    """
    sweeperlib.clear_window()
    for target in map_status["targets"]:
        sweeperlib.prepare_sprite("target", int(target["x"]), int(target["y"]))
    for fallen_target in map_status["fallen_targets"]:
        sweeperlib.prepare_sprite("target", int(fallen_target["x"]), int(fallen_target["y"]))
    for falling_target in map_status["falling_targets"]:
        sweeperlib.prepare_sprite("target", int(falling_target["x"]), int(falling_target["y"]))
    sweeperlib.resize_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_status["bg"])
    sweeperlib.prepare_sprite("sling", map_status["sling_x"], map_status["sling_y"])
    sweeperlib.prepare_sprite("duck", duck["x"], duck["y"])
    sweeperlib.draw_sprites()
    sweeperlib.draw_text("Aim: {}°".format(round(math.degrees(duck["angle"]))), 10, 600)
    sweeperlib.draw_text("Powah!: {}".format(round(duck["force"])), 10, 660)
    sweeperlib.draw_text("Ducks: {}".format(map_status["ducks"]), 10, 540)



#endregion

def main():
    """
    Loads all assets, creates window and sets all the handlers. 
    Starts the program
    """
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT, bg_image = map_status["bg"])
    sweeperlib.set_draw_handler(draw)
    sweeperlib.set_interval_handler(flight)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_drag_handler(drag_duck)
    sweeperlib.set_release_handler(release_duck)
    sweeperlib.set_keyboard_handler(keyboard_handler)
    sweeperlib.start()


if __name__ == "__main__":
    main()
