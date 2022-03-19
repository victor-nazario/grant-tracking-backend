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
    try:
        feed = feedparser.parse(url)

        data = {}
        # print(feed.updated_parsed)

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
    print(len(make_pull(constant.RSS_FEED_MOD_OP)))


if __name__ == '__main__':
    feedparser.USER_AGENT = constant.USER_AGENT
    schedule.every(10).seconds.do(job2)

    while True:
        schedule.run_pending()
