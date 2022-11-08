from factories import make_celery_worker
import sys, os, gc
sys.dont_write_bytecode = True

#import the env file if it exists
if os.path.exists("env.py"):
    import env

celery = make_celery_worker(os.environ.get("REDIS_URL"))

print("Worker Started. Clearing garbage...")
print("Before: " + str(gc.get_count()))
gc.collect()
print("After: " + str(gc.get_count()))