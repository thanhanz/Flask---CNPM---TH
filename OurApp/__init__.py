from urllib.parse import quote
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import cloudinary

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thanhan:%s@localhost/qlks_db?charset=utf8mb4' % quote('An@290304')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'mysecretkey'

db = SQLAlchemy()
db.init_app(app)
migrate=Migrate(app, db)
login = LoginManager(app=app)
app.config['PAGE_SIZE'] = 8
app.config['COMMENT_SIZE'] = 3


cloudinary.config(
    cloud_name = "dc0apkpb1",
    api_key = "779694575782262",
    api_secret = "9FHCYpnOesWR8JMM9VTLGYOyKqs", # Click 'View API Keys' above to copy your API secret
    secure=True
)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

