from Models.db_models import MongoDB
def test_db():
    mongo = MongoDB()
    rec = mongo.db.tgbot_records.find({})
    for r in rec:
        print(r)

if __name__== "__main__":
    test_db()