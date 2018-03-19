
import pymongo
from pymongo import MongoClient
IP_ADDRESS='localhost'

def insert_employee(obj):
        client = MongoClient()
        client = MongoClient(IP_ADDRESS, 27017)
        db = client.cv_db
        collection = db.employee_data

        posts = db.posts

        post_id = db.employee_data.insert_one(obj).inserted_id
        client.close()

def find_skill_list(skillsList):
        client = MongoClient()
        client = MongoClient(IP_ADDRESS, 27017)
        db = client.cv_db
        query='result=list(db.employee_data.find({"$and":['
        for skill in skillsList:
            query+='{"techSkills.skillName":"'+skill['name']+'"},'
        query+=']},{"_id": 0}))'

        result={"result":None,"db":db}
        exec(query,result)
        client.close()
        result=result["result"]
        final=[]
        for r in result:
                flg = False
                for skill in r["techSkills"]:
                        for temp in skillsList:
                                if skill["skillName"]==temp['name'] and skill["skillExp"]<temp['exp']:
                                        flg=True
                if not flg:
                        final.append(r)
        return final

def update_status(id):
        client = MongoClient()
        client = MongoClient(IP_ADDRESS, 27017)
        db = client.cv_db
        db.employee_data.update_one({"id": id}, {"$set": {"status": "unavailable"}})
        client.close()

def update_team_status(team):
        for emp in team:
                update_status(emp["id"])




