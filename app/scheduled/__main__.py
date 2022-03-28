import schedule
from job import initiate_pull_and_process_layers

if __name__ == '__main__':
    schedule.every(10).seconds.do(initiate_pull_and_process_layers)
    while True:
        schedule.run_pending()
