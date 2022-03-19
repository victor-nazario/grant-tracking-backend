import feedparser
import constant
import schedule
import pickle


def make_pull(url: str) -> {}:
    """
    make_pull receives a URL linking to an RSS feed with relevant grant data to be acquired.
    The obtained data is then filtered to only include grants relevant to Puerto Rico and
    nonprofits. Returns a map with entries for the relevant columns, each containing a list of entries
    :type url: str
    :returns {}
    """
    try:
        # load your data back to memory when you need it
        with open('mypickle.pk', 'rb') as fi:
            previous_etag = pickle.load(fi)
        print(previous_etag)

        feed = feedparser.parse(url, agent='Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; '
                                           'feed-id=8639390370582375869)', etag=previous_etag)
        if feed.status == 304:
            print(feed.status)
            print(feed.etag)
            return feed.feed

        # open a pickle file
        filename = 'mypickle.pk'
        with open(filename, 'wb') as fi:
            # dump your data into the file
            pickle.dump(feed.etag, fi)
        data = {}

        for entry in feed.entries:
            if constant.NON_PROFITS_SEARCH_TERM in str(entry.content[0]['value']).lower() \
                    and constant.PR_SEARCH_TERM in str(entry.content[0]['value']).lower():
                data.setdefault('title', [])
                data.setdefault('content', [])
                data.setdefault('link', [])
                data['title'].append(entry.title)
                data['content'].append(entry.content)
                data['link'].append(entry.link)
        return data

    except ConnectionResetError:
        print("connection err")  # Needs proper logging
        return {}


def job():
    print('example')


def job2():
    # print(len(make_pull(constant.RSS_FEED_MOD_OP, feed_etag=etag)))
    print(len(make_pull(constant.RSS_FEED_MOD_OP)))


if __name__ == '__main__':
    initial_feed = feedparser.parse(constant.RSS_FEED_MOD_OP,
                            agent='Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; '
                                  'feed-id=8639390370582375869)')

    # open a pickle file
    filename = 'mypickle.pk'
    with open(filename, 'wb') as fi:
        # dump your data into the file
        pickle.dump(initial_feed.etag, fi)

    # schedule.every(10).seconds.do(job2, etag=initial_feed.etag)
    schedule.every(10).seconds.do(job2)
    while True:
        schedule.run_pending()
