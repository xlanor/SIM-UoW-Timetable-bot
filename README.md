## IN PROGRESS  [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Build Status](https://travis-ci.com/xlanor/SIM-UoW-Timetable-bot.svg?branch=master)](https://travis-ci.com/xlanor/SIM-UoW-Timetable-bot-v2)


Refactored version of the current SIM Timetable bot.

Development is still in progress. v1 is still up.

v2.0.0
Author - xlanor

# Disclaimer
* This bot is an unofficial bot which is not being developed with any support from the SIMConnect team.
* I have attempted to go through official channels to get some form of support to no avail.
* As such, please understand that it may not work smoothly.
* For current status of the rewrite, please look at the [changelog](https://github.com/xlanor/SIM-UoW-Timetable-bot/blob/master/CHANGELOG.md)

# Current Rewrite Progress

* :no_entry_sign: = Not done
* :heavy_check_mark: = Done

| SIMConnect Ripper Module       | status             |
| ------------------------------ | ------------------ |
| Login                          | :heavy_check_mark: |
| Attendance                     | :no_entry_sign:    |
| Timetable                      | :heavy_check_mark: |
| Other Classes (ie: IS)         | :heavy_check_mark: |


| Telegram Component             | status             |
| ------------------------------ | ------------------ |
| Chatbot component (Sign up)    | :heavy_check_mark: |
| Timetable Initial call         | :heavy_check_mark: |
| Timetable callback navigation  | :heavy_check_mark: |
| Alert system                   | :no_entry_sign:    |
| Mega system                    | :no_entry_sign:    |


| Dev Component                  | status             |
| ------------------------------ | ------------------ |
| Definition of Holding Models   | :heavy_check_mark: |
| Database redesign              | :heavy_check_mark: |
| Proper partitioning            | :heavy_check_mark: |
| Open Github issue on exception | :no_entry_sign:    |
| Task management with Celery    | :heavy_check_mark: |
| Server Migration               | :heavy_check_mark: |
| Integration of MQ feature      | :heavy_check_mark: | ( Initial testing )
| Redesign of configuration file | :heavy_check_mark: |

# Special thanks
Authors of all libraries / modules used in the development of this bot, in no particular order:
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) - the most readable framework for the telegram bot API .
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - best HTML parser
* [Selenium](https://pypi.org/project/selenium/) - making headless navigation easy
* [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) - Chromedriver and chromium authors.
* [SIMConnect](https://simconnect.simge.edu.sg/) - For not providing native API methods
* [Celery](https://github.com/celery/celery)
* [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server)
* [Redis](https://github.com/antirez/redis)
* Anybody else I missed
