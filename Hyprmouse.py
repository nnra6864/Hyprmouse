import setproctitle, subprocess, cairo, os, re, gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib


"""
UTILS
"""


def hex_to_rgb(hex_string):
    return tuple(int(hex_string[i:i+2], 16) / 255 for i in ((1, 3, 5) if hex_string.startswith('#') else (0, 2, 4)))


def get_screen_res():
    output = subprocess.check_output(["hyprctl", "monitors", "all"]).decode("utf-8")
    wh = re.search(r"\d+x\d+", output).group()
    return map(int, wh.split('x'))


def get_mouse_pos():
    return map(int, subprocess.check_output(["hyprctl", "cursorpos"]).decode("utf-8").split(','))



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
                    if value.lower() == "true":
                        config[key] = True
                    elif value.lower() == "false":
                        config[key] = False
                    elif value.lstrip('-').isdigit():
                        config[key] = -int(value.lstrip('-')) if '-' in value else int(value)
                    else:
                        config[key] = value
    except FileNotFoundError:
        print("Config file not found.")
    except Exception as e:
        print("An error occurred while loading the config file:", e)


def draw_background(window, cr):
    cr.set_source_rgba(*hex_to_rgb(config["background_color"]), config["background_opacity"])
    cr.rectangle(0, 0, width, height)
    cr.fill()


def draw_grid(window, cr):
    global config, width, height, posX, posY
    cr.set_source_rgb(*hex_to_rgb(config["grid_color"]))
    cr.set_line_width(config["grid_thickness"])
    spacing = config["spacing"]

    follow_mouse = config["follow_mouse"]
    w =  posX % spacing - spacing if follow_mouse else (width // 2) % spacing
    h =  posY % spacing - spacing if follow_mouse else (height // 2) % spacing
    tw = width + spacing if follow_mouse else width
    th = height + spacing if follow_mouse else height

    for x in range(w, tw, spacing):
        cr.move_to(x, 0)
        cr.line_to(x, height)
        cr.stroke()
    
    for y in range(h, th, spacing):
        cr.move_to(0, y)
        cr.line_to(width, y)
        cr.stroke()


def draw_dots(window, cr):
    global config, width, height, posX, posY
    spacing = config["spacing"]

    follow_mouse = config["follow_mouse"]
    w =  posX % spacing - spacing if follow_mouse else (width // 2) % spacing
    h =  posY % spacing - spacing if follow_mouse else (height // 2) % spacing
    tw = width + spacing if follow_mouse else width
    th = height + spacing if follow_mouse else height
    
    cr.set_source_rgb(*hex_to_rgb(config["dot_color"]))
    rad = config["dot_radius"]
    pi = 2 * 3.14159
    for x in range(w, tw, spacing):
        for y in range(h, th, spacing):
            cr.arc(x, y, rad, 0, pi)
            cr.fill()


def draw_numbers(window, cr):
    global config, width, height, posX, posY
    cr.select_font_face(config["font"], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(config["font_size"])
    spacing = config["spacing"]
    
    follow_mouse = config["follow_mouse"]
    w =  posX % spacing - spacing if follow_mouse else (width // 2) % spacing
    h =  posY % spacing - spacing if follow_mouse else (height // 2) % spacing
    tw = width + spacing if follow_mouse else width
    th = height + spacing if follow_mouse else height

    offset = config["text_outline_thickness"]
    y_offset = config["text_y_offset"]

    for x in range(w, tw, spacing):
        for y in range(h, th, spacing):
            cr.set_source_rgb(*hex_to_rgb(config["text_outline_color"]))
            label = f"{x - posX} {posY - y}"
            xp = x - cr.text_extents(label)[4] // 2
            yp = y + cr.text_extents(label)[3] // 2 - y_offset
            cr.move_to(xp + offset, yp + offset)
            cr.show_text(label)
            cr.move_to(xp - offset, yp + offset)
            cr.show_text(label)
            cr.move_to(xp + offset, yp - offset)
            cr.show_text(label)
            cr.move_to(xp - offset, yp - offset)
            cr.show_text(label)
            
            cr.set_source_rgb(*hex_to_rgb(config["text_color"]))
            cr.move_to(xp, yp)
            cr.show_text(label)


def update(window):
    global posX, posY
    posX, posY = get_mouse_pos()
    window.queue_draw()
    return True


def on_key_press(window, event):
    if event.keyval == Gdk.KEY_Delete:
        Gtk.main_quit()

    if event.keyval == Gdk.KEY_Escape:
        subprocess.run(["ydotool", "mousemove", "-a", f"{startPosX}", f"{startPosY}"])
        Gtk.main_quit()

    if event.keyval == Gdk.KEY_Return:
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
        if config["show_background"]: window.connect("draw", draw_background)
        if config["show_grid"]: window.connect("draw", draw_grid)
        if config["show_dots"]: window.connect("draw", draw_dots)
        if config["show_numbers"]: window.connect("draw", draw_numbers)
    window.connect("key-press-event", on_key_press)

    update_rate = int(1 / config["fps"] * 1000)
    GLib.timeout_add(update_rate, lambda: update(window))
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


"""
PROGRAM
"""

font_params = Gtk.Settings.get_default().get_property("gtk-font-name").split()
config = {
    "show_ui": True,
    "show_background": True,
    "show_grid": True,
    "show_dots": True,
    "show_numbers": True,
    "follow_mouse": False,
    "format": "x, y",
    "font": " ".join(font_params[:-1]),
    "font_size": int(font_params[-1]),
    "background_color": "#000000",
    "grid_color": "5E81AC",
    "dot_color": "#EBCB8B",
    "text_color": "#ECEFF4",
    "text_outline_color": "#2E3440",
    "fps": 60,
    "text_outline_thickness": 1,
    "text_y_offset": 0,
    "background_opacity": 0.5,
    "grid_thickness": 1,
    "dot_radius": 3,
    "spacing": 400
}

startPosX, startPosY = get_mouse_pos()
posX = startPosX
posY = startPosY
setproctitle.setproctitle("Hyprmouse")
load_config()
width, height = get_screen_res() #Setting values once on launch
draw_window()
