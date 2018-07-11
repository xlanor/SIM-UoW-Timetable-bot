# Changelog will begin from version 2.

## This will currently keep a log of the refactoring as it goes along.

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