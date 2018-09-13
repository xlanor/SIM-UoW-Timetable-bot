#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
#   Copyright (C) 2018 JING KAI TAN
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
#   License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##
#  Methods for the registration process.
##
# 3rd party or native import
from telegram.ext import ConversationHandler

# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from Models.encryption import Encrypt

# declares state for subsequent import.
NAME,USERNAME,PASSWORD,APP_KEY = range(4)


def start_register(bot,update):
    """
    Kickstarts registeration process. Gets name and 
    subsequently passes it to the next handler in process.
    """
    try:
        # gets the telegram ID
        tg_id = update.message.from_user.id
        # Checks the database for the user ID
        message_array = []
        if not db_interface.user_exist(tg_id):
            message_array.append("Hi! Let's get started by registering with this bot\n")
            message_array.append("By using this bot, you hereby declare that you have read the documentation and disclaimer on github.\n")
            message_array.append("*As such, you release the author from any responsibilities of events incurred by the usage of this bot*\n")
            message_array.append("At any point of time during this process, you can stop the bot by typing /cancel\n")
            message_array.append("Now, can I have your name?")
            message = "".join(message_array)
            update.message.reply_text(message,parse_mode='Markdown')
            # instructs the chatbox to move to the next method.
            return NAME
        else:
            message_array.append("You are already registered!\n")
            message_array.append("If you have forgotten your application key, please use /forget to clear your information and re-register.")
            message = "".join(message_array)
            update.message.reply_text(message,parse_mode='Markdown')
            return ConversationHandler.END

    except Exception as e:
        print(str(e)) #To be changed.
        return ConversationHandler.END


def name(bot,update,user_data):
    """
    Receives name from registeration process. Gets
    username and passes it to the next handler in the process.
    """
    try:
        user_input_name = update.message.text
        user_data["user_id"] = update.message.from_user.id
        user_data["name"] = user_input_name
        message_array = [f"Thank you, {user_input_name}.\n"]
        message_array.append("Now, can I have your *SIMConnect* User ID?")
        message = "".join(message_array)
        update.message.reply_text(message,parse_mode = 'Markdown')
        return USERNAME
    except Exception as e:
        print(str(e)) #to be changed
        return ConversationHandler.END

def username(bot,update,user_data):
    """
    Gets Password, passes it to next handler in the process.
    """
    try:
        user_input_username = update.message.text
        user_data["username"] = user_input_username
        message_array = ["Successfully received your username\n"]
        message_array.append("Now, I need your SIMConnect password.\n")
        message_array.append("For more information about how your password will be stored, please read the github README.md page.")
        message = "".join(message_array)
        update.message.reply_text(message,parse_mode='Markdown')
        return PASSWORD

    except Exception as e:
        # to be changed.
        print(str(e))
        return ConversationHandler.END

def password(bot,update,user_data):
    """
    Gets password, passes it to next handler in the process.
    """
    try:
        user_input_password = update.message.text
        user_data["password"] = user_input_password
        message_array = ["Successfully received your password\n"]
        message_array.append("Now, I need you to enter an *Application Key*\n")
        message_array.append("This key will be case-sensetive and stripped of all spaces\n")
        message_array.append("This key will be *used to encrypt your password, DO NOT FORGET IT!*\n")
        message = "".join(message_array)
        update.message.reply_text(message,parse_mode='Markdown')
        return APP_KEY

    except Exception as e:
        print(str(e))
        return ConversationHandler.END

def application_key(bot,update,user_data):
    try:
        user_input_application_key = update.message.text
        user_input_application_key = user_input_application_key.strip()
        if len(user_input_application_key) <= 16:
            #TODO: Place the encrypted password in user_data encrypted_password
            pass #TODO: Send to celery for testing. 
        else:
            if not user_input_application_key:
                message = "Please enter an application key"
            else:
                message = "Please enter an encryption key that is under 17 characters."
            update.message.reply_text(message,parse_mode='Markdown')
            return KEY
    
    except Exception as e:
        print(str(e))
        return ConversationHandler.END
def cancel(bot,update):
    """
    Cancels the chatbot process.
    """
    message = "Cancelling registeration! Goodbye"
    update.message.reply_text(message, parse_mode='Markdown')
	return ConversationHandler.END