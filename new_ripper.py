import json
from Controllers.Ripper.login import SIMConnect
from Controllers.Ripper.timetable import RipTimeTable
user_to_load = input("Enter a user to load: (ray|jk|yz|fail) : ")
with open("testing_accounts.json") as json_file:
    data = json.load(json_file)
    try:
        data[user_to_load]
    except KeyError:
        print("Cannot find data in file")
        sys.exit()
    else:
        username = data[user_to_load]["username"]
        password = data[user_to_load]["password"]
        method = input("What type of test would you like to perform? (rip | login): ")  # noqa
        if method == "rip":
            list_of_classes = (RipTimeTable(username, password).execute())
            for cl in list_of_classes:
                print(cl.get_dict())
        elif method == "login":

            SIMConnect(username,password).execute()
            #print(LoginTest(username, password).execute())
        else:
            print("Unknown method")