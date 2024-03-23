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

def queue_job():

    structured_audio_files_list = getAllFiles()

    diarization_job = []
    for arg_dict in structured_audio_files_list:
        audio_diarization_instance = audio_diarization(**arg_dict)
        job = queue.enqueue(audio_diarization_instance.run)
        diarization_job.append(job)
        
    # Enqueue second set of jobs, each depending on the corresponding first job
    '''for i, arg_dict in enumerate(second_job_args):
        job_instance = MySecondJob(**arg_dict)
        # Each second job depends on the corresponding first job
        queue.enqueue(job_instance.run, depends_on=first_jobs[i])'''

# Add the job to the APScheduler to run at the 45th minute of every hour
scheduler.add_job(queue_job,  'cron', minute=45)


# Start the scheduler
print("Starting the scheduler...")
scheduler.start()

#rq worker
#python audio_diarization_schedule.py