import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

# build app
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']= '6f9bdbe14a868fe55abfdf77d21f7355bdc76674'
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'database/UserData.sqlite')
app.config['SQLALCHEMY_BINDS'] = {
    'UserData': 'sqlite:///'+os.path.join(basedir,'database/UserData.sqlite'),
    'ScoreboardData': 'sqlite:///'+os.path.join(basedir,'database/ScoreboardData.sqlite')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# flask admin
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# build db
db = SQLAlchemy(app)
Migrate(app,db)

# build login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# build admin panel
admin = Admin(app)
