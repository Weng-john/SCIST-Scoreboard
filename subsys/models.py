from subsys import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for, request, redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

# User in database
class User(db.Model, UserMixin):
    __bind_key__ = 'UserData'
    # columns
    id             = db.Column(db.Integer, primary_key = True)
    email          = db.Column(db.String(64),unique=True, index=True)
    username       = db.Column(db.String(64),unique=True, index=True)
    password_hash  = db.Column(db.String(1024))
    auth           = db.Column(db.String(32))
    avatar         = db.Column(db.String(128), nullable=True)
    uva_handle     = db.Column(db.String(64), nullable=True, unique=True)
    toj_id         = db.Column(db.String(10), nullable=True, unique=True)
    zoj_handle     = db.Column(db.String(64), nullable=True, unique=True)
    atcoder_handle = db.Column(db.String(64), nullable=True, unique=True)
    cf_handle      = db.Column(db.String(64), nullable=True, unique=True)

    def __init__(self, email, username, password, auth='User', avatar = None, uva_id=None, toj_id=None, zoj_handle=None, atcoder_handle=None, cf_handle=None):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.auth = auth
        self.avatar = avatar
        self.uva_id = uva_id
        self.toj_id = toj_id
        self.zoj_handle = zoj_handle
        self.atcoder_handle = atcoder_handle
        self.cf_handle = cf_handle
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Scoreboard in database
class Scoreboard(db.Model, UserMixin):
    __bind_key__ = 'ScoreboardData'
    # columns
    id           = db.Column(db.Integer, primary_key = True)
    name         = db.Column(db.String(1024))
    founder      = db.Column(db.String(1024))
    users        = db.Column(db.String(4096))
    uva_pnums    = db.Column(db.String(4096), nullable=True)
    toj_pids     = db.Column(db.String(4096), nullable=True)
    zoj_pids     = db.Column(db.String(4096), nullable=True)
    atcoder_pids = db.Column(db.String(4096), nullable=True)
    cf_pids      = db.Column(db.String(4096), nullable=True)

    def __init__(self, name, users, founder=None, uva_pnums=None, toj_pids=None, zoj_pids=None, atcoder_pids=None, cf_pids=None):
        self.name = name
        self.founder = founder
        self.users = users
        self.uva_pnums = uva_pnums
        self.toj_pids = toj_pids
        self.zoj_pids = zoj_pids
        self.atcoder_ids = atcoder_pids
        self.cf_ids = cf_pids

# admin panel permission setting
# using flask_admin
class AdminModelView(ModelView):
    def is_visible(self):
        try:
            if(current_user.auth == 'Admin'):
                return True
            else:
                return False
        except:
            return False

    def is_accessible(self):
        try:
            if(current_user.auth == 'Admin'):
                can_create = True
                can_edit = True
                can_delete = True
                return True
            else:
                return False
        except:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)