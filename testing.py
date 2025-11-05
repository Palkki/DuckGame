import sweeperlib
WIN_WIDTH = 1200
WIN_HEIGHT = 600

map_status = {
    "targets": [],
    "objects": [],
    "ducks": 3
}


def get_maps(filename):
    with open(filename, encoding="UTF-8") as source:
        lista = source.read().split("\n")
        map_status["targets"] = lista[0].split(":")
        map_status["objects"] = lista[1].split(":")
        map_status["ducks"] = lista[2]

def draw():
    """
    Draws all boxes into the window.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    for box in game["boxes"]:
        sweeperlib.prepare_sprite(" ", box["x"], box["y"])
    sweeperlib.draw_sprites()


#if __name__ == "__main__":
#    sweeperlib.load_sprites("sprites")
#    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT)
#    sweeperlib.set_draw_handler(draw)
#    sweeperlib.start()

def get_maps(filename):
    with open(filename, encoding="UTF-8") as source:
        lista = source.read().split("\n")
        map_status["targets"] = lista[0].split(":")
        map_status["objects"] = lista[1].split(":")
        map_status["ducks"] = lista[2]


get_maps("map_2.txt")
print(map_status["targets"])
print("---")

for target in map_status["targets"]:
    x,y,w,h,vy = target.split(",")
    print(x,y,w,h,vy)

#x,y,w,h,vy = map_status["targets"][0].split(",")
#print(x,y,w,h,vy)

