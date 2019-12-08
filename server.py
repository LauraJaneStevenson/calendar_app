
from jinja2 import StrictUndefined

from flask import Flask, send_from_directory, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from twilio.rest import Client

from twilio.twiml.messaging_response import MessagingResponse

from model import connect_to_db, db, User, Calendar, Event, EventRequest, AccessRequest, Invitation, Notification

from helper_functions import get_user, get_event, get_invitation, get_access_request, get_approved_events, map_event_colors, get_notifications, send_init_sms, get_event_request, get_calendar

import os

import random

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123"

@app.route("/")
def homepage():
    """Show homepage."""


    return render_template("homepage.html")


# @app.route('/static/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

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

    # query for user
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
    # session["housemates"] = user.get_housemates()
    flash(f"Hello, {user.name}")

    # if user has a calendar  
    if user.calendar:

        # create calendar var and add calendar id to session
        calendar = user.calendar
        session["cal_id"] = calendar.cal_id
        
    return redirect("/calendar")

   
    # return render_template("find_or_create_cal.html") 

@app.route("/calendar")
def show_calendar():
    """Renders calendar page if user has calendar, else, Renders find-or-create-cal """
    if get_user(session['user_id']).cal_id != None:
      
        return render_template("calendar.html",user=get_user(session['user_id']))

    return render_template("create_cal.html",user=get_user(session['user_id']))

@app.route("/profile/<user_id>")
def user_profile(user_id):
    """Renders user profile page"""

    # get user to pass through to html
    user = get_user(user_id)

    # check if user has a calendar to determine what to send to html
    if user.cal_id:

        house_name = "In house: " + get_calendar(user.cal_id).house_name

    else:

        house_name = "No House"

    # list of events to display on profile page
    events = Event.query.filter_by(user_id=user.user_id,event_type='party').all()

    if not events and user.cal_id:
        # if user hasn't created any events, display events on calendar
        events = Event.query.filter_by(cal_id=user.cal_id,event_type='party').all()

    events.reverse()

    return render_template("profile.html",user=user,house_name=house_name,my_user=get_user(session['user_id']),events=events)

@app.route("/edit_profile")
def edit_profile():

    return render_template("edit-profile.html",user=get_user(session['user_id']))

@app.route('/upload_file', methods=['POST'])
def upload_file():

    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # print("\n\n\n\n\n\n")
    # print(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # print("\n\n\n\n\n\n")
    get_user(session['user_id']).profile_pic = '/' + UPLOAD_FOLDER + file.filename
    db.session.commit()

    # new_file = FileContents(name=file.filename,data=file.read())
    # db.session.add(new_file)
    # db.session.commit()
    # return f"Saved {file.filename} to the Database"
    return redirect(f"/profile/{session['user_id']}")

@app.route('/upload_party_pic/<event_id>', methods=['POST'])
def upload_party_img(event_id):

    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # print("\n\n\n\n\n\n")
    # print(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    # print("\n\n\n\n\n\n")
    get_event(event_id).image = '/' + UPLOAD_FOLDER + file.filename
    db.session.commit()

    # new_file = FileContents(name=file.filename,data=file.read())
    # db.session.add(new_file)
    # db.session.commit()
    # return f"Saved {file.filename} to the Database"
    return redirect(f"/edit_party/{event_id}")


@app.route("/get_notifications.json")
def user_notifications():
    """Retruns all the notifications for loggedin user"""

    notifications = get_notifications(session['user_id'])

    notif_list = []

    for notification in notifications:
        notif_dict = {}
        notif_dict['id'] = notification.notification_id
        notif_dict['type'] = notification.notification_type

        # first get the type then depending on the type set its foreign key
        if notification.notification_type == 'event request':
            notif_dict['event_id'] = notification.event_id

            # get creator of event's username to make 'from_user' key
            from_user_id = get_event(notification.event_id).user_id
            notif_dict['from'] = get_user(from_user_id).username

            # get start and end times of event

            notif_dict['start'] = get_event(notification.event_id).start_time.strftime('Starting on %m/%d at %I:%M:%p')
            notif_dict['end'] = get_event(notification.event_id).end_time.strftime(' until %m/%d at %I:%M:%p')
            notif_dict['event_type'] = get_event(notification.event_id).event_type 

        elif notification.notification_type == 'access request':
            notif_dict['request_id'] = notification.request_id

            # get user requesting access username to make 'from_user' key
            from_user_id = get_access_request(notification.request_id).from_user_id
            notif_dict['from'] = get_user(from_user_id).username

        else:
            notif_dict['invite_id'] = notification.invite_id
            # create key calue pair for house name 
            cal_id = get_invitation(notification.invite_id).from_cal_id
            notif_dict['from'] = get_calendar(cal_id).house_name
        
        notif_list.append(notif_dict)

    # print("\n\n\n\n\n\n\n")
    # print("jsonify notification list",notif_list)
    # print("\n\n\n\n\n\n\n")
    return jsonify(notif_list)


@app.route("/handle_notif_response", methods=['POST'])
def handle_notif_response():
    
    # query for the correct notification object with notif_id passed in
    notification = Notification.query.filter_by(notification_id=request.form.get('id')).one()

    # set notif to seen commit to DB
    notification.seen = True
    db.session.commit()

    approved = request.form.get('approved')

    # check if user clicked approve or deny
    if approved == 'true':
        # check what type of notification it is 
        if notification.notification_type == 'access request':

            # set access request to approved 
            access_req = get_access_request(notification.request_id)
            access_req.approved = True

            # set user's calendar to 
            get_user(access_req.from_user_id).cal_id = access_req.to_cal_id

            # commit to DB
            db.session.commit()

            # flash message to user
            return f"You've granted {access_req.from_user.name} access to {get_calendar(session['cal_id']).house_name}"

        elif notification.notification_type == 'invitation':

            # set invitation to accepted 
            invitation = get_invitation(notification.invite_id)
            invitation.accepted = True

            # set current users calendar to calendar that invited them
            get_user(session['user_id']).cal_id = invitation.from_cal_id
            session['cal_id'] = invitation.from_cal_id
           
            # commit tp DB
            db.session.commit()

            # house_naem var for reponse message
            house_name = get_calendar(invitation.from_cal_id).house_name

            # flash message to user
            return f"You've accepted the invitation from the house {house_name}!"

        elif notification.notification_type == 'event request':

            event = get_event(notification.event_id)

            # query for event request with event id and are intended for the current user
            event_request = EventRequest.query.filter_by(event_id=event.event_id,to_user_id=session['user_id']).one()

            # set event request to approved 
            event_request.approved = True

            # commit to DB
            db.session.commit()

            return f"You've approved the event {event.event_type}!"     

    return f"You've denied this notification"


# @app.route("/notif_hover/<notif_id>")
# def get_proposed():
#     """Returns a json object of a single event"""
#     get_event()

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
    return render_template("create_cal.html",user=get_user(session['user_id']))


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
    
    return render_template("find_housemates.html", users=users,user=get_user(session['user_id']))

@app.route("/invite", methods=['POST'])
def invite_housemates():

    user_id = request.form["user_id"]
    invited_user = get_user(user_id).name

    # check to see if an invitation to this person already exists
    # first query for other invitations 
    invitations = Invitation.query.filter_by(from_cal_id=session['cal_id'],
                                             to_user_id=user_id).all()
    if not invitations:
        # create an invitation object 
        invitation = Invitation(from_cal_id=session['cal_id'],
                                to_user_id=user_id)
        

        # add and commit invitation to DB
        db.session.add(invitation)
        db.session.commit()

        # create a notification object
        notification = Notification(invite_id=invitation.invite_id,
                                    notification_type='invitation',
                                    to_user_id=user_id)
        # add and commit notification to DB
        db.session.add(notification)
        db.session.commit()

        # flash a success message to user
        return f"A notification has been sent to {invited_user}"

    # flash this message if invitation to this user already been sent 
    return f"An invitation from this calendar has already been sent to {invited_user}."

@app.route("/find_calendar")
def find_calendar():
    """Takes in a house_name string and finds a list of 
    calendars with that name"""

    # get calendar name user entered in form 
    house_name = request.args.get("house_name")

    # list of calendars with the house name user searched for
    cal_list = Calendar.query.filter(Calendar.house_name == house_name).all()

    # 

    cal_imgs = ['cal1.jpg','cal2.jpg','cal3.jpg','cal4.jpg']
    random.sample(cal_imgs,4)


    print("\n\n\n\n\n\n\n\n\n\n\n")
    print(cal_list)
    print("\n\n\n\n\n\n\n\n\n\n\n")

    return render_template("calendar_list.html",cal_list=cal_list,user=get_user(session['user_id']),cal_imgs=cal_imgs)


@app.route("/request_access_to_cal",methods=['POST'])
def request_access_to_cal():
    """Creates an access_request obj and many notification 
    objs for each user of cal"""

    cal_id = request.form['cal_id']
    user = get_user(session['user_id'])

    # check to see if an access_request from this user to this calendar exists
    # first query for existing access_requests 
    requests = AccessRequest.query.filter_by(to_cal_id=cal_id,
                                   from_user_id=user.user_id).all()

    # if there aren't any make new request and notification objects
    if not requests:

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

        # this message will be flashed to user 
        return f"You have requested access to {get_calendar(cal_id).house_name}"

    return f"You have already requested access to {get_calendar(cal_id).house_name}"

@app.route("/add_event", methods=['POST'])
def add_event():
    """Adds event to the database and send housemates event requests if applicable"""

    # get event info from form 
    start = request.form.get("start")
    end = request.form.get("end")
    event_type = request.form.get("eventType")
    title = request.form.get("title")
    description = request.form.get("description")
    # create new event
    event = Event(cal_id=session['cal_id'],user_id=session['user_id'],
                  event_type=event_type,start_time=start,end_time=end,
                  title=title,description=description)
    # commit it to the DB
    db.session.add(event)
    db.session.commit()

    # add a url to parties so users can click on events and visit party page
    if event_type == 'party':
        event.url = "http://localhost:5000/party/" + str(event.event_id)
        db.session.commit()

    if event_type == 'shower':
        # showers are first come first serve so approved gets set to true
        event.approved == True
        db.session.commit()
        return "Shower event has been added to calendar!"


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
        # create a notification object
        notification = Notification(notification_type='event request',event_id=event.event_id,
                                    to_user_id=housemate.user_id)
        db.session.add(notification)
        db.session.commit()

    event_info = {}
    event_info['url'] = event.url
    event_info['author'] = get_user(session['user_id']).username
   
    return jsonify(event_info)

@app.route("/party/<event_id>")
def show_party_deets(event_id):
    """Renders a party event detail page"""

    party = get_event(event_id)
    start = party.start_time.strftime('Starting on %m/%d at %I:%M:%p')
    end = party.end_time.strftime(' until %m/%d at %I:%M:%p')

    return render_template("party.html",party=party,start=start,end=end,user=get_user(session['user_id']))

@app.route("/edit_party/<event_id>")
def edit_party_deets(event_id):

    party = get_event(event_id)
    start = party.start_time.strftime('Starting on %m/%d at %I:%M:%p')
    end = party.end_time.strftime(' until %m/%d at %I:%M:%p')

    return render_template("edit_party.html", party=party,user=get_user(session['user_id']))


    
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
        if db_event.event_type == 'party':
            event['title'] = db_event.title
        else:
            event['title'] = db_event.event_type
        event['start'] = db_event.start_time.isoformat()
        event['end'] = db_event.end_time.isoformat()
        event['author'] = get_user(db_event.user_id).username
        event['url'] = db_event.url
        # if db_event.event_type
        # if the event is in the dictionary, give event obj 'eventColor' attibute 
        # and set it to correct color
        if db_event.event_type in map_event_colors():
            event['backgroundColor'] = map_event_colors()[db_event.event_type]
            event['borderColor'] = map_event_colors()[db_event.event_type]

        event_list.append(event)

    return jsonify(event_list)

@app.route("/single_evt_info")
def get_event_info():

    event = request.form.get("event_id")

    return event

@app.route("/event_req_notif.json")
def display_event_request():
    """Returns a single event object"""

    notif_id = request.args.get('id')

    notif = Notification.query.filter_by(notification_id=notif_id).one() 

    if notif.notification_type != 'event request':

        # pass
        return None

    event = get_event(notif.event_id)
    print("\n\n\n\n\n\n\n")
    print(event.start_time)
    print("\n\n\n\n\n\n\n")

    evt_dict = {}

    evt_dict['title'] = event.event_type
    evt_dict['start'] = event.start_time
    evt_dict['end'] = event.end_time
    evt_dict['author'] = get_user(event.user_id).username
    evt_dict['backgroundColor'] = '#71eeb8'

    return jsonify(evt_dict)

@app.route("/edit_event_des/<event_id>",methods=['POST'])
def edit_event(event_id):

    print("\n\n\n\n\n\n\n\n")
    print(request.form.get('event_des'))
    print("\n\n\n\n\n\n")

    get_event(event_id).description = request.form.get('event_des')
    db.session.commit()

    return redirect(f"/party/{event_id}")



@app.route("/unapproved_events.json")
def my_req_evts():

    events = Event.query.filter_by(user_id=session['user_id'],approved=False).all()

    event_list = []
    
    for event in events:
        # event_list.append({'title': event.event_type,
        #                    'start': event.start_time,
        #                    'end': event.end_time})
        event_dict = {}
        # event['id'] = db_event.event_id
        event_dict['title'] = event.event_type
        event_dict['id'] = event.event_id
        event_dict['start'] = event.start_time.isoformat()
        event_dict['end'] = event.end_time.isoformat()
        event_dict['author'] = get_user(event.user_id).username
        event_dict['url'] = event.url
        event_dict['backgroundColor'] = '#DCB239'

        event_list.append(event_dict)
    
    return jsonify(event_list)
    # return f"my requested events"

@app.route("/hm_evt_req.json")
def hm_evt_req():

    events = []

    for housemate in get_user(session['user_id']).housemates:

        events.extend(Event.query.filter_by(user_id=housemate.user_id,approved=False).all())

    event_list = []
    
    for event in events:
        # event_list.append({'title': event.event_type,
        #                    'start': event.start_time,
        #                    'end': event.end_time})
        event_dict = {}
        # event['id'] = db_event.event_id
        event_dict['title'] = event.event_type
        event_dict['id'] = event.event_id
        event_dict['start'] = event.start_time.isoformat()
        event_dict['end'] = event.end_time.isoformat()
        event_dict['author'] = get_user(event.user_id).username
        event_dict['backgroundColor'] = '#71eeb8'

        event_list.append(event_dict)
    
    return jsonify(event_list)
    # return f"my requested events"





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)























