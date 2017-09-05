#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Module that allows a groupt to define 'sub-groups' for easy notification
# to interested parties, similar to Discord roles
import pickle
from pathlib import Path
from utility import is_from_admin

def get_chat_roles(chat_data, chat_id):
    return chat_data.setdefault('roles', get_roles_file(chat_id))

def get_roles_file(chat_id):
    f_name = Path(str(chat_id)+'.role')
    if not f_name.is_file():
        return {}
    with open(f_name, 'rb') as f:
        roles = pickle.load(f)
    return roles
def save_roles_file(chat_data, chat_id):
    with open(str(chat_id)+'.role', 'wb') as f:
        pickle.dump(chat_data['roles'], f, protocol=pickle.HIGHEST_PROTOCOL)
        
def join(bot, update, args, chat_data):
    if len(args) == 0:
        update.message.reply_text("Usage: /join [role_name]")
        return
    roles = get_chat_roles(chat_data, update.message.chat_id)
    role = args[0] 
    if role not in roles:
        update.message.reply_text("Role does not exist")
        return
    roles[role].add(update.effective_user.name)
    update.message.reply_text("Joined role "+role)
    save_roles_file(chat_data, update.message.chat_id)
def create_role(bot, update, args, chat_data):
    if len(args) == 0:
        update.message.reply_text("Usage: /create_role [role_name]")
    chat_type = update.message.chat.type
    if (chat_type == "group" or chat_type == "supergroup") and not is_from_admin(bot, update):
        update.message.reply_text("Command only available to admins")
        return
    roles = get_chat_roles(chat_data, update.message.chat_id)
    role = args[0]
    if role in roles:
        update.message.reply_text("Role already exists")
        return
    roles[args[0]] = set()
    update.message.reply_text("Created role "+args[0])
    save_roles_file(chat_data, update.message.chat_id)
def notify(bot, update, args, chat_data):
    if len(args) == 0:
        update.message.reply_text("Usage: /notify [role_name]")
        return
    roles = get_chat_roles(chat_data, update.message.chat_id)
    role = args[0]
    if role not in roles:
        update.message.reply_text("Role does not exist")
        return
    string = "Calling role "+role+": "
    for username in roles[role]:
        string += username + " "
    update.message.reply_text(string)
    
