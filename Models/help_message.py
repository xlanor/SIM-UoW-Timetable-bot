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
#   Help message.
##
# Native/3rd party imports.
# 
# Local imports
from .exceptions import *
from Models.markdown import Markdown
from cfg import Configuration
from Models.singleton_sp import Singleton


class HelpMessage(metaclass = Singleton):
    def __init__(self):
        self.__cfg = Configuration()

    def get_help_message(self)->str:
        email = self.__get_type("email")
        author = self.__inline_author()
        git_uri = self.__inline_url(self.__cfg.GITHUB_URL,"Github")
        inline_uri = self.__inline_url(f"{self.__cfg.GITHUB_URL}/issues","Open an Issue")
        message_array = []
        message_array.append(f"{self.__title()}\n\n")
        message_array.append(f"Before contacting the owner, check the README in {git_uri} to make sure that your issue is not addressed in the FAQs\n")
        message_array.append("\n")
        message_array.append(f"If you are confident that your issue is not already addressed, kindly refer to the following links:\n\n")
        message_array.append(f"📧 Email: {email}\n")
        message_array.append(f"📱 Telegram: {author}\n")
        message_array.append(f"📊 Github Issues:{inline_uri}\n")
        message_array.append("\n")
        return "".join(message_array)
    
    @Markdown.wrap_bold
    def __title(self)->str:
        return "Need Help? Read the following:"

    def __inline_author(self)->str:
        return Markdown.get_inline_user(self.__cfg.AUTHOR_TELEGRAM_ID,"Jingkai")
    
    def __inline_url(self,url_to_display:str, text_to_show: str)->str:
        return Markdown.get_url(url_to_display,text_to_show)
    
    @Markdown.wrap_italics
    def __get_type(self,type:str)->str:
        if type == "email":
            return self.__cfg.AUTHOR_EMAIL
        elif type == "tg":
            return self.__cfg.AUTHOR_TELEGRAM
            

        
