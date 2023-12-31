import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "Your DB URL"
})

ref = db.reference('Students')

data = {
    "1": {
        "name": "Taha HA",
        "major": "Business",
        "starting_year": 2017,
        "total_attendance": 6,
        "standing": 6,
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },

    "2": {
        "name": "Farah Riahi",
        "major": "Computer Sc",
        "starting_year": 2016,
        "total_attendance": 5,
        "standing": 1,
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },


    "3": {
        "name": "Mark Zuckerberg",
        "major": "Computer Sc",
        "starting_year": 2018,
        "total_attendance": 6,
        "standing": 6,
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },

    "4": {
        "name": "Harry Poter",
        "major": "Magic",
        "starting_year": 2017,
        "total_attendance": 6,
        "standing": 6,
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },

    "5": {
        "name": "Elon Musk",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 8,
        "standing": 6,
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}

for key,value in data.items() :
    ref.child(key).set((value))
