from mwt import MWT

@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def is_from_admin(bot, update):
    if update.chat.type == "group" or \
       update.chat.type == "supergroup":
        return update.message.from_user.id in get_admin_ids(bot, update.effective_chat.id)
    return True
        
