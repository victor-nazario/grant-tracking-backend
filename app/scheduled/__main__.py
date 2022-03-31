import schedule
from job import initiate_pull_and_process_layers
from models import init_db
from deletion import delete_grant

if __name__ == '__main__':
    init_db()
    schedule.every(10).seconds.do(initiate_pull_and_process_layers)
    schedule.every(20).seconds.do(delete_grant)
    while True:
        schedule.run_pending()
