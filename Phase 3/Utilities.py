from pymongo import MongoClient
import os
from dotenv import load_dotenv


class Utilities:
    # connects my cluster to the database
    @staticmethod
    def startup():
        #change cluster to your string from atlas accordingly
        load_dotenv()
        cluster = os.environ["MONGODB_URI"]
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
