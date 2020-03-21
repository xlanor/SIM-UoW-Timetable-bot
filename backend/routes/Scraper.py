#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from .Templates.error_template import ErrorTemplate



class Scraper(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return ErrorTemplate(400, 'no data received')

