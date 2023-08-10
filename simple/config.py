class Config:
    """This is the app configuration class , it contains the app secret key , database uri , mail server configuration
    and the ckeditor configuration
    """
    SECRET_KEY = open("flaskapp.venv/app_sec.key", "r").read()
    SQLALCHEMY_DATABASE_URI = "sqlite:///simple.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True # this is just to suppress a warning
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = "main.upload"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = open("flaskapp.venv/mail.key", "r").read() 
    MAIL_PASSWORD = open("flaskapp.venv/email_pass.key", "r").read()
