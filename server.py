
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
