from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
)
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField

from simple.models import Course



def choice_query():
    return Course.query


class NewLessonForm(FlaskForm):
    course = QuerySelectField("Course", query_factory=choice_query, get_label="title")
    title = StringField("Lesson Title", validators=[DataRequired(), Length(max=100)])
    slug = StringField(
        "slug",
        render_kw={
            "placeholder": "Descriptive short version of your title. Seo Friendly"
        },
        validators=[DataRequired(), Length(max=32)],
    )
    content = CKEditorField(
        "Lesson Content", render_kw={"rows": "12"}, validators=[DataRequired()]
    )
    thumbnail = FileField(
        "Thumbnail", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Lesson")

class LessonUpdateForm(NewLessonForm):
    thumbnail = FileField("Thumbnail", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")