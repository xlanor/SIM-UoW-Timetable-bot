#!/usr/bin/python
# -*- coding: utf-8 -*-
class ErrorTemplate():
    def __init__(self, response_code: int, message: str):
        self.__response_code = response_code
        self.__message = message

    def dict(self):
        return {
            "code": self.__response_code,
            "message": self.__message
        }