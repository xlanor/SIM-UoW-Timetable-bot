from cfg import Configuration
import Models.db_models as db_model
from typing import Dict
from typing import List
import calendar

mdb = db_model.MongoDB().db

def insert_into_new_db(constructed_record:Dict):
    new_db = mdb.tgbot_records.insert(constructed_record)

def get_old_records()->List:
    return mdb.old_db.find({})

def mutate_record(initial_record:Dict)->Dict:
    new_dict = {}
    try:
        new_dict["telegram_id"] = initial_record["telegram_id"]
        new_dict["username"] = initial_record["user_name"]
        new_dict["name"] = initial_record["name"]
        new_dict["encrypted_pass"] = initial_record["encrypted_pass"]
        new_dict["class_list"] = initial_record["class_name"]
        """
            "class_name" : "CSIT 110 - Fundamental Programming w Pyth",
            "date" : ISODate("2018-10-02T00:00:00.000Z"),
            "day" : "Tuesday",
            "numeric_day" : 1,
            "start_time" : ISODate("2018-10-02T08:30:00.000Z"),
            "end_time" : ISODate("2018-10-02T11:30:00.000Z"),
            "location" : "HQ BLK B LT B.5.03",
            "type" : "Lecture"
        vs
            "date" : ISODate("2017-07-11T00:00:00.000Z"),
            "name" : "ISIT 100 - System Analysis",
            "type" : "Lecture",
            "end_time" : ISODate("2017-07-11T18:30:00.000Z"),
            "location" : "HQ BLK A LT A.3.09C",
            "start_time" : ISODate("2017-07-11T15:30:00.000Z")
        """
        for class_dict in new_dict["class_list"]:
            class_dict["numeric_day"] = class_dict["date"].weekday()
            class_dict["day"] = calendar.day_name[class_dict["numeric_day"]]
            class_dict["class_name"] = class_dict["name"]
            del class_dict["name"]
        
        try:
            initial_record["alert"]
        except KeyError:
            new_dict["alert"] = True
        else:
            new_dict["alert"] = initial_record["alert"]
        
        try:
            initial_record["nightly_alert"]
        except KeyError:
            new_dict["nightly_alert"] = True
        else:
            new_dict["nightly_alert"] = initial_record["nightly_alert"]
        
        try:
            initial_record["alert"]
        except KeyError:
            new_dict["alert"] = True
        else:
            new_dict["alert"] = initial_record["alert"]
        return new_dict
    except KeyError as ke:
        print(ke)
        # skips any of those which does not have non-replaceable fields.
        # they will not be compatible with the new db structure.
        pass
if __name__ == "__main__":
    oldr = get_old_records()
    count = 0
    new_records = []
    for record in oldr:
        count += 1
        mutated = mutate_record(record)
        new_records.append(mutated)
    new_count = 0
    for new in new_records:
        if new:
            insert_into_new_db(new)
            new_count += 1
    print (f"{count} records processed")
    print (f"{new_count} records processed")