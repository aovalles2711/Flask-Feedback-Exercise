"""Flask Feedback app."""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db. db. User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.congif['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.congif['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.configp['DEBUG_TB_INTERCENT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """Homepage."""

    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user with form and handle submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.userame}")
    
    else:
        return redirect("users/register.html", form=form)

@app.route('/login', method=['GET', 'POST'])
def login():
    """Login form."""

    if "username" in session:
        return redirect(f"/users.{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username and/or password."]
            return render_template("users/login.html", form=form)
    
    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """Logged-in example."""

    if "username" not in session or username != session ['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login page."""

    if "username" not in session or username != session ['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and handle submission."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/new.html", form=form)
    
@app.route("/feedback/<int:feedback_id</update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and handle submission."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.cotent = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedack(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")