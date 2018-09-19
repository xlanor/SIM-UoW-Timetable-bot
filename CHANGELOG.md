Current Version: 
**2.0.0 beta 1 - Hera**
~~1.4.0 - Styx~~
~~1.3.0 - Eris~~
~~1.2.0 - Rhea~~
~~1.1.0 - Prometheus~~
~~1.0.0 - Cronus~~



### 2018-09-18 - 2018-09-19
* Various bug fixes and exception handlers added.
* Began beta testing

### 2018-09-17
* Added /timetable and the relevant callbacks for scrolling.

### 2018-09-13 - 2018-09-16
* Several changes were made to mongodb structure.
* Namedly, additional fields were add in to store the date and time,class_name is now known as class_list
* Finished delegation of entire scraping procedure to celery.
* Both update, forget, and register are now completed.
* Added redis to prepare for potential future caching. We will see how it goes.
* For now, we use redis mainly to check if a user already has a queue job running
* Will begin work on a) concurrency and b) displaying the timetable.

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

### 2018-07-18
* Rewrote entire class model to allow it to be reusable from other class and individual class.
* Rewrote unit tests to handle for the new ripper
* Deleted old and redundant classes.

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

### 2018-07-13
* Wrote some code for Other Timetable (ie: IS)

### 2018-07-12
* Started refactoring ripper
* Added some unit tests for ripper.

### 2018-07-11
* Deprecated PhantomJS in favour of headless chrome.
* Theoretical code for attendance module. Untested.
* Added unit tests for class structure.
* Added base travis integration.

### 2018-06-12
* Began refactoring the most basic portion - the ripper script.
* Started following OOP Principles more strictly.
* Instead of duplicating redundant code, inheritance was incorporated into the ripper script to allow testlogin and riptimetable to share the same code.
* Moved the retrieved classes into an object. An array of retrived class objects should now be a response.
* Switched string true/false to boolean true/false (What the fuck was I even thinking?)
