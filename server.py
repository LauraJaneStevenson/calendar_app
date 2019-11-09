
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Calendar, Event

from helper_functions import get_user



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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)























