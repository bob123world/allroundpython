from celery import Celery

# docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

app = Celery('tasks', broker='pyamqp://guest@localhost')

@app.task
def add(x, y):
    return x + y