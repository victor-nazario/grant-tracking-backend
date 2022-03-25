import feedparser
import constant
import schedule
import pickle


def make_pull(url: str) -> []:
    """
    make_pull receives a URL linking to an RSS feed with relevant grant data to be acquired.
    The obtained data is then filtered to only include grants relevant to Puerto Rico and
    nonprofits. Returns a map with entries for the relevant columns, each containing a list of entries
    :type url: str
    :returns {}
    """
    try:
        # load your data back to memory when you need it
        with open('mypickle.pk', 'rb') as etag_file:
            previous_etag = pickle.load(etag_file)

        feed = feedparser.parse(url, etag=previous_etag)
        if feed.status == 304:
            print(feed.status)
            print(feed.etag)
            return feed.feed

        # open a pickle file
        file_name = 'mypickle.pk'
        with open(file_name, 'wb') as etag_file:
            # dump your data into the file
            pickle.dump(feed.etag, etag_file)

        entry_list = []

        for entry in feed.entries:
            if constant.NON_PROFITS_SEARCH_TERM in str(entry.content[0]['value']).lower() \
                    and constant.PR_SEARCH_TERM in str(entry.content[0]['value']).lower():

                entry_list.append({
                    'title': entry.title,
                    'content': entry.content,
                    'link': entry.link
                })

        return entry_list

    except ConnectionResetError:
        print("connection err")  # Needs proper logging
        return {}


def job():
    print('example')


def job2():
    print(len(make_pull(constant.RSS_FEED_MOD_OP)))


if __name__ == '__main__':
    feedparser.USER_AGENT = constant.USER_AGENT

    # open a pickle file
    filename = 'mypickle.pk'
    with open(filename, 'wb') as file:
        # dump your data into the file
        pickle.dump('', file)

    schedule.every(10).seconds.do(job2)

    while True:
        schedule.run_pending()
