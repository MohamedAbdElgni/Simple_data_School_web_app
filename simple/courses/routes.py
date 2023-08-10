from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint

)

from simple.courses.forms import NewCourseForm
from simple.models import Lesson ,Course
from simple import db
from simple.helpers import save_pic
from flask_login import (current_user, login_required)

from bs4 import BeautifulSoup





courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/dashboard/new_course", methods=["GET", "POST"])
@login_required
def new_course():
    new_course_form = NewCourseForm()
    if new_course_form.validate_on_submit():
        if new_course_form.icon.data:
            pic_file = save_pic(
                new_course_form.icon.data,
                path="static/course_icon",
                output_size=(150, 150),
            )
        # This is to remove spaces from the title and replace them with dashes
        # to be used in the url SEO friendly
        course_title = str(new_course_form.title.data).replace(" ", "-")
        course_description = new_course_form.description.data
        soup = BeautifulSoup(course_description, "html.parser")
        course_description_text = soup.get_text()

        course = Course(
            title=course_title, description=course_description_text, icon=pic_file
        )
        db.session.add(course)
        db.session.commit()
        flash("New Course has been created!", "success")
        return redirect(url_for("lessons.new_lesson"))
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")

    return render_template(
        "new_course.html",
        img_file=img_file,
        title="New course",
        new_course_form=new_course_form,
        active_tab="new_course",
    )





@courses_bp.route("/<string:course_title>")
@login_required
def course(course_title):
    course = Course.query.filter_by(title=course_title).first()
    course_id = course.id if course else None
    course = Course.query.get_or_404(course_id)
    courses = Course.query.all()
    courses_limit = Course.query.paginate(page=1, per_page=6)
    page = request.args.get("page", 1, type=int)
    lessons = Lesson.query.filter_by(course_id=course_id).paginate(
        page=page, per_page=3
    )
    # this is to check if the course has lessons or not to help us in the jinja
    flag_lesson = 0 if len(course.lessons) == 0 else 1
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    return render_template(
        "course.html",
        lessons=lessons,
        flag_lesson=flag_lesson,
        courses_limit=courses_limit,
        courses=courses,
        title=course.title,
        course=course,
        img_file=img_file,
    )


@courses_bp.route("/courses")
@login_required
def courses():
    course_count = Course.query.all()
    page = request.args.get("page", 1, type=int)
    courses = Course.query.paginate(page=page, per_page=6)
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    return render_template(
        "courses.html",
        title="Courses",
        courses=courses,
        img_file=img_file,
        course_count=course_count,
    )
