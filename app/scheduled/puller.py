import feedparser
import constant
import schedule


def make_pull(url: str) -> {}:
    """
    make_pull receives a URL linking to an RSS feed with relevant grant data to be acquired.
    The obtained data is then filtered to only include grants relevant to Puerto Rico and
    nonprofits. Returns a map with entries for the relevant columns, each containing a list of entries
    :type url: str
    :returns {}
    """
    feed = feedparser.parse(url, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/86.0.4240.183 Safari/537.36')
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


def job():
    print('example')


def job2():
    make_pull(constant.RSS_FEED_MOD_OP)


if __name__ == '__main__':
    schedule.every().day.at("13:52").do(job)
    schedule.every().day.at("13:53").do(job2)

    while True:
        schedule.run_pending()
