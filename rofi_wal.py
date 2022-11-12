# NOTE that I went through and got rid of the whitepace padding.
# if a rofi update adds the padding back(it shouldnt...) then
# that could cause a problem that you may currently be troubleshooting.

from Color_Grabber import Color_Grabber
from os import environ

template_path = environ['HOME'] + "/wal-script/default_configs/rofi/Chameleon.rasi_template"
rofi_path = environ['HOME'] + "/.config/rofi/Chameleon.rasi"


def main():

    colors_dict = Color_Grabber.grab_colors_dict()

    # convert the hex colors to rgba
    for key in colors_dict.keys():
        colors_dict[key] = hex_to_rgba(colors_dict[key], 80)

    # open and format the template
    with open(template_path, 'r') as f:
        rofi_config = f.read().format_map(colors_dict)

    # save it to the config location
    with open(rofi_path, 'w') as f:
        f.write(rofi_config)


def hex_to_rgba(hex, a):
    """converts hex to rgba

    Args:
        hex (str): hex color we are converting from
        a (int): a value for rgba

    Returns:
        str: input color in rgba
    """
    hex = hex.lstrip('#')
    temp = list(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return "( {}, {}, {}, {} % )".format(temp[0], temp[1], temp[2], a)
