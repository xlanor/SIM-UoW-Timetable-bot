#!/usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, 200

def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(HelloWorld, '/')
    return app


application = create_app()

if __name__ == '__main__':
    application.run(debug=True)