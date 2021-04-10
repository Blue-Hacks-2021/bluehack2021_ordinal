from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms import TextField, BooleanField

from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    middleName = StringField('Middle Name')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class StartEventForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    description = StringField('Event Description')
    volunteerCount = IntegerField('Volunteers Needed', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    startEvent = DateTimeField('Event Start', validators=[DataRequired()])
    endEvent = DateTimeField('Event Start', validators=[DataRequired()])
    submit = SubmitField('Host Event')

class VolunteerForm(FlaskForm):
    volunteer = SubmitField('Volunteer')

class CommentForm(FlaskForm):
    textComment = TextField('Comment', validators=[DataRequired()])
    submitComment = SubmitField('Comment')

class ReplyForm(FlaskForm):
    textReply = TextField('Reply', validators=[DataRequired()])
    submitReply = SubmitField('Comment')

