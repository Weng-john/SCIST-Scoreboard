from flask import render_template, redirect, request, url_for, flash, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from subsys import app, db, admin
from subsys.models import User, Scoreboard, AdminModelView
from subsys.forms import LoginForm, RegistrationForm, UserConfigForm, OJConfigForm
from wtforms import ValidationError
from OJCapture.uva import get_uva_data

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', **locals())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if(user is None):
            flash('Invalid username or password')
            return render_template('login.html', form=form, invalid=True)
        elif user.check_password(form.password.data):
            login_user(user)
            flash("Successfully Login")
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return render_template('login.html', form=form, invalid=True)
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out of the system')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if(form.validate_on_submit()):
        try:
            form.check_email(form.email, User)
            form.check_username(form.username, User)
        except ValidationError:
            return render_template('register.html', form=form, invalid=True)

        user = User(email=form.email.data,
        username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Successfully registered')
        return redirect(url_for('login'))
    current_app.logger.info(form.errors)
    return render_template('register.html',form=form)

@app.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
    UserConfig = UserConfigForm()
    OJConfig = OJConfigForm()
    return render_template('userpage.html', OJConfigForm=OJConfig, UserConfigForm=UserConfig)

@app.route('/userpage/UpdateUserForm', methods=['POST'])
@login_required
def UpdateUserForm():
    '''
        Allow users to update 
        - username
        - email
        - avatar link
    '''
    UserConfig = UserConfigForm()
    OJConfig = OJConfigForm()
    if(UserConfig.validate_on_submit()):
        current_app.logger.info('in User session')
        # update avatar
        if(UserConfig.avatar.data != 'None' and len(UserConfig.avatar.data) != 0):
            current_app.logger.info('avatar: {}'.format(UserConfig.avatar.data))
            current_user.avatar = UserConfig.avatar.data
        else:
            current_user.avatar = None
        
        # update username
        if(UserConfig.username.data != 'None' and len(UserConfig.username.data) != 0):
            current_app.logger.info('username: {}'.format(UserConfig.username.data))
            current_user.username = UserConfig.username.data

        # update email
        if(UserConfig.email.data != 'None' and len(UserConfig.email.data) != 0):
            current_app.logger.info('email: {}'.format(UserConfig.email.data))
            current_user.email = UserConfig.email.data
        db.session.commit()
    return render_template('userpage.html', OJConfigForm=OJConfig, UserConfigForm=UserConfig)

@app.route('/userpage/UpdateOJForm', methods=['POST'])
@login_required
def UpadteOJForm():
    '''
    Allows users to update their OJ ids and handles
    '''

    current_app.logger.info('in OJ Form session')
    UserConfig = UserConfigForm()
    OJConfig = OJConfigForm()
    current_app.logger.info('object: {}'.format(OJConfig.validate_on_submit()))
    if(OJConfig.validate_on_submit()):
        current_app.logger.info('in OJ session')
        # update uva_handle
        if(OJConfig.uva_handle.data != 'None' and len(OJConfig.uva_handle.data) != 0):
            current_app.logger.info('uva: {}'.format(OJConfig.uva_handle.data))
            current_user.uva_handle = OJConfig.uva_handle.data
        else:
            current_user.uva_handle = None

        # update toj_id
        if(OJConfig.toj_id.data != 'None' and len(OJConfig.toj_id.data) != 0):
            current_app.logger.info('toj: {}'.format(OJConfig.toj_id.data))
            current_user.toj_id = OJConfig.toj_id.data
        else:
            current_user.toj_id = None

        #update zoj_handle
        if(OJConfig.zoj_handle.data != "None" and len(OJConfig.zoj_handle.data) != 0):
            current_app.logger.info('zoj: {}'.format(OJConfig.zoj_handle.data))
            current_user.zoj_handle = OJConfig.zoj_handle.data
        else:
            current_user.zoj_handle = None

        #update atcoder_handle
        if(OJConfig.atcoder_handle.data != "None" and len(OJConfig.atcoder_handle.data) != 0):
            current_app.logger.info('atcoder: {}'.format(OJConfig.atcoder_handle.data))
            current_user.atcoder_handle = OJConfig.atcoder_handle.data
        else:
            current_user.atcoder_handle = None

        #update cf_handle
        if(OJConfig.cf_handle.data != "None" and len(OJConfig.cf_handle.data) != 0):
            current_app.logger.info('cf: {}'.format(OJConfig.cf_handle.data))
            current_user.cf_handle = OJConfig.cf_handle.data
        else:
            current_user.cf_handle = None

        db.session.commit()
    return render_template('userpage.html', OJConfigForm=OJConfig, UserConfigForm=UserConfig)

@app.route('/userpage/<id>')
def public_userpage(id):
    '''
    show public userpage (a.k.a no userpage without setting forms)
    '''
    user = User.query.filter_by(id = id).first()
    if(user is not None):
        return render_template('public_userpage.html', user=user)
    else:
        return render_template('Error.html', message='404 Page Not Found!')

@app.route('/scoreboard', methods=['GET'])
def scoreboard():
    mode = request.args.get('mode')
    if(mode is None):
        # Preset mode 'list'
        mode='list'
    
    if(mode == 'list'):
        '''
            To show some scoreboard list
            10 scoreboards per page
            atmost 5 page items at a time
        '''

        page = request.args.get('page')
        if(page is None or int(page) <= 0):
            page = '1'
        page = int(page)
        column_name = ['id', 'name', 'founder']
        scoreboard = Scoreboard.query.all()
        page_nums = int(len(scoreboard)/10 if len(scoreboard)%10==0 else len(scoreboard)/10)+1

        if(page < 4):
            tmp_page = 5
        elif(page == page_nums):
            tmp_page = page
        else:
            tmp_page = page if page%5 == 0 else page+5-(page%5)
            if(page%4 >= 0 and page/4 >= 1):
                tmp_page += 1
        
        page_item = []
        for x in range(tmp_page-4, tmp_page+1):
            if(x > page_nums or x < 1):
                pass
            else:
                page_item.append(x)
            
        return render_template('scoreboard_list.html', table=scoreboard[10*(page-1):10*page], pages=page_item, current=page)
    elif(mode == 'spec_list'):
        '''
        show specify scoreboard completely
        '''
        id = request.args.get('id')
        scoreboard = Scoreboard.query.filter_by(id=int(id)).first()
        users = scoreboard.users.split(',')
        OJs = ['TOJ', 'UVa', 'ZOJ', 'AtCoder', 'CodeForces']

        if(id is None or scoreboard is None):
            return render_template('Error.html', message='Invalid id')
        else:
            stat_res = {}
            for user in users:
                stat_res[user] = {}
                for OJ in OJs:
                    stat_res[user][OJ] = {}

            # TOJ
            if(scoreboard.toj_pids is not None):
                toj_pids = scoreboard.toj_pids.split(',')
            else:
                toj_pids = None

            # UVa
            if(scoreboard.uva_pnums is not None):
                uva_pnums = scoreboard.uva_pnums.split(',')
                unames = []
                for username in users:
                    unames.append(User.query.filter_by(username=username).first().uva_handle)
                uva_res = get_uva_data(users, unames, uva_pnums)
                for user in users:
                    for pnum in uva_pnums:
                        stat_res[user]['UVa'][int(pnum)] = uva_res[user][int(pnum)]
                current_app.logger.info(f'UVa stat_res: {stat_res[user]["UVa"]}')
            else:
                uva_pnums = None
                uva_res = None
            
            # ZOJ
            if(scoreboard.zoj_pids is not None):
                zoj_pids = scoreboard.zoj_pids.split(',')
            else:
                zoj_pids = None
            
            # AtCoder
            if(scoreboard.atcoder_pids is not None):
                atcoder_pids = scoreboard.atcoder_pids.split(',')
            else:
                atcoder_pids = None
            
            # CodeForces
            if(scoreboard.cf_pids is not None):
                cf_pids = scoreboard.cf_pids.split(',')
            else:
                cf_pids = None
            # TODO: All pids switch into a list
            # TODO: All stats switch into a list
            # TODO: Every Scoreboard has a database, in order to prevent load page too long
            return render_template('scoreboard.html', users=users,
                                                      toj_pids=toj_pids,
                                                      uva_pnums=uva_pnums,
                                                      zoj_pids=zoj_pids,
                                                      atcoder_pids=atcoder_pids,
                                                      cf_pids=cf_pids,
                                                      stat_res = stat_res)
            #return render_template('/scoreboards/{}.html'.format(id))
    else:
        return render_template('Error.html', message='Invalid Mode')


@app.route('/admin')
@login_required
def AdminPanel():
    if(current_user.auth != 'Admin'):
        return redirect(url_for('index'))

# This route is just for test every tiny test QQ
@app.route('/test')
@login_required
def tester():
    return render_template('scoreboard.html')

if __name__ == '__main__':
    db.create_all()
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Scoreboard, db.session))
    app.run(debug=True)