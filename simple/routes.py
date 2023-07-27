from flask import Flask, render_template,redirect, url_for, flash,request
from simple.forms import RegistrationForm, LoginForm, UpdateProfileForm, NewLessonForm
from simple.models import Lesson, User, Course
from simple import app,lessons,courses,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image


def save_pic(formpic):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(formpic.filename)
  picture_name = random_hex + f_ext
  pic_path = os.path.join(app.root_path,'static/user_pics',picture_name)
  output_size = (150,150)
  i = Image.open(formpic)
  i.thumbnail(output_size)
  i.save(pic_path)
  return picture_name

@app.route('/')
@app.route('/home' ,methods=['POST','GET'])
def home():
  if current_user.is_authenticated:
    img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
    return render_template('home.html' ,img_file=img_file , courses=courses,lessons=lessons ,title="home")
  else :
    return render_template('home.html'  , courses=courses,lessons=lessons ,title="home")
  
  
#about
@app.route('/about')
def about():
  if current_user.is_authenticated:
    img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
    return render_template('about.html' ,img_file=img_file , courses=courses,lessons=lessons ,title="home")
  else :
    return render_template('about.html'  , courses=courses,lessons=lessons ,title="home")

#regfrom
@app.route('/register',methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(fname=form.fname.data,
                lname = form.lname.data,
                username=form.username.data, 
                email = form.email.data,
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created successfully for {form.username.data}", category="success")
    return redirect(url_for("login"))
  return render_template("register.html", title="Register", form=form)

@app.route('/login',methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password,form.password.data):
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      flash(f"Welcome Back {user.username.title()}" ,"success")
      return redirect((next_page) if next_page else url_for("home"))
    else:
      
      flash("Login Unsuccessful. Please check Email or password and try again","danger")
  return render_template('login.html',title='login',form=form)


@app.route('/logout',methods=['GET','POST'])
def logout():
  logout_user()
  return redirect(url_for('home'))



@app.route("/dashboard",methods=['POST','GET'])
@login_required
def dashboard():
  
  return render_template('dashboard.html',title='Dashboard', active_tab=None)


@app.route("/dashboard/profile",methods=['GET',"POST"])
@login_required
def profile():
  profile_form = UpdateProfileForm()
  if profile_form.validate_on_submit():
    if profile_form.picture.data:
      picture_file = save_pic(profile_form.picture.data)
      current_user.img_file = picture_file
    current_user.username = profile_form.username.data
    current_user.email = profile_form.email.data
    current_user.bio = profile_form.bio.data
    db.session.commit()
    flash("Your profile has been updated",'success')
    return redirect(url_for('profile'))
  elif request.method == "GET":
    profile_form.username.data = current_user.username
    profile_form.email.data = current_user.email
    profile_form.bio.data = current_user.bio
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template('profile.html',title='Profile',profile_form = profile_form, img_file = img_file ,active_tab='profile')


@app.route('/dashboard/new_lesson',methods=['GET','POST'])
@login_required
def new_lesson():
  new_lesson_form = NewLessonForm()
  if new_lesson_form.validate_on_submit():
    course = new_lesson_form.course.data
    lesson = Lesson(title = new_lesson_form.title.data,
                    content = new_lesson_form.content.data,
                    slug = new_lesson_form.slug.data,
                    author = current_user,
                    course_name = course)
    db.session.add(lesson)
    db.session.commit()
    flash(f'Lesson {new_lesson_form.title.data} has been Created','info')
    return redirect(url_for("home"))
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template('new_lesson.html',title='New Lesson', img_file = img_file, new_lesson_form = new_lesson_form ,active_tab='new_lesson')
  