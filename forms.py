from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    "Form for creating users."

    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)],)
    password = PasswordField("Password", validators=[InputRequired()],)
    email = StringField("Email", validators=[InputRequired(), Email(), Length(min=5, max=50)],)
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=2, max=30)],)
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=30)],)


class LoginForm(FlaskForm):
    "Form for logging in user."
    username = StringField("Username", validators=[InputRequired()],)
    password = PasswordField("Password", validators=[InputRequired()],)


class FeedbackForm(FlaskForm):
    "Form for adding user feedback"

    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)],)
    content = TextAreaField("Content", validators=[InputRequired()],)
    