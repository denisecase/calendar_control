# Google Calendar Control

Add week events to Google Calendar at the start of a new semester (from the command line). 

## Setup

Install Python 2.6 or greater.  See instructions for setting up environment variables and path.

Install pip for Python package management.

Follow the instructions to set up access to your Google calendar from your local Python app.

Set the options:

* showcolors = False
* addRepeating = False
* addIndividual = True

Set associated variables (see file).

When pulling dates, some times may have invalid characters - clean up csv data files before running. 


## Resources
 
* [Git for Windows](https://msysgit.github.io/) 
* [Python](https://www.python.org/downloads/)
* [Google Developers Google Calendar API Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python)
* [What does if main do?](http://stackoverflow.com/questions/419163/what-does-if-name-main-do)
* [List of time zone options](http://stackoverflow.com/questions/22526635/list-of-acceptable-google-calendar-api-time-zones)
*  [How to delete stored credentials](http://stackoverflow.com/questions/30293293/insufficient-permissions-on-google-calendar-apis-acl-list/30675031#30675031)
* [Northwest Missouri State University Academic Calendar](http://www.nwmissouri.edu/academics/calendar.htm)

## Getting started (on Windows)

Clone the repo.

```
pip install httplib2
pip install apiclient
pip install --upgrade google-api-python-client
```

Edit the semester start year, month, day.
Edit the number of weeks in the semester.


```
python calendar_control.py
```







