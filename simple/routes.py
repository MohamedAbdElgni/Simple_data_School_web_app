from flask import Flask, render_template, redirect, url_for, flash, request, session, Markup, abort,send_from_directory
from functools import wraps
from flask_ckeditor import upload_fail, upload_success
from simple.forms import RegistrationForm, LoginForm, UpdateProfileForm, NewLessonForm, NewCourseForm, LessonUpdateForm
from simple.models import Lesson, User, Course
from simple import app,bcrypt,db,modal
from flask_login import login_user,current_user,logout_user,login_required
from flask_modals import render_template_modal

import secrets
import os
from PIL import Image
from bs4 import BeautifulSoup


def delete_pic(pic_name,path):
  pic_path = os.path.join(app.root_path,path,pic_name)
  try:
    os.remove(pic_path)
  except:
    pass

def add_img_file(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    img_file = url_for('static', filename=f"user_pics/{current_user.img_file}")
    return f(img_file=img_file, *args, **kwargs)
  return decorated_function

def save_pic(formpic,path='static/user_pics',output_size=None):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(formpic.filename)
  picture_name = random_hex + f_ext
  pic_path = os.path.join(app.root_path,path,picture_name)
  if output_size :
    i = Image.open(formpic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return picture_name
  else:
    output_size=(150,150)
    i = Image.open(formpic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return picture_name


#
def get_previous_next_lesson(lesson):
    course = lesson.course_name
    for lsn in course.lessons:
        if lsn.title == lesson.title:
            index = course.lessons.index(lsn)
            previous_lesson = course.lessons[index - 1] if index > 0 else None
            next_lesson = (
                course.lessons[index + 1] if index < len(course.lessons) - 1 else None
            )
            break
    return previous_lesson, next_lesson
    

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = os.path.join(app.root_path, 'static/media')
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='File extension not allowed!')
    random_hex = secrets.token_hex(8)
    image_name = random_hex+extension
    f.save(os.path.join(app.root_path, 'static/media', image_name))
    url = url_for('uploaded_files', filename=image_name)
    return upload_success(url, filename=image_name)

@app.route('/')
@app.route('/home',methods=['POST','GET'])
def home():
  lessons = Lesson.query.all()
  courses = Course.query.all()
  if current_user.is_authenticated:
    img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
    return render_template_modal('home.html' ,img_file=img_file , courses=courses,lessons=lessons ,title="home")
  else :
    return render_template('home.html', courses=courses,lessons=lessons ,title="home")
  
  
#about
@app.route('/about')
def about():
  if current_user.is_authenticated:
    img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
    return render_template_modal('about.html' ,img_file=img_file   ,title="home")
  else :
    return render_template('about.html'  ,title="home")

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
  return redirect(url_for('login'))



@app.route("/dashboard",methods=['POST','GET'])
@login_required
def dashboard():
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template('dashboard.html',title='Dashboard', img_file=img_file,active_tab=None)


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
  new_course_form = NewCourseForm()
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  flag = session.pop('flag',False)
  form = ''
  if 'slug' in request.form:
    form = 'new_lesson_form'
    
  elif 'description' in request.form:
    
    form = 'new_course_form'
    
  if form == "new_lesson_form" and new_lesson_form.validate_on_submit():
    if new_lesson_form.thumbnail.data:
      pic_file = save_pic(new_lesson_form.thumbnail.data, path='static/lesson_thumbnails',output_size=(250,300))
    
    lesson_slug = str(new_lesson_form.slug.data).replace(" ", "-")
    course = new_lesson_form.course.data
    lesson = Lesson(
        title=new_lesson_form.title.data,
        content=new_lesson_form.content.data,
        slug=lesson_slug,
        author=current_user,
        course_name=course,
        thumbnail=pic_file
    )
    
    db.session.add(lesson)
    db.session.commit()
    flash(f'Lesson {new_lesson_form.title.data} has been Created','success')
    return redirect(url_for("new_lesson"))
  return render_template_modal(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        active_tab="new_lesson",
        modal=modal,
        img_file=img_file
    )
  
@app.route('/dashboard/new_course',methods=['GET','POST'])
@login_required
def new_course():
  new_course_form = NewCourseForm()
  if new_course_form.validate_on_submit():
      if new_course_form.icon.data:
        pic_file = save_pic(new_course_form.icon.data,path='static/course_icon',output_size=(150,150))
      # This is to remove spaces from the title and replace them with dashes 
      # to be used in the url SEO friendly
      course_title = str(new_course_form.title.data).replace(" ", "-")
      course_description = new_course_form.description.data
      soup = BeautifulSoup(course_description, 'html.parser')
      course_description_text = soup.get_text()

      course = Course(title=course_title,
                      description=course_description_text,
                      icon = pic_file)
      db.session.add(course)
      db.session.commit()
      flash("New Course has been created!", "success")
      return redirect(url_for("new_lesson"))
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  
  return render_template('new_course.html',
                        img_file=img_file,
                        title='New course',
                        new_course_form=new_course_form,
                        active_tab="new_course")



@app.route("/<string:course>/<string:lesson_slug>")
@login_required
def lesson(lesson_slug,course):
  lesson = Lesson.query.filter_by(slug=lesson_slug).first()
  if lesson:
    previous_lesson, next_lesson = get_previous_next_lesson(lesson)
  lesson_id = lesson.id if lesson else None
  lesson = Lesson.query.get_or_404(lesson_id)
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template("lesson_view.html",title=lesson.title,lesson=lesson,img_file=img_file,previous_lesson=previous_lesson,next_lesson=next_lesson)
  
  
@app.route("/<string:course_title>")
@login_required
def course(course_title):
  course = Course.query.filter_by(title=course_title).first()
  course_id = course.id if course else None
  course = Course.query.get_or_404(course_id)
  courses = Course.query.all()
  # this is to check if the course has lessons or not to help us in the jinja
  flag_lesson = 0 if len(course.lessons) == 0 else 1
  

  
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template("course.html",flag_lesson=flag_lesson,courses=courses,title=course.title,course=course,img_file=img_file)


@app.route("/courses")
@login_required
def courses():
  courses = Course.query.all()
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  return render_template("courses.html",title="Courses",courses=courses ,img_file=img_file)


@app.route('/dashboard/user_lessons',methods=['GET','POST'])
@login_required
@add_img_file
def user_lessons(img_file):
  return render_template('user_lessons.html',img_file=img_file,title='Your Lessons', active_tab='user_lessons')



@app.route("/<string:course>/<string:lesson_slug>/update" ,methods=['GET','POST'])
@login_required
def update_lesson(lesson_slug,course):
  lesson = Lesson.query.filter_by(slug=lesson_slug).first()
  if lesson:
    previous_lesson, next_lesson = get_previous_next_lesson(lesson)
  lesson_id = lesson.id if lesson else None
  lesson = Lesson.query.get_or_404(lesson_id)
  img_file = url_for('static',filename = f"user_pics/{current_user.img_file}")
  if lesson.author != current_user:
    abort(403)
  form = LessonUpdateForm()
  if form.validate_on_submit():
    lesson.course_name = form.course.data
    lesson.title = form.title.data
    lesson.slug = (form.slug.data).replace(" ", "-")
    lesson.content = form.content.data
    if form.thumbnail.data:
      #delete the old thumbnail function
      delete_pic(lesson.thumbnail,path='static/lesson_thumbnails')
      pic_file = save_pic(form.thumbnail.data, path='static/lesson_thumbnails',output_size=(250,300))
      lesson.thumbnail = pic_file
    db.session.commit()
    
    flash("Your lesson has been updated!", "success")
    print(current_user.password)
    return redirect(url_for("lesson", lesson_slug=lesson.slug,course=lesson.course_name.title))
  elif request.method == "GET":
    form.course.data = lesson.course_name.title
    form.title.data = lesson.title
    form.slug.data = lesson.slug
    form.content.data = lesson.content
  return render_template("update_lesson.html",title="Update | " +lesson.title,
                        lesson=lesson,img_file=img_file,
                        previous_lesson=previous_lesson,
                        next_lesson=next_lesson,
                        form = form)
                        


@app.route("/lesson/<lesson_id>/delete",methods=['POST'])
def delete_lesson(lesson_id):
  lesson = Lesson.query.get_or_404(lesson_id)
  if lesson.author != current_user:
    abort(403)
  db.session.delete(lesson)
  db.session.commit()
  flash("Your lesson has been deleted!", "success") 
  return redirect(url_for("user_lessons"))