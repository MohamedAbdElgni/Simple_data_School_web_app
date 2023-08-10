from functools import wraps
from flask_login import current_user
from flask_mail import Message
from flask import url_for
from simple import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Simple Data School Password Reset",
        sender="mohamed.pay.878@gmail.com",
        print(f"sending email in progress!!!!!! to {user.email}")
        recipients=[user.email],
        body=f"""To Reset your password, Visit the following Link
                {url_for('users.reset_password', token = token,_external=True)}
                If you did not make this, please ignore this Email""",
    )
    mail.send(msg)




def add_img_file(fu_nc):
    @wraps(fu_nc)
    def decorated_function(*args, **kwargs):
        img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
        return fu_nc(img_file=img_file, *args, **kwargs)

    return decorated_function
