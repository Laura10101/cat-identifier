"""
Main module for the Celery worker process.
Sets up the Celery worker, enabling it to handle requests to start
the training process.
"""
import sys
import os
import gc

from factories import make_celery_worker
sys.dont_write_bytecode = True

#import the env file if it exists
if os.path.exists("env.py"):
    import env

celery = make_celery_worker(os.environ.get("REDIS_URL"))

print("Worker Started. Clearing garbage...")
print("Before: " + str(gc.get_count()))
gc.collect()
print("After: " + str(gc.get_count()))
