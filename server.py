
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from twilio.rest import Client

from twilio.twiml.messaging_response import MessagingResponse

from model import connect_to_db, db, User, Calendar, Event, EventRequest, AccessRequest, Invitation, Notification

from helper_functions import get_user, get_approved_events, map_event_colors, get_notifications, send_init_sms, get_event_request

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123"

@app.route("/")
def homepage():
    """Show homepage."""

    # test
    # send_init_sms( 97,1)

    return render_template("homepage.html")

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""

    # construct client object
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    # get message containing event info
    messages = client.messages.list(limit=2)
    # get indexes of where the event_id begins and ends 
    indx1 = messages[1].body.find("number") + 6
    indx2 = messages[1].body.find(",",indx1)

    # store request_id in a variable by slicing the string 
    request_id = messages[1].body[indx1:indx2]

    # get event_request object with request_id
    # event_request = get_event_request(request_id)

    print("\n\n\n\n\n\n")
    print(request_id)
    print("\n\n\n\n\n\n")

    # Get user's response
    user_resp = request.values.get('Body', None)

    # create a Messaging response obj
    app_resp = MessagingResponse()

    if user_resp != 'Y' and user_resp != 'N':
        # Add a message
        app_resp.message("Invalid Response.")

    if user_resp == 'Y':
        # set event.approved to true 
        get_event_request(request_id).approved = True
        db.session.commit()
        # print("\n\n\n\n\n\n")
        # print(get_event_request(request_id))
        # print("\n\n\n\n\n\n")
        app_resp.message("You have successfully approved this request!")
    elif user_resp == 'N':
        # set event.approved to true
        app_resp.message("You have successfully denied this request.")
       

    return str(app_resp)

@app.route("/register")
def register_page():
    """Show registration page."""

    return render_template("register.html")

@app.route("/add_user", methods=['POST'])
def register_user():
    """Add a user to the database."""
    
    # get info from form
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    # check if that username exists 

    # get all existing usernames
    existing_usernames = db.session.query(User.username).all()
    
    # check if username from frorm is already taken
    for existing_username in existing_usernames:
        
        if username == existing_username[0]:

            print("Sorry that user name is taken!")
            return redirect("/register")

    
    # if username not taken create new user object
    new_user = User(name=name,username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    flash(f"Hi {name}! Welcom to roomies!")
    return redirect("/")

  


@app.route("/login", methods=['POST'])
def login_proccess():

    # getting login info from form
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username,password=password).first()

    if user == None:
        flash("User does not exist, click register to join Roomies!")
        return redirect("/")
    if user.password != password: 
        flash("Incorrect password.")

    # add user_id to the session 
    session["user_id"] = user.user_id
    session["name"] = user.name
    session["username"] = user.username
    flash(f"Hello, {user.name}")

    # if user has a calendar  
    if user.calendar:

        # create calendar var and add calendar id to session
        calendar = user.calendar
        session["cal_id"] = calendar.cal_id
        
        return render_template("calendar.html",user=user)

   
    return render_template("find_or_create_cal.html") 

@app.route("/get_notifications.json")
def user_notifications():
    """Retruns all the notifications for loggedin user"""

    notifications = get_notifications(session['user_id'])

    notif_list = []

    for notification in notifications:
        notif_dict = {}
        notif_dict['id'] = notification.request_id
        notif_dict['event_id'] = notification.event_id
        notif_list.append(notif_dict)

    print("\n\n\n\n\n\n\n")
    print("jsonify notification list",notif_list)
    print("\n\n\n\n\n\n\n")
    return jsonify(notif_list)

@app.route("/logout_process")
def logout_user():
    """method for logging out user redirects to homepage"""

    # delete user info from session
    del session["user_id"]
    del session["name"]
    del session["username"]

    # if user has a calendar delete from session
    if "cal_id" in session:

        del session["cal_id"]

    return redirect("/")

@app.route("/create_cal")
def create_or_find_cal():
    """retuns the html page where user can create a new calendar object"""
    return render_template("create_cal.html")


@app.route("/create_cal_process", methods=['POST'])
def create_cal_process(): 
    """Creates a calendar object, binds it to user who created it,
        redirects to calendar.html"""

    house_name = request.form["house_name"]
    house_addr = request.form["house_addr"]

     # get all existing usernames
    existing_addrs = db.session.query(Calendar.house_addr).all()
    # check if username from frorm is already taken
    for address in existing_addrs:
        
        if house_addr == address[0]:

            print("Sorry there is already a calendar with that address!")
            return redirect("/create_cal")

    new_calendar = Calendar(house_name=house_name,house_addr=house_addr)
    user = get_user(session["user_id"])
    user.calendar = new_calendar
    db.session.add(new_calendar)
    db.session.commit()
    
    # get cal_id of newly created calendar and add it to the session
    session["cal_id"] = user.cal_id

    return render_template("/calendar.html",user=user)

@app.route("/add_housemates", methods=['POST'])
def add_housemates():
    """Display list of all users and their info with name from input search bar"""

    housemate = request.form['housemate_name']
    users = User.query.filter(User.name==housemate, User.cal_id == None).all()
    

    return render_template("find_housemates.html", users=users)


@app.route("/invite", methods=['POST'])
def invite_housemates():

    user_id = request.form["user_id"]

    # user = User.query.filter_by(user_id=user_id).first()

    # user.cal_id = session['cal_id']

    # db.session.commit()

    # create an invitation object 
    invitation = Invitation(from_cal_id=session['cal_id'],
                            to_user_id=user_id)
    # create a notification object
    notification = Notification(invite_id=invitation.invite_id,
                                notification_type='invitation')

    db.session.add(invitation,notification)
    db.session.commit()

    invited_user = get_user[user_id].name

    return f"A notification has been sent to {invited_user}"

@app.route("/find_calendar")
def find_calendar():
    """Takes in a house_name string and finds a list of 
    calendars with that name"""

    # get calendar name user entered in form 
    house_name = request.args.get("house_name")

    # list of calendars with the house name user searched for
    cal_list = Calendar.query.filter(Calendar.house_name == house_name).all()
    
    return render_template("calendar_list.html",cal_list=cal_list)


@app.route("/request_access_to_cal",methods=['POST'])
def request_access_to_cal():
    """Creates an access_request obj and many notification 
    objs for each user of cal"""

    cal_id = request.form['cal_id']
    user = get_user(session['user_id'])
    # create a new access_request and notification object
    access_request = AccessRequest(to_cal_id=cal_id,
                                   from_user_id=user.user_id)
    db.session.add(access_request)
    db.session.commit()
    
    
    # get list if all users currently on calendar that user is 
    # requesting acess to
    cal_users = get_calendar(cal_id).get_users()

    # loop over list and create a notification for each user
    for user in cal_users:
        # create new notification with access_request's id 
        notification = Notification(request_id=access_request.request_id,
                                    notification_type='access request',
                                    to_user_id=user.user_id)
        db.session.add(notification)
        db.session.commit()

    # user = User.query.filter(User.user_id == session['user_id']).one()
    # user.cal_id = cal_id

    # db.session.commit()

    # return render_template("calendar.html",user=user)

    # this message will be flashed to user 
    return f"You have requested access to {get_calendar(cal_id).house_name} "

@app.route("/add_event", methods=['POST'])
def add_event():
    """Adds event to the database and send housemates event requests if applicable"""

    # get event info from form 
    start = request.form.get("start")
    end = request.form.get("end")
    event_type = request.form.get("eventType")
    # create new event
    event = Event(cal_id=session['cal_id'],user_id=session['user_id'],
                  event_type=event_type,start_time=start,end_time=end)
    # commit it to the DB
    db.session.add(event)
    db.session.commit()

    if event_type == 'shower':
        # showers are first come first serve so approved gets set to true
        event.approved == True
        db.session.commit()

    else:
        # if event not shower, send event request to other users
        current_user = get_user(session['user_id'])
        # get list of current user's housemates
        housemates = current_user.get_housemates()
        # loop through housemates and send event request to each
        for housemate in housemates:
            event_request = EventRequest(event_id=event.event_id,
                                          to_user_id=housemate.user_id)
            db.session.add(event_request)
            db.session.commit()
            send_init_sms(event_request.request_id,housemate.user_id)


    return "An event request has been sent to your housemates!"
    
@app.route("/approved_events.json")
def display_all_events():
    """Returns a list of events from database"""

    # call helper function to get list of all event objects with this cal_id
    db_events = get_approved_events(session['cal_id'])

    # list of objects, each represent one event, to pass to calendar on front end
    event_list = []
    
    for db_event in db_events:
        # event_list.append({'title': event.event_type,
        #                    'start': event.start_time,
        #                    'end': event.end_time})
        event = {}
        # event['id'] = db_event.event_id
        event['title'] = db_event.event_type
        event['start'] = db_event.start_time.isoformat()
        event['end'] = db_event.end_time.isoformat()
        event['author'] = get_user(db_event.user_id).username
        # if the event is in the dictionary, give event obj 'eventColor' attibute 
        # and set it to correct color
        if db_event.event_type in map_event_colors():
            event['backgroundColor'] = map_event_colors()[db_event.event_type]
            event['borderColor'] = map_event_colors()[db_event.event_type]

        event_list.append(event)

    return jsonify(event_list)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)























