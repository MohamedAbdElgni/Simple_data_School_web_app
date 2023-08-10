
import secrets
import os
from flask_login import current_user
from flask_ckeditor import upload_fail, upload_success
from flask import (
    render_template,
    url_for,
    request,
    send_from_directory,Blueprint
)
from flask import current_app
from simple.models import Lesson, Course

main = Blueprint("main", __name__)

@main.route("/files/<path:filename>")
def uploaded_files(filename):
    path = os.path.join(current_app.root_path, "static/media")
    return send_from_directory(path, filename)


@main.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("upload")
    extension = f.filename.split(".")[-1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        return upload_fail(message="File extension not allowed!")
    random_hex = secrets.token_hex(8)
    image_name = random_hex + extension
    f.save(os.path.join(current_app.root_path, "static/media", image_name))
    url = url_for("uploaded_files", filename=image_name)
    return upload_success(url, filename=image_name)


@main.route("/")
@main.route("/home", methods=["POST", "GET"])
def home():
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(
        page=1, per_page=3
    )
    courses = Course.query.all() 
    courses_limit = Course.query.paginate(page=1, per_page=6)
    if current_user.is_authenticated:
        img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
        return render_template(
            "home.html",
            courses_limit=courses_limit,
            img_file=img_file,
            courses=courses,
            lessons=lessons,
            title="home",
        )
    else:
        return render_template(
            "home.html",
            courses_limit=courses_limit,
            courses=courses,
            lessons=lessons,
            title="home",
        )


# about
@main.route("/about")
def about():
    if current_user.is_authenticated:
        img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
        return render_template("about.html", img_file=img_file, title="About")
    else:
        return render_template("about.html", title="About")
