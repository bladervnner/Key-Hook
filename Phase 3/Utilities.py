import getpass
from pymongo import MongoClient


class Utilities:
    # connects my cluster to the database
    @staticmethod
    def startup():
        #print("Prompting for the password.")
        #password = getpass.getpass(prompt='MongoDB password --> ')

        #change cluster to your string from atlas accordingly
        cluster = "mongodb+srv://rafiks7:test@cluster0.k70iogb.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster)
        db = client.Hook_Project
        return db
'''
# draws the student id from a student document
    @staticmethod
    def get_student_id(db, student_id):
        result = db.students.find_one({"student_id": student_id})['_id']
        return result
'''
