# Hyprmouse

## Control the mouse with your keyboard using Vim Motions
A highly customizeable Hyprland overlay that enables you to never move your hands away from the keyboard.

## Binds
Custom keybinds will be supported shortly
- <b>DEL</b> - Force quit the app
- <b>ESC</b> - Return to the initial position and close the overlay
- <b>Return</b> - Confirm the new position and close the overlay
- <b>0</b>-<b>9</b> - Enter a digit
- <b>B</b>/<b>b</b>/<b>Backspace</b> - Delete a digit
- <b>+</b>/<b>=</b> - Switch to positive direction
- <b>-</b>/<b>=</b> - Switch to negative direction
- <b>I</b>/<b>i</b> - Invert direction
- <b>X</b>/<b>x</b> - Move on the X axis in the set direction
- <b>Y</b>/<b>y</b> - Move on the Y axis in the set direction
- <b>R</b>/<b>r</b> - Move to the center of the screen
- <b>U</b>/<b>u</b> - Undo the last position change

## Config
Config file should be located in `~/.config/hypr/hyprmouse.conf`  
Some of the things to keep in mind:
- All of the following values are valid for bools: `True`/`true`, `False`/`false`
- All the colors must be provided as HEX values, # is not required
- Keep the fps relatively low, it can have a huge impact on the performance
- Spaces don't matter, `key=value` is just as fine as `key = value`
- Font will be retrieved from your gtk settings but you can overwrite it and adjust the size

<br/>

<b>Example</b> provided below contains all the options
- `show_ui = True` - <b>bool</b> - Will the UI be shown
- `show_background = True` - <b>bool</b> - Will the background be shown
- `show_grid = True` - <b>bool</b> - Will the grid be shown
- `show_dots = True` - <b>bool</b> - Will the dots be shown
- `show_numbers = True` - <b>bool</b> - Will the numbers be shown
- `follow_mouse = False` - <b>bool</b> - Will the UI be relative to the cursor
- `format = x, y` - <b>string</b> - How will the coordinates be formatted
- `font = Cascadia Code` - <b>string</b> - Font that the UI will use
- `font_size = 30` - <b>int</b> - Font size
- `background_color = #000000` - <b>string</b> - Color of the background
- `grid_color = #5E81AC` - <b>string</b> - Color of the grid
- `dot_color = #EBCB8B` - <b>string</b> - Color of dots
- `text_color = #ECEFF4` - <b>string</b> - Color of the text
- `text_outline_color = #2E3440` - <b>string</b> - Color of the text outline
- `fps = 60` - <b>int</b> - Framerate at which the app will be redrawn
- `background_opacity = 0.5` - <b>float</b> - Opacity of the background
- `spacing = 400` - <b>int</b> - Spacing between grid lines
- `grid_thickness = 1` - <b>float</b> - Thickness of grid lines
- `dot_radius = 3` - <b>float</b> - Radius of dots
- `text_outline_thickness = 1` - <b>float</b> - Thickness of the text outline(I would advise against going above 2)
- `text_y_offset = 0` - <b>float</b> - Y offset applied to text
