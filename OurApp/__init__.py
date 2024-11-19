from urllib.parse import quote
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thanhan:%s@localhost/qlks_db?charset=utf8mb4' % quote('An@290304')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'mysecretkey'

db = SQLAlchemy()
db.init_app(app)
migrate=Migrate(app, db)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

