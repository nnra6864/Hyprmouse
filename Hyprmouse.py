import setproctitle, subprocess, cairo, os, re, gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib


"""
UTILS
"""


def hex_to_rgb(hex_string):
    return tuple(int(hex_string[i:i+2], 16) / 255 for i in (1, 3, 5))


def get_screen_res():
    output = subprocess.check_output(["hyprctl", "monitors", "all"]).decode("utf-8")
    wh = re.search(r"\d+x\d+", output).group()
    return map(int, wh.split('x'))


"""
FUNCTIONS
"""


def load_config():
    global config
    cfg_path = os.path.expanduser("~/.config/hypr/hyprmouse.conf")
    try:
        with open(cfg_path, 'r') as cfg:
            for line in cfg:
                key, value = line.strip().split('=')
                key = key.strip()
                value = value.strip()
                if key in config:
                    if value == "True":
                        config[key] = True
                    elif value == "False":
                        config[key] = False
                    elif value.isdigit():
                        config[key] = int(value)
                    else:
                        config[key] = value
    except FileNotFoundError:
        print("Config file not found.")
    except Exception as e:
        print("An error occurred while loading the config file:", e)


def draw_grid(window, cr):
    global config, width, height
    cr.set_source_rgb(*hex_to_rgb(config["grid_color"]))
    cr.set_line_width(config["grid_thickness"])

    for x in range((width // 2) % config["spacing"], width, config["spacing"]):
        cr.move_to(x, 0)
        cr.line_to(x, height)
        cr.stroke()

    for y in range((height // 2) % config["spacing"], height, config["spacing"]):
        cr.move_to(0, y)
        cr.line_to(width, y)
        cr.stroke()

    #Try to remove this func from the draw call later if I figure out a way to not erase the grid whilst doing it :/


def draw_numbers(window, cr):
    global config, width, height, posX, posY
    font = Gtk.Settings.get_default().get_property("gtk-font-name").rsplit(maxsplit=1)[0] #Don't ask o_0
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(20)



def update(window):
    window.queue_draw()
    return True


def on_key_press(window, event):
    if event.keyval == Gdk.KEY_Delete:
        Gtk.main_quit()


def draw_window():
    global config
    window = Gtk.Window()
    window.set_title("Hyprmouse")
    window.set_size_request(width, height)
    window.resize(1, 1) #No clue why this is needed but it triggers the window resize so whatever :/
    window.set_app_paintable(True) #Needed for transparency ig

    GtkLayerShell.init_for_window(window)
    GtkLayerShell.set_namespace(window, "Hyprmouse") #Needed so you can apply layer styles via hyprland.conf to Hyprmouse
    GtkLayerShell.set_layer(window, GtkLayerShell.Layer.OVERLAY)
    GtkLayerShell.set_keyboard_mode(window, GtkLayerShell.KeyboardMode.EXCLUSIVE) #Overlay now blocks the kb input

    if config["show_ui"]:
        if config["show_grid"]: window.connect("draw", draw_grid)
        if config["show_numbers"]: window.connect("draw", draw_numbers)
    window.connect("key-press-event", on_key_press)

    GLib.timeout_add(100, lambda: update(window))
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


"""
PROGRAM
"""

font_params = Gtk.Settings.get_default().get_property("gtk-font-name").split()
config = {
    "show_ui": True,
    "show_grid": True,
    "show_dots": True,
    "show_numbers": True,
    "format": "x, y",
    "font": " ".join(font_params[:-1]),
    "font_size": int(font_params[-1]),
    "grid_color": "#ECEFF4",
    "dot_color": "#FFFFFF",
    "text_color": "#ECEFF4",
    "text_outline_color": "#2E3440",
    "grid_thickness": 0.5,
    "spacing": 200
}


startPosX, startPosY = map(int, subprocess.check_output(["hyprctl", "cursorpos"]).decode("utf-8").split(','))
posX = startPosX
posY = startPosY
setproctitle.setproctitle("Hyprmouse")
load_config()
width, height = get_screen_res() #Setting values once on launch
draw_window()
