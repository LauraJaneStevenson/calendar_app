
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
        

        # a variable to store all other users who can also view that calendar
        housemates = User.query.filter_by(cal_id=calendar.cal_id).all()
        # print("\n\n\n\n\n\n")
        # print(housemates)
        # print(session)
        # print("\n\n\n\n\n\n")
       
        return render_template("calendar.html",housemates=housemates)

   
    return redirect("/create_or_find") 


@app.route("/create_or_find")
def create_or_find_cal():
    pass


@app.route("/calendar")
def calendar_page(): 

    return render_template("calendar.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)























