import setproctitle, cairo
import subprocess, re, gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell


def get_screen_res():
    output = subprocess.check_output(["hyprctl", "monitors", "all"]).decode("utf-8")
    match = re.search(r"\d+x\d+", output)
    if match:
        wh = match.group()
        w, h = map(int, wh.split('x'))
        return w, h
    else:
        print("Failed to retrieve the resolution.")
width, height = get_screen_res()
step_size = 500

def draw_grid(window, cr):
    global step_size
    print("here")
    cr.set_source_rgb(0.9255, 0.9373, 0.9569)
    cr.set_line_width(0.5)

    for x in range((width // 2) % step_size, width, step_size):
        cr.move_to(x, 0)
        cr.line_to(x, height)
        cr.stroke()

    for y in range((height // 2) % step_size, height, step_size):
        cr.move_to(0, y)
        cr.line_to(width, y)
        cr.stroke()

    cr.set_source_rgb(0.1328, 0.1569, 0.1569)
    font = Gtk.Settings.get_default().get_property("gtk-font-name").rsplit(maxsplit=1)[0]
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(20)
    
    for x_offset in range(-2, 3):
        for y_offset in range(-2, 3):
            if x_offset != 0 or y_offset != 0:
                for x in range((width // 2) % step_size, width, step_size):
                    for y in range((height // 2) % step_size, height, step_size):
                        label = f"{x}, {height - y}"
                        x_text_offset = x - cr.text_extents(label)[4] // 2 + x_offset
                        y_text_offset = y + cr.text_extents(label)[3] // 2 + y_offset
                        cr.move_to(x_text_offset, y_text_offset - cr.text_extents(label)[3])
                        cr.show_text(label)

                        relative_label = f"{x - prevXPos}, {height - (prevYPos + y)}"
                        x_text_offset = x - cr.text_extents(relative_label)[4] // 2 + x_offset
                        y_text_offset = y + cr.text_extents(relative_label)[3] // 2 + y_offset
                        cr.move_to(x_text_offset, y_text_offset + cr.text_extents(relative_label)[3])
                        cr.show_text(relative_label)

    
    for x in range((width // 2) % step_size, width, step_size):
        for y in range((height // 2) % step_size, height, step_size):
            cr.set_source_rgb(0.5333, 0.7529, 0.8157)
            label = f"{x}, {height - y}"
            x_text_offset = x - cr.text_extents(label)[4] // 2
            y_text_offset = y + cr.text_extents(label)[3] // 2
            cr.move_to(x_text_offset, y_text_offset - cr.text_extents(label)[3])
            cr.show_text(label)

            cr.set_source_rgb(0.9216, 0.7961, 0.5455)
            relative_label = f"{x - prevXPos}, {height - (prevYPos + y)}"
            x_text_offset = x - cr.text_extents(relative_label)[4] // 2
            y_text_offset = y + cr.text_extents(relative_label)[3] // 2
            cr.move_to(x_text_offset, y_text_offset + cr.text_extents(relative_label)[3])
            cr.show_text(relative_label)

            cr.set_source_rgb(0.9255, 0.9373, 0.9569)
            cr.arc(x, y, 3, 0, 2 * 3.14159)
            cr.fill_preserve()

    return False


xPos = 0
yPos = 0
prevXPos, prevYPos = map(int, subprocess.check_output(["hyprctl", "cursorpos"]).decode("utf-8").split(','))
direction = 1
liveUpdate = True

def editAxis(axis, window, event):
    global liveUpdate
    global isEditingX, isEditingY
    global xPos, yPos, prevXPos, prevYPos
    
    if isEditingX: yPos = prevYPos
    else: xPos = prevXPos

    if event.keyval == Gdk.KEY_Escape:
        isEditingX = isEditingY = False
        subprocess.run(["ydotool", "mousemove", "-a", f"{prevXPos}", f"{height - prevYPos}"])
        xPos = yPos = 0
        return
    if event.keyval == Gdk.KEY_Return:
        subprocess.run(["ydotool", "mousemove", "-a", f"{xPos}", f"{height - yPos}"])
        isEditingX = isEditingY = False
        prevXPos = xPos
        prevYPos = yPos
        xPos = yPos = 0
        window.queue_draw()
        return

    if chr(event.keyval).isdigit():
        if axis == 'x': xPos = xPos * 10 + int(chr(event.keyval))
        else: yPos = yPos * 10 + int(chr(event.keyval))
        if liveUpdate: subprocess.run(["ydotool", "mousemove", "-a", f"{xPos}", f"{height - yPos}"])
    elif event.keyval == Gdk.KEY_BackSpace:
        if axis == 'x': xPos = xPos // 10
        else: yPos = yPos // 10
        if liveUpdate: subprocess.run(["ydotool", "mousemove", "-a", f"{xPos}", f"{height - yPos}"])


def editAxisRelative(axis, window, event):
    global isRelEditingX, isRelEditingY, direction
    global xPos, yPos, prevXPos, prevYPos

    if event.keyval == Gdk.KEY_Escape:
        isRelEditingX = isRelEditingY = False
        subprocess.run(["ydotool", "mousemove", "-a", f"{prevXPos}", f"{height - prevYPos}"])
        direction = 1
        return
    if event.keyval == Gdk.KEY_Return:
        subprocess.run(["ydotool", "mousemove", "-a", f"{prevXPos + (xPos * direction)}", f"{height - prevYPos - (yPos * direction)}"])
        isRelEditingX = isRelEditingY = False
        prevXPos = prevXPos + (xPos * direction)
        prevYPos = height - prevYPos + (yPos * direction)
        xPos = yPos = 0
        direction = 1
        window.queue_draw()
        return

    if chr(event.keyval) == '+' or chr(event.keyval) == '=':
        direction = 1
    if chr(event.keyval) == '-' or chr(event.keyval) == '_':
        direction = -1
    if chr(event.keyval).lower == 'i':
        direction = -direction

    if chr(event.keyval).isdigit():
        if axis == 'x': xPos = xPos * 10 + int(chr(event.keyval))
        else: yPos = yPos * 10 + int(chr(event.keyval))
    elif event.keyval == Gdk.KEY_BackSpace:
        if axis == 'x': xPos = xPos // 10
        else: yPos = yPos // 10
    
    if liveUpdate: subprocess.run(["ydotool", "mousemove", "-a", f"{prevXPos + (xPos * direction)}", f"{height - prevYPos - (yPos * direction)}"])

isEditingX = False
isEditingY = False
isRelEditingX = False
isRelEditingY = False

def on_key_press(window, event):
    if event.keyval == Gdk.KEY_Delete:
        Gtk.main_quit()

    global step_size
    global liveUpdate
    global isEditingX, isEditingY, isRelEditingX, isRelEditingY
    global xPos, yPos, prevXPos, prevYPos

    if isEditingX:
        editAxis('x', window, event)
        return
    if isEditingY:
        editAxis('y', window, event)
        return
    if isRelEditingX:
        editAxisRelative('x', window, event)
        return
    if isRelEditingY:
        editAxisRelative('y', window, event)
        return

    if event.keyval == Gdk.KEY_Escape or event.keyval == Gdk.KEY_Return:
        Gtk.main_quit()

    if chr(event.keyval).lower() == 'r':
        prevXPos = width // 2
        prevYPos = height // 2
        subprocess.run(["ydotool", "mousemove", "-a", f"{prevXPos}", f"{prevYPos}"])
        window.queue_draw()

    if chr(event.keyval).lower() == 'l':
        liveUpdate = not liveUpdate
    
    if chr(event.keyval).lower() == '+' or chr(event.keyval).lower() == '=':
        step_size = step_size - 100
        window.queue_draw()

    if chr(event.keyval).lower() == '-' or chr(event.keyval).lower() == '_':
        step_size = step_size + 100
        window.queue_draw()

    isEditingX = chr(event.keyval) == 'X';
    isEditingY = chr(event.keyval) == 'Y';
    isRelEditingX = chr(event.keyval) == 'x';
    isRelEditingY = chr(event.keyval) == 'y';


def draw_window():
    window = Gtk.Window()
    window.set_title("Hyprmouse")
    window.set_size_request(width, height)
    window.resize(1, 1)
    window.set_app_paintable(True)
    
    GtkLayerShell.init_for_window(window)
    GtkLayerShell.set_namespace(window, "Hyprmouse")
    GtkLayerShell.set_layer(window, GtkLayerShell.Layer.OVERLAY)
    GtkLayerShell.set_keyboard_mode(window, GtkLayerShell.KeyboardMode.EXCLUSIVE)
    window.connect('draw', draw_grid)
    window.connect("key-press-event", on_key_press)

    window.show_all()
    window.connect('destroy', Gtk.main_quit)
    Gtk.main()


setproctitle.setproctitle("Hyprmouse")
draw_window()
