#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
# this runs wal and all our extended wal scripts. All one command.
# run with command args similar to those of wal

  TODO if there are any running instances of chromium they will need to be
  rebooted/refreshed in order for changes to metriculate

# TODO
# O YTMDesktop -> this will be similar to the way discord is done.. see apar or
# whatever for hacking electron with css injection.
"""
from os import system
from os import listdir
from os import environ
from os import popen
import os.path
from re import sub
from random import choice
from Color_Grabber import Color_Grabber
import argparse

HOME = environ['HOME']
script_path = os.path.join(HOME, 'wal-script')
images_path = os.path.join(script_path, 'images')
reddit_images_path = os.path.join(script_path, 'reddit_images')


def main():

    parser = argparse.ArgumentParser(
        description="Massively Extended Wal Script.")

    parser.add_argument('-R', '--restore', action='store_true',
                        help="restore config from previous session")

    parser.add_argument('--random', action='store_true',
                        help="chose a random image from ~/wal-script/images")

    parser.add_argument('-i', '--image', action='store', nargs=1,
                        help="run with a given image")

    parser.add_argument('-s', '--save', action='store_true',
                        help="save the given backgroun to ~/wal-script/images")

    parser.add_argument('--reddit', action='store_true',
                        help="use a random image from the reddit folder")

    parser.add_argument('-A', '--autoscroll', action='store_true',
                        help="automatically scroll through reddit images and choose which ones you want to save")

    parser.add_argument('--browse_directory', action='store', nargs=1,
                        help="easily test out all of the images in a directory.")

    args = vars(parser.parse_args())
    if args['restore']:
        system("wal -R -n")
        image = grab_current_background()
        change_background(image)
        extra_scripts()

    elif args['random']:
        image = grab_random_image()
        change_background(image)
        system("wal -i {} -n".format(image))
        extra_scripts()

    elif args['image']:
        image = os.path.join(script_path, args['image'][0])
        change_background(image)
        print(args['image'][0])
        system("wal -i {} -n".format(args['image'][0]))
        extra_scripts()

    elif args['save']:
        save_current_background()

    elif args['reddit']:
        image = grab_reddit_image()
        change_background(image)
        system("wal -i {} -n".format(image))
        extra_scripts()

    elif args['autoscroll']:
        scroll_reddit_images()

    elif args['browse_directory']:
        scroll_directory(args['browse_directory'][0])


def extra_scripts():
    # First, update color.css
    Color_Grabber.update_colors_css()

    print("Setting Openbox Theme...")
    system("python {}".format(os.path.join(script_path, "openbox_wal.py")))

    print("Setting Sublime Theme...")
    system("python {}".format(os.path.join(script_path, "sublime_wal.py")))

    print("Setting Rofi Theme...")
    system("python {}".format(os.path.join(script_path, "rofi_wal.py")))

    print("Setting Discord Theme...")
    system("python {}".format(os.path.join(script_path, "discord_wal.py")))

    print("Setting tint2 Theme...")
    system("./tint2_wal.sh &> /dev/null 2>&1")


def change_background(image):
    """
    Change the background by editting the nitrogen config file.
    Note that the image path here must be absolute!

    Args:
        image (str): ABSOLUTE path to the image.
    """

    # This does the actual setting of the bg.
    system("nitrogen --set-tiled {}".format(image))

    # This saves the setting to consist through multiple sessions..
    # but wal-script is called on startup, making this seemingly pointless.
    # However, this is a nice way for us to figure out the current desktop
    # background for things like saving the image.

    # open up the config file to save our new preferred background
    with open(os.path.join(HOME, ".config/nitrogen/bg-saved.cfg"), 'r') as temp:
        cfg = temp.read()

    cfg = sub(r'(?<=file\=).*', image, cfg)

    with open(os.path.join(HOME, ".config/nitrogen/bg-saved.cfg"), 'w') as temp:
        temp.write(cfg)


def grab_random_image():
    images = listdir(images_path)
    image = choice(images)
    return os.path.join(images_path, image)


def scroll_directory(directory):
    """Scrolls a given directory in a manner very similary to doing so
    for the reddit ones.
    This would be for if you pulled a batch folder of wallpapers from the
    internet and wanted to test them all out.

    Args:
        directory (str): absolute path to the directory with the images.
    """
    images = listdir(directory)
    print("Cycling through images in {}".format(directory))
    print("Y -> Save N -> Don't save")
    for image in images:
        image_path = os.path.join(directory, image)
        change_background(image_path)
        system("wal -i {}".format(image_path))
        extra_scripts()
        response = input("Save? [Y/N]: ")

        if response == "Y":
            save_current_background()
            print("Saved.")

        else:
            print("Passed.")

        # Remove it to clean up.
        system("rm {}".format(image_path))

    print("All done.")


def scroll_reddit_images():
    """
    Starts out by calling grab_wallpapers.py
    Then cycles through the images giving a prompt asking
    if you would like to keep them or not.
    """
    # grab wall papers
    system("python {}".format(os.path.join(script_path, "grab_wallpapers.py")))

    # Count how many were grabbed.
    images = listdir(reddit_images_path)
    print("Cycling through {} grabbed images.".format(len(images)))

    # Cylce through them and ask for what to do
    print("Y -> Save N -> Don't save")
    image_folder_path = os.path.join(script_path, "reddit_images")
    for image in images:
        print(image)
        image_path = os.path.join(image_folder_path, image)
        change_background(image_path)
        system("wal -i {}".format(image_path))
        extra_scripts()
        response = input("Save? [Y/N]: ")

        if response == "Y":
            save_current_background()
            print("Saved.")

        else:
            print("Passed.")

    print("All done.")


def grab_reddit_image():
    """
    Grabs a reddit image. Does so systematically.
    First, it checks if a reddit image is being used.
        -> if so, use the NEXT image in the directory
        -> otherwise, use the first.

    Returns:
        string: path to a reddit image to use.
    """
    images = listdir(reddit_images_path)

    current_background = grab_current_background()
    if "reddit_images" in current_background:
        # Stupid hacky way of getting the filename.
        current_background = current_background[len(reddit_images_path):]
        image_index = images.index(current_background)

        # Grab the next image if a reddit image is being used.
        try:
            image = images[image_index + 1]

        # If last image is being used, wrap around to the first.
        except IndexError:
            image = images[0]

    else:
        image = images[0]

    return reddit_images_path + "/" + image


def grab_current_background():
    """For nitrogen. Returns the name of the currently set backgroun
    by piping the cat of the config file to grep.

    Returns:
        str: path to the background image that is currently in use.
    """
    return popen(
        "cat {}/.config/nitrogen/bg-saved.cfg | grep file".format(HOME)
        ).read()[5:-1]


def save_current_background():
    """Takes the currently saved background from nitrogen config and moves
    it to the ~/wal-script/images directory, if it is not already there.
    """
    # 5:-1 strips out the file= and the trailing newline.
    image_url = grab_current_background()

    # cp this current image to the images folder.
    system('cp {} {}'.format(image_url, images_path))
    print("Successfully saved image.")


main()
