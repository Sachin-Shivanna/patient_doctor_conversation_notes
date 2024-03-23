from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from redis import Redis #pip install rq apscheduler redis
from models.diarization_model.audio_diarization import audio_diarization
from audio_diarization_schedule_helper import getAllFiles

# Connect to Redis server
redis_conn = Redis()

# Set up the RQ queue
queue = Queue(connection=redis_conn)

# Set up the scheduler
scheduler = BlockingScheduler()

filesDictToProcess = getAllFiles()

def queue_job():
    # Create an instance of your class
    audio_diarization_job = audio_diarization(filesDictToProcess)
    # This adds the job's run method to the RQ queue
    print("Adding a job to the queue.")
    queue.enqueue(audio_diarization_job.run)

# Add the job to the APScheduler (for example, to run every 10 seconds)
scheduler.add_job(queue_job, 'interval', seconds=10)


# Start the scheduler
print("Starting the scheduler...")
scheduler.start()

#rq worker
#python audio_diarization_schedule.py