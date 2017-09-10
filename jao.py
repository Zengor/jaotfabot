#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Job
from functools import wraps
import os
import time
import sys
import configparser
import logging
import xkcd
import notifyroles
import utility

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('jao.ini')

def start(bot, update):
    update.message.reply_text("I°_°I\nCommencing opperation...")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    
def main():
    updater = Updater(token=config['KEY']['api_key'])
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    # setting up xkcd commands
    dp.add_handler(CommandHandler("xkcd", xkcd.get,
                                  pass_args=True))
    
    for command in notifyroles.get_commands():
        dp.add_handler(CommandHandler(**command))
        
    dp.add_handler(CommandHandler("restart",
                                  restart))
    dp.add_error_handler(error)
    
    #start bot activity
    #clean means we ignore updates sent while the bot was off
    updater.start_polling(clean=True)
    updater.idle()

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in config['KEY']['higher_privileges']:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    main()
