from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    jsonify
)

from config import PASSWORD

from services.google_sheets import (
    get_events,
    get_leaders,
    get_helpers,
    get_event,
    update_event
)

app = Flask(__name__)
app.secret_key = "icafe_secret_key"


# -------------------------------------------------
# Login Page
# -------------------------------------------------

@app.route("/")
def login():
    return render_template("login.html")


# -------------------------------------------------
# Login Validation
# -------------------------------------------------

@app.route("/login", methods=["POST"])
def do_login():

    name = request.form["name"].strip()
    password = request.form["password"]

    leaders = get_leaders()

    if name in leaders and password == PASSWORD:

        session["leader"] = name

        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid name or password."
    )


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if "leader" not in session:
        return redirect(url_for("login"))

    events = get_events()

    return render_template(
        "dashboard.html",
        leader=session["leader"],
        events=events
    )


# -------------------------------------------------
# Logout
# -------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -------------------------------------------------
# Test Google Form Responses
# -------------------------------------------------

@app.route("/test_helpers")
def test_helpers():

    helpers = get_helpers()

    return jsonify(helpers)


# -------------------------------------------------

@app.route("/save_event/<int:event_id>", methods=["POST"])
def save_event(event_id):

    mc = request.form["mc"]
    
    devotion = request.form["devotion"]
    food = request.form["food"]

    update_event(
        event_id,
        mc,
        
        devotion,
        food
    )

    return redirect(url_for("dashboard"))

@app.route("/edit/<int:event_id>")
def edit_event(event_id):

    if "leader" not in session:
        return redirect(url_for("login"))

    event = get_event(event_id)

    leaders = get_leaders()

    return render_template(
        "edit_event.html",
        event=event,
        leaders=leaders
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)