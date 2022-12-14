from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///user_feedback'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'secret-user-key'
app.config["DEBUG_TB_INTERCEPTS_REDIRECTS"] = False

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def render_home_page():
    """Display home page."""
    return render_template('index.html')
    # else:
    # username = session["username"]
      #  return render_template('index.html', username=username)

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register user: produce form and handle form submission."""

    if "username" in session:
        username = session["username"]
        return redirect(f'/users/{username}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.register(username, password, email, first_name, last_name)
        
        db.session.commit()
        flash(f"User {user.username} added!")
        session["username"] = user.username
        username = session["username"]

        return redirect(f'/users/{username}')
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Login user: produce form and handle form submission"""
    if "username" in session:
        username = session["username"]
        return redirect(f'/users/{username}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {user.username}!")
            session["username"] = user.username
            username = session["username"]
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ["Incorrect username/password"]
    
    return render_template("login.html", form=form)


@app.route('/logout')
def logout_user():
    """Logout user by popping from session and redirect to hompage"""
    session.pop("username")
    flash("Sucessfully logged out.")
    return redirect('/')


@app.route('/users/<username>', methods=["GET", "POST"])
def show_user_info(username):
    if "username" not in session or username != session["username"]:
        flash("Must be logged in to view page")
        return redirect('/login')
    else:
        user = User.query.get(username)
        return render_template("user-info.html", user=user)

@app.route('/users/<username>/delete')
def delete_user(username):
    """Delete user from session and database. Delete all feedback related to user."""
    if "username" not in session or username != session["username"]:

        flash("Must be logged in to delete account")
        return redirect(f'/users/{user.username}')

    else:
        user = User.query.get(username)

        session.pop("username")
        db.session.delete(user)
        db.session.commit()
        
        return redirect('/')
    

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def get_feedback_form(username):
    """Display feedback form for user and submit and handle submission"""
    if "username" not in session or username != session["username"]:
        flash("Must be logged in to add feedback")
        return redirect('/login')

    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback(title=title, content=content, username=username)
            
            db.session.add(feedback)
            db.session.commit()

            flash(f"Feedback {feedback.title} added")
            return redirect(f'/users/{feedback.username}')

        return render_template("feedback.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def show_edit_feedback_form(feedback_id):
    """Display form to edit user's feedback """

    feedback = Feedback.query.get_or_404(feedback_id)

    username = session["username"]
    if session["username"] == feedback.user.username:

        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()

            return redirect(f"/users/{feedback.username}")

        return render_template("feedback.html", form=form, feedback=feedback)
    
    else:
        flash(f"You do have permission to edit this form")
        return redirect(f'/users/{username}')

def update_feedback_form(fid):
    """Handle edit submissions from feedback form"""
    feedback = Feedback.query.get_or_404(fid)
    form = FeedbackForm(obj=feedback)
    username = session["username"]

    if form.validate_on_submit():
        form.title = form.title.data
        form.content = form.content.data

        db.session.add(form)
        db.session.commit()

        flash(f"Feedback edited")
        return redirect(f'/users/{username}')
    
    return render_template("feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    username = session["username"]
    if "username" not in session:
        flash("Must be logged in to delete feedback")
        return redirect('/login')
    else:

        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
    
    return redirect(f'/users/{username}')



