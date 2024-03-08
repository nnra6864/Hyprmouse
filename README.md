# Hyprmouse

## Control the mouse with your keyboard using Vim Motions
A highly customizeable Hyprland overlay that enables you to never move your hands away from the keyboard.

## Binds
Custom keybinds will be supported shortly
- <b>DEL</b> - Force quit the app
- <b>ESC</b> - Return to the initial position and close the overlay
- <b>Return</b> - Confirm the new position and close the overlay
- <b>0</b>-<b>9</b> - Enter a digit
- <b>b</b>/<b>B</b>/<b>Backspace</b> - Delete a digit
- <b>+</b>/<b>=</b> - Switch to positive direction
- <b>-</b>/<b>=</b> - Switch to negative direction
- <b>i</b>/<b>I</b> - Invert direction
- <b>x</b>/<b>X</b> - Move on the X axis in the set direction
- <b>y</b>/<b>Y</b> - Move on the Y axis in the set direction
- <b>r</b>/<b>R</b> - Move to the center of the screen
- <b>u</b>/<b>U</b> - Undo the last position change

## Config
Config file should be located in `~/.config/hypr/hyprmouse.conf`
Some of the things to keep in mind:
- All of the following values are valid for bools: `True`/`true`, `False`/`false`
- All the colors must be provided as HEX values, # is not required
- Keep the fps relatively low, it can have a huge impact on the performance
- Spaces don't matter, `key=value` is just as fine as `key = value`
- Font will be retrieved from your gtk settings but you can overwrite it and adjust the size
Example provided below contains all the options
- `show_ui = True` - Will the UI be shown
- `show_background = True` - Will the background be shown
- `show_grid = True` - Will the grid be shown
- `show_dots = True` - Will the dots be shown
- `show_numbers = True` - Will the numbers be shown
- `follow_mouse = False` - Will the UI be relative to the cursor
- `format = "x, y"` - How will the coordinates be formatted
- `font = Cascadia Code` - Font that the UI will use
- `font_size = 30` - Font size
- `background_color = #000000` - Color of the background
- `grid_color = #5E81AC` - Color of the grid
- `dot_color = #EBCB8B` - Color of dots
- `text_color = #ECEFF4` - Color of the text
- `text_outline_color = #2E3440` - Color of the text outline
- `fps = 60` - Framerate at which the app will be redrawn
- `background_opacity = 0.5` - Opacity of the background
- `spacing = 400` - Spacing between grid lines
- `grid_thickness = 1` - Thickness of grid lines
- `dot_radius = 3` - Radius of dots
- `text_outline_thickness = 1` - Thickness of the text outline(I would advise against going above 2)
- `text_y_offset = 0` - Y offset applied to text
