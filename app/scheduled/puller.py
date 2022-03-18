import feedparser
import constant
import schedule


def make_pull(url: str):
    feed = feedparser.parse(url)
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
    print(len(data['link']))


def job():
    print('example')


def job2():
    make_pull(constant.RSS_FEED_MOD_OP)


if __name__ == '__main__':
    schedule.every().day.at("13:52").do(job)
    schedule.every().day.at("13:53").do(job2)

    while True:
        schedule.run_pending()
