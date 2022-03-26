import schedule
from app.scheduled.puller import job2

if __name__ == '__main__':
    schedule.every(10).seconds.do(job2)
    while True:
        schedule.run_pending()


