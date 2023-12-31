from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from flask_wtf.file import FileField, FileAllowed
from simple.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    fname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "User name Already exists! please choose a different username "
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email Already exists! please choose a different email "
            )


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])

    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Login")


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField()
    picture = FileField(
        label="Update your image", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:  # type: ignore
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "User name Already exists! please choose a different username "
                )

    def validate_email(self, email):
        if email.data != current_user.email:  # type: ignore
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email Already exists! please choose a different email "
                )
                
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
