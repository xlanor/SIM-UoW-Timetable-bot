<h1 align="center">SIM-UoW Timetable Bot 2.0.0 beta 1: Hera </h1> 

<div align="center">

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![pythonver](https://img.shields.io/badge/python-3.6%2B-ff69b4.svg)](https://www.python.org/) [![Build Status](https://travis-ci.com/xlanor/SIM-UoW-Timetable-bot.svg?branch=master)](https://travis-ci.com/xlanor/SIM-UoW-Timetable-bot-v2)

</div>

A telegram bot for ripping timetables from SIM Connect built in python3

This bot is **not** an official bot sanctioned by either the University of Wollongong or the Singapore Institute of Management.

Please read the [Disclaimer](DISCLAIMER.md) before proceeding.

<hr>


### Why?

![Why?](https://i.imgur.com/7b3GTNU.png "Why?")

And also to familarize myself with mongoDB

<hr>

### Supported
* SIM-UoW Timetables.
* SIM-UB Timetables.
* IS Timetables **BETA**

>  In theory, all other timetables should work as long as they are on SIMConnect.
>  Without an account to test, I cannot officially support them.

When I say "Supported", unless explictly stated like IS timetables, this does not work with any timetables other than your regular module timetables.

This **DOES NOT** support the following:
* Exam Timetables
* Any classes with TBA time.

**I DO NOT STORE YOUR PASSWORDS IN PLAINTEXT. AS SUCH, I CANNOT MAGICALY UPDATE IT FOR YOU. YOU NEED TO DO A /update EVERYTIME YOUR TIMETABLE CHANGES!!!!!!!!!**


<hr>

### Commands

* **/register**
>  Registers your details with the bot.

* **/timetable**

>  Retrieves your timetable from the stored database.

* **/forget**

>  Removes your details from the stored database.

* **/update**

>  Re-scrapes the timetable from SIMConnect

* **/alert**

>  Toggle for the morning alert.

* **/nightly**

>  Toggle for the nightly alert
<hr>

### Running your own instance

Read the [Wiki](https://github.com/xlanor/SIM-UoW-Timetable-bot/wiki/Running-your-own-instance.) article for more.

You should have some experience in deploying applications in a linux environment before you attempt this.

<hr>

### Encryption

**I strongly encourage users to run their own instance of this bot instead of relying on the one I'm hosting.**

However, if you're using the instance that I am hosting, please read the following sentence

Although you are asked to enter your login credentials, At no point of time whatsoever does the bot store your password **in plaintext** to the database.

The bot encrypts your password with a key of your choice with AES-256 and requires the key to decrypt the password each time it syncs. The module can be found under modules/encryption.py

The stored password is the **encrypted text**. The key is kept by **you**. This is why you will need to enter the key each time to decrypt it on sync.

You are free to audit the source code.

You should take note that this is not the most secure method, but is the most convenient method for users.

As such, I strongly reccomend that you do not reuse your SIM Connect password anywhere else should you use this instance.

I am not responsible for any damages incurred from the usage of this bot.

<hr>

### Licensing

The bot is licensed under the [GNU Affero General Public License v3](LICENSE).

All derivatives works not intended for personal use must be released into the public domain for the sake of transparency

Derivatives works which are intended for personal use, but if hosted on a live server, may be used by others, even against the intentions of the owner of that particular instance, are not considered as "intended for personal use" and **must** be released into the public domain

If you wish to host a current instance of the bot for personal usage, you **must** modify the source code to prevent usage by any persons other than yourself.

If you wish to host a current instance of the bot but are not willing to modify the source code, you must run the current version of the source code at all times, and explicitly link to this source code.

The stipulated conditions above are due to the sensitive nature of the data that the bot is handling. Users of any instance must at all times be aware of the sensitive nature of the data and the measures that are being taken to protect against said data falling into the hands of any unknown persons. 

<hr>

### F.A.Q

* **What is a "Application Key?"**

>  Like the name suggests, a key is used to unlock a lock. In this case, a key is used to unlock the encrypted password. It can be any alphanumeric string you want.

* **But you're stealing my passwords!**

>  Read above section regarding encryption and **running your own local instance**

* **When do I need to sync? Do I sync it weekly?**

>  You only need to sync your timetable when theres an update to your timetable. ie: New semester, change of venue.
Other than that, the bot should detect the current day of the week and pull the entire week's timetable automatically with /timetable.
>
>  The flow of this program is as such:
>   `Register -> Update -> Rips timetable to Database -> Pull out with /timetable. `

* **Your bot sucks! It didnt tell me that I had a class and I missed it!**

>  Read the disclaimer, and notify me so that I can fix the bug.

* **I read the output wrongly and missed my class!**

> **User Problem.**

* **The bot is not responding! Why?!**

> 2.0.0+ takes advantages of the new MessageQueue class in PTB to enqueue messages to avoid breaching telegram's API limits.
> 
>Unfortunately, telegram API limits are enforced on a per bot, not a per user basis. Thus, this bot can only send/edit 30 messages a minute
>
> There are 2 solutions to this, only one of which is feasible
> * User can self host the bot
> * Donate to a bitcoin fund for me to raise enough money to buy over telegram and increase the API limits.

<hr>

### Current Rewrite Progress

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
| Alert system                   | :heavy_check_mark: |
| Mega system                    | :heavy_check_mark: |


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

<hr>

### Special thanks
Authors of all libraries / modules used in the development of this bot, in no particular order:
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) - the most readable framework for the telegram bot API .
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - best HTML parser
* [Selenium](https://pypi.org/project/selenium/) - making headless navigation easy
* [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) - Chromedriver and chromium authors.
* [Celery](https://github.com/celery/celery) - Task delegation. This is utilized during the timetable ripping
* [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server) - RabbitMQ is used as a message broker.
* [Redis](https://github.com/antirez/redis) - Experimenting with Redis as a in-memory data store for communication between celery and the bot.
* [Arrow](https://github.com/crsmithdev/arrow) - Arrow is ocassionally used in place of the date-time module. I will probably replace all of them soon, I'm just lazy.
* [jsonpickle](https://github.com/jsonpickle/jsonpickle) - jsonpickle is used to seralize the bot object that is then passed to celery, enabling communications to be maintained.
* [PyMongo](https://github.com/mongodb/mongo-python-driver) - PyMongo is objectively the best raw mongo connector, coming with a default connection pool enabled by default.
* [MongoDB](https://www.mongodb.com/) - mongoDB is used as the main database for this system, because I wanted to experiment with noSQL systems.

Last but not least,
* [SIMConnect](https://simconnect.simge.edu.sg/) - For not providing native API methods
* Anybody else I missed
