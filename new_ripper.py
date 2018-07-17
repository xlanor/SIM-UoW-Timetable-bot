import json
from Controllers.Ripper.ripper import RipperFactory
user_to_load = input("Enter a user to load: (ray|jk|yz|fail|vi) : ")
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
        method = input("What type of test would you like to perform? (Rip | Login | Other | NewRip: ")  # noqa
        obj = RipperFactory.get_ripper(method,username,password)
        result = obj.execute()

        if method == "Rip":
            for cl in result:
                print(cl.get_dict())
       