from celery import Celery
from celery import current_app
app = Celery('queue',
             broker='amqp://',
             backend='amqp://',
             include=['Controllers.celery_queue'])

process_order = app.signature('Controllers.celery_queue.register_user')
user = {}
user["user_id"] = "test",
user["username"] = "username",
user["password"] = "password",
user["name"] = "name"
user["encrypted_password"] = "12345"
process_order.delay(user,"b")
#result = process_order.delay("test")  # standard calling api works
#print(result)#