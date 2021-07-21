import imp
from imutils import paths
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

previous_image = 0
# job schedule event
def job():
    global previous_image
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    imagePaths = list(paths.list_images('dataset'))
    current_image = int(len(imagePaths))
    print(time,'Current photos',len(imagePaths))
    if current_image != previous_image:
        print('Detect photos change,Training Again!')
        imp.load_source('a','extract_embeddings.py')
        imp.load_source('b','train_model.py')
        previous_image = current_image
        f = open("status.txt","w")
        f.write('change')
        f.close()
        print('file close')

    previous_image = current_image
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval',seconds=5)
scheduler.start()