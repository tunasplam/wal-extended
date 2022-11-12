"""
    Edits the massive xml file that is the sublime text settings.

    Okay we need to make a package so that everytime we redo our
    system this is all just one button press away.

    For this:
    - need to move Chameleon.tmTheme to
    ~/.config/sublime-text-3/Packages/Chameleon/Chameleon.tmTheme
    Then it will show up as an option under Preferences->color scheme
    in the main program.
    - Gonna make it a try-catch on the file not found for opening the
    file.

    # TODO top bar of sublime requires refresh to set colors.
    # left file explorer not either.

"""

from os import environ
from Color_Grabber import Color_Grabber

template_path = environ['HOME'] + "/wal-script/default_configs/sublime-text-3/Chameleon.tmTheme_template"
dest_path = environ['HOME'] + "/.config/sublime-text/Packages/Chameleon/Chameleon.tmTheme"


def main():

    # extract the colors generated by wal and stored in xresources
    colors_dict = Color_Grabber.grab_colors_dict()

    with open(template_path, 'r') as f:
        theme = f.read().format_map(colors_dict)

    try:
        with open(dest_path, 'w') as f:
            f.write(theme)

    except FileNotFoundError:
        print("SUBLIME ISSUE.")
        print("ERROR could not find the filepath where Chameleon color scheme is saved.")
        print("Is this a new install?? Moving the file to the correct spot.")
        print("Make sure you change your color scheme to Chameleon in sublime")
        print("Preferences -> Color Scheme")
        raise


main()
