import schedule
from job import initiate_pull_and_process_layers
from models import init_db

if __name__ == '__main__':
    init_db()
    schedule.every(10).seconds.do(initiate_pull_and_process_layers)
    while True:
        schedule.run_pending()
