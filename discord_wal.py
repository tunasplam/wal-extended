"""
    This uses beautiful discord.
    Steps to setup:
    O Find the github page, download it.
    O run:
        beautifuldiscord --css ~/.config/discord/discord_custom_stylesheet.css
        - this allows us to alter the css stylesheet for discord and update the window
        everytime the css file is saved.
    O Put the discord_custom_stylesheet in ~/.config/discord

    Note the :root section of the css is where we save the wal colors.

"""

from Color_Grabber import Color_Grabber
from os import environ
from os import system
from re import sub

template_path = environ['HOME'] + "/wal-script/default_configs/custom_stylesheet.css"
discord_css_path = environ['HOME'] + "/.config/discord/custom_stylesheet.css"

try:
    with open(discord_css_path, 'r') as file:
        text = file.read()
    # ALRIGHT this hopefully ends the saga of discord overwriting the
    # css file on update. I added ~/.config/discord to NoUpgrade in
    # /var/cache/pacman/pkg/pacman.conf to make sure we don't have to deal
    # with the problem anymore. We will have to see on the next discrod update.
    # If there are any future issues with discord, it probably has to do with
    # the config folder never getting updated. But hopefully that does not
    # happen :)
    system("python -m beautifuldiscord --css {}".format(discord_css_path))

except FileNotFoundError:
    print("File not found. Copying template over.")
    system("python -m beautifuldiscord --css {}".format(discord_css_path))
    source_path = environ['HOME'] + "/wal-script/default_configs/discord/custom_stylesheet.css"
    dest_path = environ['HOME'] + "/.config/discord/"
    system("cp {} {}".format(source_path, dest_path))
    system("python -m beautifuldiscord --css {}".format(environ['HOME'] + \
           "/.config/discord/custom_stylesheet.css"))
    with open(discord_css_path, 'r') as temp:
            text = temp.read()

cols = Color_Grabber.grab_colors()

# update the colors.
# this re matches the lines that declare the xresources colors. The first
# capture group represents the colors that we want.
replace_re = r'(?<=color{}: )[\w\#]{{7}}'

i = 0
for col in cols:

    text = sub(replace_re.format(i), col, text)
    i += 1

# reopen and save the updated file.
with open(discord_css_path, 'w') as file:
    file.write(text)
