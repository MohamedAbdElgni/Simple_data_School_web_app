from flask_login import (current_user, login_required)
from flask_modals import render_template_modal
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    abort,
    Blueprint
)
from simple import  db, modal
from simple.models import Lesson
from simple.helpers import save_pic
from simple.lessons.forms import (
    NewLessonForm,
    LessonUpdateForm,
)
from simple.lessons.helpers import get_previous_next_lesson, delete_pic

from simple.courses.forms import NewCourseForm
from simple.users.helpers import add_img_file

lessons = Blueprint('lessons', __name__)

@lessons.route("/<string:course>/<string:lesson_slug>")
@login_required
def lesson(lesson_slug, course):
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    return render_template(
        "lesson_view.html",
        title=lesson.title,
        lesson=lesson,
        img_file=img_file,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
    )
    

@lessons.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()
    new_course_form = NewCourseForm()
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    flag = session.pop("flag", False)
    form = ""
    if "slug" in request.form:
        form = "new_lesson_form"

    elif "description" in request.form:
        form = "new_course_form"

    if form == "new_lesson_form" and new_lesson_form.validate_on_submit():
        if new_lesson_form.thumbnail.data:
            pic_file = save_pic(
                new_lesson_form.thumbnail.data,
                path="static/lesson_thumbnails",
                output_size=(250, 300),
            )

        lesson_slug = str(new_lesson_form.slug.data).replace(" ", "-")
        course = new_lesson_form.course.data
        lesson = Lesson(
            title=new_lesson_form.title.data,
            content=new_lesson_form.content.data,
            slug=lesson_slug,
            author=current_user,
            course_name=course,
            thumbnail=pic_file,
        )

        db.session.add(lesson)
        db.session.commit()
        flash(f"Lesson {new_lesson_form.title.data} has been Created", "success")
        return redirect(url_for("lessons.new_lesson"))
    return render_template_modal(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        active_tab="new_lesson",
        modal=modal,
        img_file=img_file,
    )

@lessons.route("/dashboard/user_lessons", methods=["GET", "POST"])
@login_required
@add_img_file
def user_lessons(img_file):
    return render_template(
        "user_lessons.html",
        img_file=img_file,
        title="Your Lessons",
        active_tab="user_lessons",
    )


@lessons.route("/<string:course>/<string:lesson_slug>/update", methods=["GET", "POST"])
@login_required
def update_lesson(lesson_slug, course):
    lesson = Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson = Lesson.query.get_or_404(lesson_id)
    img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
    if lesson.author != current_user:
        abort(403)
    form = LessonUpdateForm()
    if form.validate_on_submit():
        lesson.course_name = form.course.data
        lesson.title = form.title.data
        lesson.slug = (form.slug.data).replace(" ", "-")
        lesson.content = form.content.data
        if form.thumbnail.data:
            # delete the old thumbnail function
            delete_pic(lesson.thumbnail, path="static/lesson_thumbnails")
            pic_file = save_pic(
                form.thumbnail.data,
                path="static/lesson_thumbnails",
                output_size=(250, 300),
            )
            lesson.thumbnail = pic_file
        db.session.commit()

        flash("Your lesson has been updated!", "success")
        print(current_user.password)
        return redirect(
            url_for("lessons.lesson", lesson_slug=lesson.slug, course=lesson.course_name.title)
        )
    elif request.method == "GET":
        form.course.data = lesson.course_name.title
        form.title.data = lesson.title
        form.slug.data = lesson.slug
        form.content.data = lesson.content
    return render_template(
        "update_lesson.html",
        title=f"Update | {lesson.title}",
        lesson=lesson,
        img_file=img_file,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        form=form,
    )


@lessons.route("/lesson/<lesson_id>/delete", methods=["POST"])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    db.session.delete(lesson)
    db.session.commit()
    flash("Your lesson has been deleted!", "success")
    return redirect(url_for("lessons.user_lessons"))

