
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Calendar, Event, EventRequest

from helper_functions import get_user, get_approved_events, map_event_colors, get_notifications



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123"

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")

@app.route("/register")
def register_page():
    """Show registration page."""

    return render_template("register.html")

@app.route("/add_user", methods=['POST'])
def register_user():
    """Add a user to the database."""
 
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
   
    
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
    # print()
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

    user = User.query.filter_by(user_id=user_id).first()

    user.cal_id = session['cal_id']

    db.session.commit()

    return redirect("/")

@app.route("/find_calendar")
def find_calendar():
    """Takes in a house_name string and finds a list of 
    calendars with that name"""

    # get calendar name user entered in form 
    house_name = request.args.get("house_name")

    # list of calendars with the house name user searched for
    cal_list = Calendar.query.filter(Calendar.house_name == house_name).all()
    
    return render_template("calendar_list.html",cal_list=cal_list)


@app.route("/add_self_to_cal",methods=['POST'])
def add_self_to_cal():
    """Adds cal_id to logged in user's cal_id feild."""
    cal_id = request.form['cal_id']
    user = User.query.filter(User.user_id == session['user_id']).one()
    user.cal_id = cal_id

    db.session.commit()

    return render_template("calendar.html",user=user)

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























