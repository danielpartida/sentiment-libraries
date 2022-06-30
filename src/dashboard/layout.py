moonpass_colors = {
    'purple': 'rgb(121, 71, 247)',
    'pink': 'rgb(231, 82, 117)',
    'light_blue': 'rgb(30, 155, 215)',
    'white': 'rgb(255, 255, 255)',
    'very light blue': 'rgb(148, 228, 255)',
    'dark_blue': 'rgb(19, 29, 51)'
}


def color_gradient(gradient_factor: float, col: tuple):
    """
    Returns a rgb color in the blue family
    Args:
        gradient_factor: float of how strong the blue color shall be changed, max is 2
        col:
    Returns:
        rgb color in blue family
    """

    _red = col[0]
    _green = col[1]
    _blue = col[2]

    if gradient_factor < 1:
        _red = _red * gradient_factor
        _green = _green * gradient_factor
        _blue = _blue * gradient_factor
    elif gradient_factor >= 1:
        _red = _red + ((gradient_factor - 1) * (255 - _red))
        _green = _green + ((gradient_factor - 1) * (255 - _green))
        _blue = _blue + ((gradient_factor - 1) * (255 - _blue))

    result = "rgb({red}, {green}, {blue})".format(red=_red, green=_green, blue=_blue)

    return result


main_color_tuple = (0, 123, 255)
background_page = color_gradient(1.98, main_color_tuple)  # "rgb(244, 244, 251)"
font_color = 'grey'
font_family = 'Poppins'  # "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap"

# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    # "margin-left": "18rem",
    # "margin-right": "2rem",
    "padding": "2rem 1rem",
    'color': font_color,
    'fontFamily': font_family
}