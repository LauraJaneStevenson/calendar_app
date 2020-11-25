 
Roomies
=======

Summary
-------

Roomies is a shared calendar web app that makes scheduling events between housemates simple and convenient. The app ensures that certain events only appear on the calendar once agreed upon by all housemates. Users can opt to receive notifications via text message and approve or deny events with one letter responses or simply respond to event requests in the browser. The app helps users avoid scheduling noisy events at the same time as quiet hours and allows users to reserve time slots in shared bathrooms. Roomies also protects user's calendars from being seen by strangers. Any user seeking access to a calendar must first be invited by an existing user of that calendar.

About the Developer
-------------------

Roomies was created by Laura Stevenson. Learn more about her at [LinkedIn](https://www.linkedin.com/in/laura-stevenson-design)

Technologies
------------

#### Tech Stack
* Python
* Flask
* Jinja2
* SQLAlchemy
* HTML
* CSS
* Javascript
* JQuery
* Bootstrap
* Moment.js
* FullCalendar.io
* Datetime modeule in python
* Twilio SMS API

Pages
-----

#### Creating and Editing an Event
![Creating and editing events](http://g.recordit.co/CrIM2ykBvE.gif)

#### Event Requests
![Event Requests](http://g.recordit.co/7Jcn16FLPR.gif)

<!-- #### User Profiles

![Profile and event pages](https://recordit.co/fu7vnCW9m0)
 -->
#### Search For Users

![Search for Users](http://g.recordit.co/pW8UKEmGw1.gif)

#### Search For Calendars

![Search for Calendars](http://g.recordit.co/uxrbYQtvIT.gif)


Setup/Installation
-----

#### Requirements:

* PostgresSQL
* Python 3.6
* Twilio API key

To run this app on your local computer, please follow these steps:

Clone repository:

```
$ git clone https://github.com/LauraJaneStevenson/calendar_app.git
```

Create a virtual environment:

```
$ virtualenv env
```

Activate the virtual environment: 

```
$ source env/bin/activate
```

Install dependencies:

```
$ pip3 install -r requirements.txt
```

Create your own secret keys for Twilio and save them to a secrets.sh file. Your file should look like this:

```
export ACCOUNT_SID=''
export AUTH_TOKEN=''
export SMS_NUMBER=''
export SMS_TO=''
```

Create database:

```
$ createdb calendars
```

Create tables:

```
$ python3 -i model.py

>>> db.create_all()
```

Run app from command line:

```
$ python3 server.py
```


