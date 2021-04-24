from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator, Optional, Regexp
from wtforms import ValidationError
from werkzeug.security import generate_password_hash

# Login Form
# Only login with E-mail
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login to System')

# Registration Form
class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pass_confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field, User):
        if(User.query.filter_by(email=field.data).first()):
            raise ValidationError('電子郵件已經被註冊過了')
        else:
            return 'ok'
    def check_username(self, field, User):
        if(User.query.filter_by(username=field.data).first()):
            raise ValidationError('使用者名稱已經存在')
        else:
            return 'ok'

# User basic config form
# Userpage, for change basic user setting
class UserConfigForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    avatar = StringField('Avatar Link', validators=[Optional(), Regexp('(https?:\/\/[\w - \.]+(:\d+)?(\/[~\w\/\.]*)?(\?\S*)?(#\S*)?)|(None)')])
    submit = SubmitField('Update')

# OJ setting form
# Userpage, for change OJ IDs, handles
class OJConfigForm(FlaskForm):
    uva_handle = StringField('UVa Handle', validators=[Optional(), Regexp('(\S{1,64})|(None)')])
    toj_id = StringField('TOJ ID', validators=[Optional(), Regexp('([0-9]{1,10})|(None)')])
    zoj_handle = StringField('ZOJ handle', validators=[Optional(), Regexp('(\S{1,64})|(None)')])
    atcoder_handle = StringField('AtCoder handle', validators=[Optional(), Regexp('(\S{1,64})|(None)')])
    cf_handle = StringField('Codeforces handle', validators=[Optional(), Regexp('(\S{1,64})|(None)')])
    submit = SubmitField('Update')