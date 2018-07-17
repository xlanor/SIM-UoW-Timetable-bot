# Changelog will begin from version 2.

## This will currently keep a log of the refactoring as it goes along.

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
