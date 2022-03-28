import constant
import feedparser
import pickle
from puller import make_pull


def initiate_pull_and_process_layers():
    """
    This is the function that orchestrates and manages all scheduled jobs (such as pulling, processing,
    persistence, etc) and will be run a given amount of times per day.
    """
    feedparser.USER_AGENT = constant.USER_AGENT
    # open a pickle file
    filename = 'mypickle.pk'
    with open(filename, 'wb') as file:
        # dump your data into the file
        pickle.dump('', file)
    print(len(make_pull(constant.RSS_FEED_MOD_OP)))
