#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Job
import logging
import xkcd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = config.ConfigParser()
config.read('jao.ini')

def start(bot, update):
    update.message.reply_text("I°_°I\nCommencing opperation...")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    
    
def main():
    updater = Updater(config['KEY'][api_key])
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    # setting up xkcd commands
    dp.add_handler(CommandHandler("xkcd", xkcd.get,
                                  pass_args=True,
                                  pass_job_queue=True))

    dp.add_error_handler(error)
    
    
    #start bot activity
    update.start_polling()
    update.idle()

if __name__ == "__main__":
    main()
