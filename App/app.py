from flask import Flask, render_template, url_for, session, redirect, request, jsonify
import os, json, database, mock_database_setup
from datetime import datetime, timedelta

branches = ['San Jose', 'Santa Clara', 'Palo Alto', 'Sunnyvale', 'Mountain View']
app = Flask(__name__)
app.secret_key = 'key'

@app.route('/', methods=['POST', 'GET'])
def index():
    message = session.pop('message', None)
    if 'branch' not in session.keys():
        session['branch'] = 'San Jose'
    return render_template('index.html', branches=branches, message=message)

@app.route('/branch/<name>')
def branch(name):
    session['branch'] = name
    return redirect('/')

@app.route('/log_workout', methods=['POST', 'GET'])
def log_workout():
    if request.method == 'POST':
        treadmill = int(request.form['treadmill-hours'] or 0)
        cycling = int(request.form['cycling-hours'] or 0)
        stair_machine = int(request.form['stair-machine-hours'] or 0)
        weight_training = int(request.form['weight-training-hours'] or 0)
        database.log_workout(session['username'], treadmill, cycling, stair_machine, weight_training)
        return redirect('/your_activity')
    return render_template('log_workout.html')

@app.route('/your_activity', methods=['POST', 'GET'])
def your_activity():
    if 'activity_days' not in session:
        session['activity_days'] = 7
    if request.method == 'POST':
        if request.form.get('week'):
            session['activity_days'] = 7
        if request.form.get('month'):
            session['activity_days'] = 30
        if request.form.get('three-months'):
            session['activity_days'] = 90
    activity_summary = database.get_activity_summary(session['username'], session['activity_days'])
    return render_template('your_activity.html', data=activity_summary)

@app.route('/schedules', methods=['POST', 'GET'])
def schedules():
    if 'week_offset' not in session:
        # if week_offset is not in session, set it to 0
        session['week_offset'] = 0

    if request.method == 'POST':
        if request.form.get('next-week'):
            session['week_offset'] += 1
        elif request.form.get('prev-week'):
            session['week_offset'] -= 1
        elif request.form.get('register'):
            item_id = request.form.get('register')
            database.register_to_class(item_id, session['week_offset'], session['branch'], session['username'])
            return redirect(url_for('your_classes'))

    time = datetime.utcnow() + timedelta(weeks=session['week_offset'])
    data = database.get_week_schedule(time, session['branch'])
    if len(data) == 0:
        data = [{"Class": "", "Instructor": "", "Start Time": "", "End Time": "", "Capacity": ""}]
    return render_template('schedules.html', data=data)


@app.route('/your_classes', methods=['POST', 'GET'])
def your_classes():
    past, future = database.get_classes(session['username'])
    if len(past) == 0:
        past = [{"Class": "", "Instructor": "", "Start Time": "", "End Time": "", "Location": ""}]
    if len(future) == 0:
        future = [{"Class": "", "Instructor": "", "Start Time": "", "End Time": "", "Location": ""}]
    if request.method == 'POST':        
        item_id = request.form.get('cancel')
        database.deregister_class(item_id, session['username'])
        return redirect(url_for('your_classes'))
    return render_template('your_classes.html', past=past, future=future)

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        membership = request.form['membership']
        database.register_member(name, email, password, gender, date_of_birth, membership)
        session['message'] = 'Registration successful!'
        return redirect(url_for('index'))
    return render_template('registration.html')

@app.route('/checkins', methods=['POST', 'GET'])
def checkins():
    if request.method == 'POST':
        email = request.form['email']
        submit_type = request.form['submit_type']
        if submit_type == 'Check-In':
            database.check_in(email, datetime.utcnow())
        elif submit_type == 'Check-Out':
            database.check_out(email, datetime.utcnow())
    return render_template('checkins.html')

@app.route('/trialsignup', methods=['POST', 'GET'])
def trialsignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        database.trial_signup(name, email, password)
        session['message'] = 'Trial Signup Successful!'
        return redirect(url_for('index'))
    return render_template('trialsignup.html')

@app.route('/analytics')
def analytics():
    data = database.retrieve_analytics()
    if len(data) == 0:
        data = [{"":""}]
    return render_template('analytics.html', data=data)

@app.route('/memberships')
def memberships():
    memberships = {'Premium':{'Cost':100, 'Locations':'All'}, 'Student':{'Cost':30, 'Locations':['San Jose', 'Palo Alto']}}
    return render_template('memberships.html', data = json.dumps(memberships))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Validate the user's credentials by checking if they match the ones stored in your user database.
        is_valid, msg = database.validate_credentials(email, password)
        if is_valid:
            # Set a session variable to remember that the user is logged in.
            session['logged_in'] = True
            session['username'] = email
            if email == 'admin':
                session['admin'] = True
            # Redirect the user to a secure page.
            session['message'] = msg
            return redirect('/')
        else:
            # If the credentials are invalid, show an error message on the login page.
            return render_template('login.html', message=msg)
    else:
        # If the request method is GET, render the login page.
        return render_template('login.html')
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    branch = None
    if 'branch' in session:
        branch = session['branch']
    # Clear the session variables to log the user out
    session.clear()
    if branch is not None:
        session['branch'] = branch
    # Redirect to the login page
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(port=8080)
    
    