import pymongo, sys
from datetime import datetime, timedelta

def get_week_schedule(date, location):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    query = {"Start Time": {"$gte": start_of_week, "$lte": end_of_week}, "Location": location}
    schedule = list(db.classes.find(query))
    
    for s in schedule:
        del s["_id"]
        del s["Location"]
        del s["Enrolled"]
    schedule.sort(key=lambda x: x['Start Time']) 
    
    return schedule

def get_classes(email):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    query = {"Enrolled": email}
    classes = list(db.classes.find(query))
    past_classes = []
    future_classes = []
    
    for c in classes:
        del c["_id"]
        del c["Enrolled"]

        start_time = datetime.strptime(str(c["Start Time"]), '%Y-%m-%d %H:%M:%S')
        if start_time < datetime.now():
            past_classes.append(c)
        else:
            future_classes.append(c)

    past_classes.sort(key=lambda x: x['Start Time'])
    future_classes.sort(key=lambda x: x['Start Time'])

    return past_classes, future_classes

def register_member(name, email, password, gender, date_of_birth, membership):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    db.members.insert_one({"name": name, "email": email, "gender": gender, "date_of_birth": date_of_birth, "membership": membership})
    db.credentials.insert_one({"email":email, "password":password})

def trial_signup(name, email, password):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    db.trials.insert_one({"name": name, "email": email, "password": password, "date": datetime.utcnow()})

def validate_credentials(email, password):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    t = list(db.credentials.find({"email":email}))
    if t != [] and t[0]['password'] == password:
        return True, "Welcome"
    else:
        t = list(db.trials.find({"email":email}))
        trial_time_in_minutes = 5
        if t!=[] and t[0]['password'] == password and datetime.utcnow()-t[0]['date'] <= timedelta(minutes=trial_time_in_minutes):
            return True , f"Welcome! Time left on your trial: {trial_time_in_minutes - round((datetime.utcnow() - t[0]['date']).total_seconds() / 60)} minutes"
        else:
            if t==[]:
                return False, "Wrong Password"
            else:
                return False, "Your trial is over!"
    
def retrieve_instructors():
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    return db.classes.distinct("Instructor")
    
def retrieve_instructor_classes(instructor):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    return db.classes.distinct("Class", {"Instructor": instructor})
    
def retrieve_average_enrolls(instructor, date=None):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    if date==None:
        classes = list(db.classes.find({"Instructor": instructor}))
    else:
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        query = {"Start Time": {"$gte": start_of_week, "$lte": end_of_week}, "Instructor": instructor}
        classes = list(db.classes.find(query))
    sum = 0
    for c in classes:
        sum += len(c['Enrolled'])
    if len(classes) == 0:
        return 0, 0
    return round(sum / len(classes), 2), len(classes)
    
def retrieve_analytics():
    instructors = retrieve_instructors()
    list = []
    for i, ins in enumerate(instructors):
        e_all_time, c_all_time = retrieve_average_enrolls(ins)
        e_this_week, c_this_week = retrieve_average_enrolls(ins, datetime.utcnow())
        list.append({"Name": ins, "Classes": retrieve_instructor_classes(ins), 
                     "Average Enrolls (All time)": e_all_time, "# of Classes (All time)": c_all_time,
                     "Average Enrolls (This week)": e_this_week, "# of Classes (This week)": c_this_week})
    
    return list
    
def check_in(email, time):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    update = {"$push": {"checkins": {"time": time, "type": "checkin"}}}
    db.entries.update_one({"email": email}, update, upsert=True)

def check_out(email, time):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    update = {"$push": {"checkins": {"time": time, "type": "checkout"}}}
    db.entries.update_one({"email": email}, update, upsert=True)
    
def register_to_class(item_id, week_offset, branch, email):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    time = datetime.utcnow() + timedelta(weeks=week_offset)
    start_of_week = time - timedelta(days=time.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    query = {"Start Time": {"$gte": start_of_week, "$lte": end_of_week}, "Location": branch}
    schedule = list(db.classes.find(query))
    schedule.sort(key=lambda x: x['Start Time']) 
    id = schedule[int(item_id)]['_id']
    db.classes.update_one({"_id": id },{ "$addToSet": { "Enrolled": email } })

def deregister_class(item_id, email):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    query = {"Enrolled": email}
    classes = list(db.classes.find(query))
    future_classes = []
    for c in classes:
        start_time = datetime.strptime(str(c["Start Time"]), '%Y-%m-%d %H:%M:%S')
        if start_time >= datetime.now():
            future_classes.append(c)
    future_classes.sort(key=lambda x: x['Start Time'])
    id = future_classes[int(item_id)]['_id']
    db.classes.update_one({"_id": id },{ "$pull": { "Enrolled": email } })
    
def log_workout(email, treadmill, cycling, stair_machine, weight_training):
    time = datetime.utcnow()
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    update = {"Date": time, "Treadmill": treadmill, "Cycling": cycling, "Stair Machine": stair_machine, "Weight Training": weight_training, "Weight Training": weight_training}
    db.entries.update_one({"email": email}, {"$push": {"workout": update}}, upsert=True)
 
def get_activity_summary(email, days=7):
    client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
    db = client["sjsports_db"]
    user = db.entries.find_one({"email": email})
    if user is not None:
        workouts = user['workout']
        if days > 0:
            cutoff_date = datetime.now() - timedelta(days=days)
            workouts = [w for w in workouts if w['Date'] >= cutoff_date]
        workouts.sort(key=lambda x: x['Date'], reverse=True)
        for w in workouts:
            w['Date'] = w['Date'].date()
        return workouts
    else:
        return [{"Date":"", "Treadmill":"", "Cycling":"", "Stair Machine":"", "Weight Training":""}]

# def get_average_workouts():
#     client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
#     db = client["sjsports_db"]
#     # db.entries.aggregate([{ "$group": { avgTreadmil: { "$avg": "$workout.Treadmill" }}}])
    