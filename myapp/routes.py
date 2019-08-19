from flask import render_template, request, redirect, flash, url_for
from myapp.forms import LoginForm, SignupForm
from myapp import app, db
from myapp.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from api.daily_summaries import DailySummaries



@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pass']
        print(name, password)
        user = User.query.filter_by(username=name).first()
        print(user)
        if user:
            if check_password_hash(user.password_hash, password):
                return redirect(url_for('register'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        model = request.form['model']
        vid = request.form['vid']
        password = request.form['pass']

        hashed_password = generate_password_hash(password, method='sha256')
        try:
            user = User(username=name,email=email,password_hash=hashed_password,vehicle_model=model, vehicle_id=vid)
            db.session.add(user)
            db.session.commit()
            #flash('You are now registered!')
            return redirect(url_for('index'))

        except Exception as inst:
            print(type(inst))
    return render_template('signup.html', form=form)


@app.route('/daily',methods=['GET', 'POST'])
def daily_summaries():
    daily_obj = DailySummaries()
    return daily_obj.daily_summaries()


@app.route('/daily/trip/<int:id>',methods = ['GET','POST'])
def trip_summaries(id):
    trip_obj = DailySummaries().TripSummaries()
    return trip_obj.trip_analysis(id)