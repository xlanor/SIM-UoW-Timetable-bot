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
# Runs a seperate instance of a celery application.
# This allows PTB component to transmit data over.
##
from celery import Celery
from celery import current_app

app = Celery(
    "queue", broker="amqp://", backend="rpc://", include=["Controllers.celery_queue"]
)

if __name__ == "__main__":
    app.start()
    all_task_names = current_app.tasks.keys()
    all_tasks = current_app.tasks.values()
    print(all_task_names)
