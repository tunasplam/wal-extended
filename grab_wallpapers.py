'''
 Grab wallpapers from r/wallpaper.

On startup. Initiliaze this by filling a folder with
suitable images from top 30 or so top posts.

When set to reddit mode, wal-extended will go through
this folder in a specified order.
'''

from praw import Reddit
from re import compile
from re import sub
from os import popen
from os import listdir
from os import system
from os import environ
from urllib.request import urlretrieve

hot_limit = 100
title_re = compile(r'[[(]\s*1920\s*[*x]\s*1080\s*[])]')
ext_re = compile(r'(?<=\.)[a-z]{3}$')
verify_re = compile(r'\s1920x1080\s')

reddit_images_path = environ['HOME'] + "/wal-script/reddit_images/"


def populate_wallpapers_folder(reddit):
    """Clears and then fills the temporary wallpapers folder
    with images from the top hot posts using the post titles
    as their names.

    Args:
        reddit (reddit instance): Read only instance of reddit.
    """

    # clear out the current images.
    system("rm {}*".format(reddit_images_path))

    # Scour the first of a given number of hot posts.
    for submission in reddit.subreddit("wallpaper").hot(limit=hot_limit):
        # check if they are 1920 x 1080 based on the title
        if title_re.search(submission.title):
            # skip multi-image "gallery" posts
            if "/gallery/" in submission.url:
                continue

            # get the filename extension.
            # Might not have an extension.
            try:
                ext = ext_re.findall(submission.url)[0]
            except IndexError:
                continue
            title = submission.title.replace(' ', '')
            title = sub('[()\'\"\\/-]', '', title)
            url = submission.url

            # save the images using post title as filename.
            filename = reddit_images_path + title + "." + ext
            # Need to replace () with [] in order for sh to work.

            print(title)
            urlretrieve(url, filename)


def verify_images():
    # Remove images that are not ~Truly~ 1920x1080
    # TODO: Maybe build in a cropper that quickly fixes it. These
    # images should only be marginally off.
    images = listdir(reddit_images_path)
    for image in images:
        verify_results = popen("identify {}".format(
            reddit_images_path + image)).read()

        if not verify_re.search(str(verify_results)):
            system('rm {}'.format(reddit_images_path + image))


def create_reddit_instance():
    # Create a read-only instance.
    try:
        with open('.reddit_info', 'r') as f:
            reddit_info = f.read().split('\n')

    except FileNotFoundError:
        print("Hmm looks like you lost your reddit client info file.")
        raise

    reddit = Reddit(
        client_id=reddit_info[0],
        client_secret=reddit_info[1],
        user_agent="test"
        )
    return reddit


reddit = create_reddit_instance()
populate_wallpapers_folder(reddit)
verify_images()
