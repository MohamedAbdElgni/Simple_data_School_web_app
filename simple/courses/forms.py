from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)
from flask_wtf.file import FileField, FileAllowed
from simple.models import  Course

class NewCourseForm(FlaskForm):
    title = StringField(
        "Course Name",
        render_kw={"placeholder": "Enter your Course Title"},
        validators=[DataRequired(), Length(max=50)],
    )
    description = TextAreaField(
        "Course description",
        render_kw={
            "placeholder": "Descriptive short version of your title. Seo Friendly"
        },
        validators=[DataRequired(), Length(max=150)],
    )
    icon = FileField("Icon", validators=[DataRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Create")

    def validate_title(self, title):
        course = Course.query.filter_by(title=title.data).first()
        if course:
            raise ValidationError(
                "Course name Already exists! please choose a Course Name "
            )
