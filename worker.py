from factories import make_celery_worker
import sys, os
sys.dont_write_bytecode = True

#import the env file if it exists
if os.path.exists("env.py"):
    import env

celery = make_celery_worker(os.environ.get("REDIS_URL"))