from functools import wraps
from flask_login import current_user
from flask_mail import Message
from simple import mail
from flask import url_for, current_app

def send_reset_email(user):
    token = user.get_reset_token()
    
    # Compose the HTML email content
    html = f"""
    <html>
    <head></head>
    <body>
        <div style="background-color: #f2f2f2; padding: 20px; text-align: center;">
            <img src="cid:logo" alt="Your Logo" style="width: 200px;">
            <h1>Simple Data School Password Reset</h1>
            <p>To reset your password, click the following link:</p>
            <a href="{url_for('users.reset_password', token=token, _external=True)}">Reset Password</a>
            <p>If you did not request this reset, please ignore this email.</p>
        </div>
    </body>
    </html>
    """
    
    # Create a Message object with HTML content
    msg = Message(
        "Simple Data School Password Reset",
        sender="mohamed.pay.878@gmail.com",
        recipients=[user.email]
    )
    
    msg.html = html
    
    # Attach your logo as an inline image
    logo_path = 'static/PngItem_1822974.png'  # Relative path to your image
    with current_app.open_resource(logo_path) as logo:
        msg.attach(
            "logo.png",
            "image/png",
            logo.read(),
            "inline",
            headers=[["Content-ID", "<logo>"]]
        )

    mail.send(msg)

    
    
def add_img_file(fu_nc):
    @wraps(fu_nc)
    def decorated_function(*args, **kwargs):
        img_file = url_for("static", filename=f"user_pics/{current_user.img_file}")
        return fu_nc(img_file=img_file, *args, **kwargs)

    return decorated_function
