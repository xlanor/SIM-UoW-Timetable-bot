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
#  Methods for the reminder system
##
from datetime import datetime
from datetime import timedelta
import traceback

# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from cfg import Configuration
from Models.reminder_message import ReminderMessage

def toggle_morning(bot,update):
    uid = update.message.from_user.id
    try:
        if db_interface.user_exist(uid):
            if db_interface.toggle_alert(uid,True):
                message ="Morning alert has been sucessfully *enabled*!"
            else:
                message = "Morning alert has been sucessfully *disabled*!"
            update.message.reply_text(message,parse_mode='Markdown')
        else:
            message_array=["You are not registered!\n"]
            message_array.append("Would you like to register using /register?")
            message = "".join(message_array)
            update.message.reply_text(message,parse_mode='Markdown')
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
        # To be updated

def toggle_night(bot,update):
    uid = update.message.from_user.id
    try:
        if db_interface.user_exist(uid):
            if db_interface.toggle_alert(uid,False):
                message ="Nightly alert has been sucessfully *enabled*!"
            else:
                message = "Nightly alert has been sucessfully *disabled*!"
            update.message.reply_text(message,parse_mode='Markdown')
        else:
            message_array=["You are not registered!\n"]
            message_array.append("Would you like to register using /register?")
            message = "".join(message_array)
            update.message.reply_text(message,parse_mode='Markdown')
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
        # To be updated

def morning_alert(bot,update):
    try:
        user_list = db_interface.get_all_users_alert("morning")
        for user in user_list:
            #cur_dt = datetime.now().replace(hour=0, minute=0, second=0)
            list_of_cur_classes = user.get_list_of_class_by_date(datetime.now().date())
            rm = ReminderMessage(list_of_cur_classes,"Morning",user.name,datetime.strftime(datetime.now(),'%b %d %Y'))
            msg = rm.get_message()
            bot.send_message(chat_id = user.telegram_id,text = msg,parse_mode='Markdown')
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
        # To be updated

def nightly_alert(bot,update):
    try:
        user_list = db_interface.get_all_users_alert("nightly")
        for user in user_list:
            list_of_cur_classes = user.get_list_of_class_by_date(((datetime.now())+timedelta(1)).date())
            rm = ReminderMessage(list_of_cur_classes,"Night",user.name,datetime.strftime((datetime.now())+timedelta(1),'%b %d %Y'))
            msg = rm.get_message()
            bot.send_message(chat_id = user.telegram_id,text = msg,parse_mode='Markdown')
    except Exception as e:
        print(str(e))
        # To be updated