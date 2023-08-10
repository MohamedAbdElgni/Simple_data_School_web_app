from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint
)
from flask_login import (login_user, current_user, logout_user, login_required)

from simple.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateProfileForm,
    RequestResetForm,
    ResetPasswordForm,
)
from simple.models import (Lesson, User)
from simple import  bcrypt, db 

from simple.helpers import save_pic
from simple.users.helpers import send_reset_email, add_img_file

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created successfully for {form.username.data}", category="success"
        )
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            flash(f"Welcome Back {user.username.title()}", "success")
            return redirect((next_page) if next_page else url_for("main.home"))
        else:
            flash(
                "Login Unsuccessful. Please check Email or password and try again",
                "danger",
            )
    return render_template("login.html", title="login", form=form)


@users.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    return render_template(
        "dashboard.html", title="Dashboard", img_file=img_file, active_tab=None
    )

@users.route("/dashboard/profile", methods=["GET", "POST"])
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
        flash("Your profile has been updated", "success")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        img_file=img_file,
        active_tab="profile",
    )
@users.route("/author/<string:username>", methods=["GET"])
@login_required
@add_img_file
def author(img_file, username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    lessons = (
        Lesson.query.filter_by(author=user)
        .order_by(Lesson.date_posted.desc())
        .paginate(page=page, per_page=3)
    )
    return render_template("author.html", img_file=img_file, lessons=lessons, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print("sending email in progress!!!!!!")
            send_reset_email(user)
        flash("Message sent successfully", category="success")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token: any):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("The Token Is Invalid Or Expired", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your Password now updated. you Can log in", category="success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)