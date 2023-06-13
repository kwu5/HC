import pymongo, random
from datetime import datetime, timedelta

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
db = client["sjsports_db"]

# Reset the collection
collection = db["classes"]
collection.drop()

# Add mock data
classes = [
    {"Class": "Yoga", "Instructor": "John", "Start Time": "2023-05-07T08:00:00Z", "End Time": "2023-05-07T09:00:00Z", "Capacity": 10, "Location": "San Jose", "Enrolled": []},
    {"Class": "Spinning", "Instructor": "Sarah", "Start Time": "2023-05-07T09:30:00Z", "End Time": "2023-05-07T10:30:00Z", "Capacity": 15, "Location": "San Jose", "Enrolled": []},
    {"Class": "Pilates", "Instructor": "Mary", "Start Time": "2023-05-07T11:00:00Z", "End Time": "2023-05-07T12:00:00Z", "Capacity": 8, "Location": "San Jose", "Enrolled": []},
    {"Class": "Zumba", "Instructor": "Tom", "Start Time": "2023-05-07T13:00:00Z", "End Time": "2023-05-07T14:00:00Z", "Capacity": 20, "Location": "San Jose", "Enrolled": []},
    {"Class": "Crossfit", "Instructor": "Mike", "Start Time": "2023-05-07T15:00:00Z", "End Time": "2023-05-07T16:00:00Z", "Capacity": 12, "Location": "San Jose", "Enrolled": []},
    {"Class": "Boxing", "Instructor": "David", "Start Time": "2023-05-10T08:00:00Z", "End Time": "2023-05-10T09:00:00Z", "Capacity": 10, "Location": "San Jose", "Enrolled": []},
    {"Class": "Hatha Yoga", "Instructor": "Emma", "Start Time": "2023-05-10T09:30:00Z", "End Time": "2023-05-10T10:30:00Z", "Capacity": 15, "Location": "San Jose", "Enrolled": []},
    {"Class": "Piloxing", "Instructor": "David", "Start Time": "2023-05-10T11:00:00Z", "End Time": "2023-05-10T12:00:00Z", "Capacity": 8, "Location": "San Jose", "Enrolled": []},
    {"Class": "Kickboxing", "Instructor": "Kevin", "Start Time": "2023-05-16T08:00:00Z", "End Time": "2023-05-16T09:00:00Z", "Capacity": 10, "Location": "San Jose", "Enrolled": []},
    {"Class": "Aerial Yoga", "Instructor": "John", "Start Time": "2023-05-16T09:30:00Z", "End Time": "2023-05-16T10:30:00Z", "Capacity": 15, "Location": "San Jose", "Enrolled": []},
    {"Class": "BodyPump", "Instructor": "Grace", "Start Time": "2023-05-11T11:00:00Z", "End Time": "2023-05-11T12:00:00Z", "Capacity": 8, "Location": "San Jose", "Enrolled": []},
    {"Class": "Spinning", "Instructor": "Brian", "Start Time": "2023-05-12T08:00:00Z", "End Time": "2023-05-12T09:00:00Z", "Capacity": 10, "Location": "San Jose", "Enrolled": []},
    {"Class": "Zumba", "Instructor": "Sarah", "Start Time": "2023-05-12T09:30:00Z", "End Time": "2023-05-12T10:30:00Z", "Capacity": 15, "Location": "San Jose", "Enrolled": []},
    {"Class": "Boot Camp", "Instructor": "Grace", "Start Time": "2023-05-12T11:00:00Z", "End Time": "2023-05-12T12:00:00Z", "Capacity": 8, "Location": "San Jose", "Enrolled": []},
    {"Class": "Yoga", "Instructor": "Emma", "Start Time": "2023-05-13T08:00:00Z", "End Time": "2023-05-13T09:00:00Z", "Capacity": 10, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "HIIT", "Instructor": "Grace", "Start Time": "2023-05-13T09:30:00Z", "End Time": "2023-05-13T10:30:00Z", "Capacity": 15, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Barre", "Instructor": "Lena", "Start Time": "2023-05-13T11:00:00Z", "End Time": "2023-05-13T12:00:00Z", "Capacity": 8, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Yoga", "Instructor": "John", "Start Time": "2023-05-08T08:00:00Z", "End Time": "2023-05-08T09:00:00Z", "Capacity": 10, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Spinning", "Instructor": "Sarah", "Start Time": "2023-05-09T09:30:00Z", "End Time": "2023-05-09T10:30:00Z", "Capacity": 15, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Pilates", "Instructor": "Mary", "Start Time": "2023-05-06T11:00:00Z", "End Time": "2023-05-06T12:00:00Z", "Capacity": 8, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Zumba", "Instructor": "Tom", "Start Time": "2023-05-06T13:00:00Z", "End Time": "2023-05-06T14:00:00Z", "Capacity": 20, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Crossfit", "Instructor": "Mike", "Start Time": "2023-05-12T15:00:00Z", "End Time": "2023-05-12T16:00:00Z", "Capacity": 12, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Yoga", "Instructor": "John", "Start Time": "2023-05-15T08:00:00Z", "End Time": "2023-05-15T09:00:00Z", "Capacity": 10, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Spinning", "Instructor": "Sarah", "Start Time": "2023-05-16T09:30:00Z", "End Time": "2023-05-16T10:30:00Z", "Capacity": 15, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Pilates", "Instructor": "Mary", "Start Time": "2023-05-17T11:00:00Z", "End Time": "2023-05-17T12:00:00Z", "Capacity": 8, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Zumba", "Instructor": "Tom", "Start Time": "2023-05-18T13:00:00Z", "End Time": "2023-05-18T14:00:00Z", "Capacity": 20, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Crossfit", "Instructor": "Grace", "Start Time": "2023-05-19T15:00:00Z", "End Time": "2023-05-19T16:00:00Z", "Capacity": 12, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Yoga", "Instructor": "John", "Start Time": "2023-04-30T08:00:00Z", "End Time": "2023-04-30T09:00:00Z", "Capacity": 10, "Location": "Santa Clara", "Enrolled": []},
    {"Class": "Spinning", "Instructor": "Sarah", "Start Time": "2023-05-01T09:30:00Z", "End Time": "2023-05-01T10:30:00Z", "Capacity": 15, "Location": "Santa Clara", "Enrolled": []}
]

enrolled_members_for_classes =[ [], ['johndoe@gmail.com'], ['janedoe@gmail.com'], ['johndoe@gmail.com', 'janedoe@gmail.com'], ['bobsmith@yahoo.com'], ['johndoe@gmail.com', 'bobsmith@yahoo.com'],
['janedoe@gmail.com', 'bobsmith@yahoo.com'], ['johndoe@gmail.com', 'janedoe@gmail.com', 'bobsmith@yahoo.com'], ['emilyjones@emilyjones.com'], ['johndoe@gmail.com', 'emilyjones@emilyjones.com'],
['janedoe@gmail.com', 'emilyjones@emilyjones.com'], ['johndoe@gmail.com', 'janedoe@gmail.com', 'emilyjones@emilyjones.com'], ['bobsmith@yahoo.com', 'emilyjones@emilyjones.com'],
['johndoe@gmail.com', 'bobsmith@yahoo.com', 'emilyjones@emilyjones.com'], ['janedoe@gmail.com', 'bobsmith@yahoo.com', 'emilyjones@emilyjones.com'], ['johndoe@gmail.com', 'janedoe@gmail.com', 'bobsmith@yahoo.com', 'emilyjones@emilyjones.com'],
['tomwilson@sjsu.edu'], ['johndoe@gmail.com', 'tomwilson@sjsu.edu'], ['janedoe@gmail.com', 'tomwilson@sjsu.edu'], ['johndoe@gmail.com', 'janedoe@gmail.com', 'tomwilson@sjsu.edu'], ['bobsmith@yahoo.com', 'tomwilson@sjsu.edu'],
['johndoe@gmail.com', 'bobsmith@yahoo.com', 'tomwilson@sjsu.edu'], ['janedoe@gmail.com', 'bobsmith@yahoo.com', 'tomwilson@sjsu.edu'], ['johndoe@gmail.com', 'janedoe@gmail.com', 'bobsmith@yahoo.com', 'tomwilson@sjsu.edu'],
['emilyjones@emilyjones.com', 'tomwilson@sjsu.edu'], ['johndoe@gmail.com', 'emilyjones@emilyjones.com', 'tomwilson@sjsu.edu'], ['janedoe@gmail.com', 'emilyjones@emilyjones.com', 'tomwilson@sjsu.edu'],
['johndoe@gmail.com', 'janedoe@gmail.com', 'emilyjones@emilyjones.com', 'tomwilson@sjsu.edu'], ['johndoe@gmail.com', 'janedoe@gmail.com']]

for i, c in enumerate(classes):
    c['Start Time'] = datetime.fromisoformat(c['Start Time'].replace('Z', '+00:00'))
    c['End Time'] = datetime.fromisoformat(c['End Time'].replace('Z', '+00:00'))
    c['Enrolled'] = enrolled_members_for_classes[i]

collection.insert_many(classes)

members = [{
    "name": "John Doe",
    "email": "johndoe@gmail.com",
    "gender": "Male",
    "date_of_birth": "1990-01-01",
    "membership_type": "Premium",
},
{
    "name": "Jane Doe",
    "email": "janedoe@gmail.com",
    "gender": "Female",
    "date_of_birth": "1992-03-15",
    "membership_type": "Student",
},
{
    "name": "Bob Smith",
    "email": "bobsmith@yahoo.com",
    "gender": "Male",
    "date_of_birth": "1985-07-21",
    "membership_type": "Premium",
},
{
    "name": "Emily Jones",
    "email": "emilyjones@emilyjones.com",
    "gender": "Female",
    "date_of_birth": "1995-05-10",
    "membership_type": "Student",
},
{
    "name": "Tom Wilson",
    "email": "tomwilson@sjsu.edu",
    "gender": "Male",
    "date_of_birth": "1980-12-31",
    "membership_type": "Premium",
}]

for m in members:
    m['date_of_birth'] = datetime.strptime(m['date_of_birth'], "%Y-%m-%d")
    
db.members.drop()
db.members.insert_many(members)

credentials = [{"email":"johndoe@gmail.com",            "password":"1234"}, 
            {"email":"janedoe@gmail.com",            "password":"1234"},
            {"email":"bobsmith@yahoo.com",           "password":"1234"}, 
            {"email":"emilyjones@emilyjones.com",    "password":"1234"}, 
            {"email":"tomwilson@sjsu.edu",           "password":"1234"},
            {"email":"admin",                        "password":"admin"}]

db.credentials.drop()
db.credentials.insert_many(credentials)

db.trials.drop()

def gen_workout():
    if random.random() < 0.3: 
        return 0
    else:
        return random.randint(15, 60)

def generate_workout_entries():
    past_week_activities = [
        {
            "Date": datetime.now() - timedelta(days=i),
            "Treadmill": gen_workout(),
            "Cycling": gen_workout(),
            "Stair Machine": gen_workout(),
            "Weight Training": gen_workout()
        }
        for i in range(7)
    ]

    past_90_days_activities = []
    for i in range(90):
        if random.random() < 0.3: 
            continue
        past_90_days_activities.append({
            "Date": datetime.now() - timedelta(days=i),
            "Treadmill": gen_workout(),
            "Cycling": gen_workout(),
            "Stair Machine": gen_workout(),
            "Weight Training": gen_workout()
        })
    return past_week_activities, past_90_days_activities

db.entries.drop()

past_week_activities, past_90_days_activities = generate_workout_entries()
# past_week_activities = [act for act in past_week_activities if not act['Treadmill'] == 0 and act['Cycling'] == 0 and act['Stair Machine'] == 0 and act['Weight Training'] == 0]
# past_90_days_activities = [act for act in past_90_days_activities if not act['Treadmill'] == 0 and act['Cycling'] == 0 and act['Stair Machine'] == 0 and act['Weight Training'] == 0]

for activity in past_week_activities:
    db.entries.update_one({"email": "janedoe@gmail.com"}, {"$push": {"workout": activity}}, upsert=True)
for activity in past_90_days_activities:
    db.entries.update_one({"email": "janedoe@gmail.com"}, {"$push": {"workout": activity}}, upsert=True)

past_week_activities, past_90_days_activities = generate_workout_entries()
for activity in past_week_activities:
    db.entries.update_one({"email": "johndoe@gmail.com"}, {"$push": {"workout": activity}}, upsert=True)
for activity in past_90_days_activities:
    db.entries.update_one({"email": "johndoe@gmail.com"}, {"$push": {"workout": activity}}, upsert=True)

past_week_activities, past_90_days_activities = generate_workout_entries()
for activity in past_week_activities:
    db.entries.update_one({"email": "bobsmith@yahoo.com"}, {"$push": {"workout": activity}}, upsert=True)
for activity in past_90_days_activities:
    db.entries.update_one({"email": "bobsmith@yahoo.com"}, {"$push": {"workout": activity}}, upsert=True)


