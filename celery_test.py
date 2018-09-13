from celery import Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def test_message(bot,update):
    print("MESSAAGE RECEIVED")
    chat_id = update.message.chat_id
    for i in range(10):
        bot.send_message(chat_id= chat_id, text = "Hi, yoona!")