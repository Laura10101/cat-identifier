from celery import Celery
import sys, os
sys.dont_write_bytecode = True

#import the env file if it exists
if os.path.exists("env.py"):
    import env

#Inspired by StackOverflow: https://stackoverflow.com/questions/22172915/relative-imports-require-the-package-argument
def make_celery_worker(broker_url):
    return Celery(
        "flask-celery-app",
        broker=broker_url,
        include=["blueprints.apis.training_image.tasks"]
    )

worker = make_celery_worker(os.environ.get("REDIS_URL"))