#Celery factory to enable integration between Celery and Flask
#Taken from Flask documentation: https://flask.palletsprojects.com/en/2.2.x/patterns/celery/
#Modified as per Celery documentation: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(broker=app.config["BROKER_URL"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery