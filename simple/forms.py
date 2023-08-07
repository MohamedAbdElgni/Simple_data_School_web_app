from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired ,Length,Email,Regexp,EqualTo,ValidationError
from flask_wtf.file import FileField, FileAllowed
from simple.models import User,Course
from flask_login import current_user
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField

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
        validators=[
            DataRequired()
            
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")
    
    def validate_username(self,username):
      user = User.query.filter_by(username = username.data).first()
      if user:
        raise ValidationError("User name Already exists! please choose a different username ")
    def validate_email(self,email):
      user = User.query.filter_by(email = email.data).first()
      if user:
        raise ValidationError("Email Already exists! please choose a different email ")
  
  
  
class LoginForm(FlaskForm):
    
    email = StringField(label="Email", validators=[DataRequired(),Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])

    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label='Login')
    
class UpdateProfileForm(FlaskForm):
    
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField()
    picture = FileField(label='Update your image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField("Update")
    
    def validate_username(self,username):
      if username.data != current_user.username:
        user = User.query.filter_by(username = username.data).first()
        if user:
          raise ValidationError("User name Already exists! please choose a different username ")
    def validate_email(self,email):
      if email.data != current_user.email:
        user = User.query.filter_by(email = email.data).first()
        if user:
          raise ValidationError("Email Already exists! please choose a different email ")

def choice_query():
  
  return Course.query
class NewLessonForm(FlaskForm):
  course = QuerySelectField("Course", query_factory=choice_query,get_label='title')
  title = StringField('Lesson Title', validators=[DataRequired(),Length(max=100)])
  slug = StringField('slug',render_kw={"placeholder":"Descriptive short version of your title. Seo Friendly"}, validators=[DataRequired(),Length(max=32)])
  content = CKEditorField('Lesson Content',render_kw={"rows":"12"}, validators=[DataRequired()])
  thumbnail = FileField("Thumbnail",validators=[DataRequired(),FileAllowed(['jpg','png'])])
  submit = SubmitField("Lesson")
  
class NewCourseForm(FlaskForm):
  title = StringField('Course Name',render_kw={"placeholder":"Enter your Course Title"},validators=[DataRequired(),Length(max=50)])
  description = TextAreaField('Course description',render_kw={"placeholder":"Descriptive short version of your title. Seo Friendly"},validators=[DataRequired(),Length(max=150)])
  icon = FileField('Icon',validators=[DataRequired(),FileAllowed(['jpg','png'])])
  submit = SubmitField('Create')
  def validate_title(self,title):
      
    course = Course.query.filter_by(title = title.data).first()
    if course:
      raise ValidationError("Course name Already exists! please choose a Course Name ")
    

class LessonUpdateForm(NewLessonForm):
  thumbnail = FileField("Thumbnail",validators=[FileAllowed(['jpg','png'])])
  submit = SubmitField("Update")

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

