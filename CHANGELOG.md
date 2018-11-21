## Current Version: 2.0.2 beta 1 - Hera

>  *Gone but not forgotten:*
>  
>  ~~*1.4.0* - Styx~~
>
>  ~~*1.3.0* - Eris~~
>  
>  ~~*1.2.0* - Rhea~~
>  
>  ~~*1.1.0* - Prometheus~~
>  
>  ~~*1.0.0* - Cronus~~

<hr>

### Bump in major from 1.x.x to 2.x.x

* The entire backend has been rewritten for this major bump.
* There are some significant changes to the back-end and logical processes. End users may only notice a front-end change.
  * Noticeably, where the scraping used to be handled by the bot directly, this resulted in issues when high sign-up volumes were encountered. As a result, **celery** was used to handle the jobs instead. This ensures that the bot will not freeze during the scraping progress.
  * As such, it can be right to say that this bot runs with two seperate applications entirely, one application handles the bot while the other handles the job queue delegation.
  * The entire ripper has been written to reduce code. In total, I estimate that about 50% of code was reduced.
  * The entire configuration now acts as a singleton class because it is kind of redundant to keep instantiating a new instance everytime I want to use a variable.
  * Instead of opening and closing connections, PyMongo's connection pool is utilised instead to recycle connections.
  * The entire server has been moved to a Netherlands instance. This means that the response from users to the bot API takes significantly lesser latency (200ms down to 1ms), but the downside is that the scraping takes a longer time.
  * The entire codebase was repartitioned to make it easier to maintain in future.
  * Some fields in the database were renamed to make more sense.
  * Some additional fields were computed at scraping time instead of at retrival time.
  * The majority of the other changes are with the system design and should not ultimately affect the end users.

<hr>

## CHANGELOG

### v2.2.0 (2018-11-03)
* Fixes UoB timetables
* Added /today

### v2.1.0 (2018-10-25)
* Added /fuck 

### v2.0.2-b1 (2018-10-02)
* Update not returning a proper message may leave users confused and assuming that the bot has hanged. This was fixed.
* Chromedriver depreciated options were updated (selenium parameters)
* Markdown sanitising was added to sanitise class text in the unlikely event that 

### v2.0.1-b1 (2018-09-25)
* Minor bugfixes.
* Fixed an issue whereby the last_synced_datetime was both timezone naive and did not update properly.

### v2.0.0-b1 (2018-09-22)
* Initial open beta.
* Added a counter to the megaphone so that I can tell how many users received the message.

<hr>

## Rewrite Changelog

This is the old changelog used during the rewrite process.

### 2018-09-18 - 2018-09-19
* Various bug fixes and exception handlers added.
* Began beta testing

<hr>

### 2018-09-17
* Renamed repos. Added counter for megaphones.

### 2018-09-17
* Added /timetable and the relevant callbacks for scrolling.

<hr>

### 2018-09-13 - 2018-09-16
* Several changes were made to mongodb structure.
* Namedly, additional fields were add in to store the date and time,class_name is now known as class_list
* Finished delegation of entire scraping procedure to celery.
* Both update, forget, and register are now completed.
* Added redis to prepare for potential future caching. We will see how it goes.
* For now, we use redis mainly to check if a user already has a queue job running
* Will begin work on a) concurrency and b) displaying the timetable.

<hr>

### 2018-09-10
* Begin writing the telegram bot skeleton.
* Setup nginx configuration in favour of a webhook model over long polling.
* Integrated a new ![Message Queue](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits) feature from PTB
* Redesigned configuration file.
* Migrated server to NL server for better response times with telegram api (situated in NL)
```
(venv) jingkai@ubuntu-bionic:/projects/timetable_v2/src$ ping -c 5 api.telegram.org
PING api.telegram.org (149.154.xxx.xx) 56(84) bytes of data.
64 bytes from 149.154.xxx.xx (149.154.xxx.xx): icmp_seq=1 ttl=59 time=1.11 ms
64 bytes from 149.154.xxx.xx (149.154.xxx.xx): icmp_seq=2 ttl=59 time=1.14 ms
64 bytes from 149.154.xxx.xx (149.154.xxx.xx): icmp_seq=3 ttl=59 time=0.978 ms
64 bytes from 149.154.xxx.xx (149.154.xxx.xx): icmp_seq=4 ttl=59 time=1.15 ms
64 bytes from 149.154.xxx.xx (149.154.xxx.xx): icmp_seq=5 ttl=59 time=1.09 ms

--- api.telegram.org ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 0.978/1.096/1.153/0.062 ms
```
* Will begin integrating mongoDB and rewriting some other methods next week

<hr>

### 2018-07-18
* Rewrote entire class model to allow it to be reusable from other class and individual class.
* Rewrote unit tests to handle for the new ripper
* Deleted old and redundant classes.

<hr>

### 2018-07-17
* Began refactoring TimeTable ripper code to enable class compatibility with Other Timetable
* Removed many redundant methods and signifcantly neatened the parsing code
* Added a formatting decorator for time.
* Fixed an error whereby original re-written regex query would not retrive classes if the users had more than 100 classes
* \d{1,2}$ to 1,3 . Pretty simple.
* Begin upgrading ripper code to modern python
* Removing all "{}".format(text) instances and replacing with f-strings
* Adding type-hinting for funcs.
* Adding docstrings

<hr>

### 2018-07-13
* Wrote some code for Other Timetable (ie: IS)

<hr>

### 2018-07-12
* Started refactoring ripper
* Added some unit tests for ripper.

<hr>

### 2018-07-11
* Deprecated PhantomJS in favour of headless chrome.
* Theoretical code for attendance module. Untested.
* Added unit tests for class structure.
* Added base travis integration.

<hr>

### 2018-06-12
* Began refactoring the most basic portion - the ripper script.
* Started following OOP Principles more strictly.
* Instead of duplicating redundant code, inheritance was incorporated into the ripper script to allow testlogin and riptimetable to share the same code.
* Moved the retrieved classes into an object. An array of retrived class objects should now be a response.
* Switched string true/false to boolean true/false (What the fuck was I even thinking?)