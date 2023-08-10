import os
from flask import current_app




def delete_pic(pic_name: str, path: str) -> None:
    pic_path = os.path.join(current_app.root_path, path, pic_name)
    try:
        os.remove(pic_path)
    except FileNotFoundError as e:
        # Log the exception details for debugging purposes
        print(f"Error deleting {pic_path}: {e}")
    except Exception as e:
        # Handle other exceptions here, or log them for debugging
        print(f"An error occurred while deleting {pic_path}: {e}")



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
