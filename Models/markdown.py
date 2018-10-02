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
#   Model to hold data from a Class retrieved via scraping
##
class Markdown():
    @classmethod
    def strip_markdown(_,func):
        def func_wrapper(self, *args, **kwargs)->str:
            string_to_format = func(self,*args,**kwargs)
            markdown_array = ['*','_','[',']','(',')','`']
            for x in markdown_array:
                string_to_format = string_to_format.replace(x, " ")
            return string_to_format
        return func_wrapper
    
    @classmethod
    def wrap_blockquotes(_,func):
        def func_wrapper(self,*args,**kwargs)->str:
            sanitized_string = func(self,*args,**kwargs)
            message_array = []
            message_array.append("```\n")
            message_array.append(sanitized_string)
            message_array.append("```")
            return "".join(message_array)
        return func_wrapper    
    
    @classmethod
    def wrap_italics(_,func):
        def func_wrapper(self,*args,**kwargs)->str:
            sanitized_string = func(self,*args,**kwargs)
            message_array = []
            message_array.append("_")
            message_array.append(sanitized_string)
            message_array.append("_")
            return "".join(message_array)
        return func_wrapper    