#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Module responsible for handling XKCD comics.
# Can get arbitrary comics and has a job that posts them periodically
from random import randint
import urllib.request
import json

# number of the latest xkcd as an initial hint for the random grabber
# gets updated every time someone calls for the latest one
latest_num = 1789

def get_latest():
    response = urllib.request.urlopen("http://xkcd.com/info.0.json")
    latest =json.loads(response.read()
                       .decode(response.info().get_param('charset') or 'utf-8'))
    latest_num = latest["num"]
    return latest

def get_comic_json(n):
    response = urllib.request.urlopen("http://xkcd.com/{}/info.0.json".format(n))
    return json.loads(response.read()
                      .decode(response.info().get_param('charset') or 'utf-8'))

def post_comic(comic, update):
    text = "Title: {}\nAlt: {}".format(comic['safe_title'], comic['alt'])
    # image = urllib.request.urlopen(comic['img']).read()
    image  = comic['img']
    update.message.reply_photo(photo=image,
                               caption=text)

def get(bot, update, args):
    """
    Responds with a comic. If argument provided, responds with that comic. Else, random
    """
    comic_num = 0
    if len(args) == 0:
        comic_num = randint(0, latest_num)
    else:
        try:
            comic_num = int(args[0])
        except:
            update.message.reply_text("Usage: /xkcd [number]")
    if comic_num == 0:
        comic = get_latest()
    else:
        comic = get_comic_json(comic_num)
    post_comic(comic, update)

latest_num = get_latest()
if __name__ == "__main__":
    n = int(input())
    print(get_latest())
    print(get_comic(n))
    
    
