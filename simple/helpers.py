import os
import secrets
from PIL import Image
from flask import current_app

def save_pic(formpic, path="static/user_pics", output_size=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(formpic.filename)
    picture_name = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, path, picture_name)
    if output_size:
        i = Image.open(formpic)
        i.thumbnail(output_size)
        i.save(pic_path)
        return picture_name
    else:
        output_size = (150, 150)
        i = Image.open(formpic)
        i.thumbnail(output_size)
        i.save(pic_path)
        return picture_name
