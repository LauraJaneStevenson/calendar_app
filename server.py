
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Calendar, Event



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

    # return render_template("register.html")


@app.route("/login", methods=['POST'])
def login_proccess():

    # getting login info from form
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    

    if user == None:
        flash("User does not exist, click register to join Roomies!")
        return redirect("/")
    if user.password != password: 
        flash("Incorrect password.")

    # add user_id to the session 
    session["user_id"] = user.user_id
    flash(f"Hello, {user.name}")


    # if user has a calendar  
    if user.calendar:

        # add calendar object to session
        # create calendar var 
        calendar = user.calendar
        session["cal_id"] = calendar.cal_id
        

        # a variable to store a list of user's housemates
        housemates = User.query.filter(User.user_id != user.user_id, 
                                       User.cal_id == calendar.cal_id).all()

        # add instance attribute housemates
        user.housemates = housemates

        return render_template("calendar.html",user=user)

   
    return render_template("find_or_create_cal.html") 

@app.route("/logout_process")
def logout_user():
    """method for logging out user redirects to homepage"""

    # delete user and calendar from session
    del session["user_id"]
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

    user = User.query.filter_by(user_id=session["user_id"]).first()
    user.calendar = new_calendar
    db.session.add(new_calendar)
    db.session.commit()


    return render_template("/calendar.html",user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)























