import feedparser

from app.scheduled.layers import constant


def make_pull(url: str, previous_etag: str) -> []:
    """
    make_pull receives a URL linking to an RSS feed with relevant grant data to be acquired.
    The obtained data is then filtered to only include api relevant to Puerto Rico and
    nonprofits. Returns a map with entries for the relevant columns, each containing a list of entries
    :param previous_etag: Str representing the prev. known etag of the RSS. Used to identify if feed is already parsed.
    :param url: The url where the feed to pull is available
    :returns {}
    """
    try:
        feed = feedparser.parse(url, etag=previous_etag)

        if feed.status == 304:
            return 304

        entry_list = []

        for entry in feed.entries:
            if constant.NON_PROFITS_SEARCH_TERM in str(entry.content[0]['value']).lower() \
                    and constant.PR_SEARCH_TERM in str(entry.content[0]['value']).lower():
                entry_list.append({
                    'title': entry.title,
                    'content': entry.content,
                    'link': entry.link,
                    'etag': feed.etag,
                    'opp_num': entry.description
                })

        return entry_list

    except ConnectionResetError:
        return []
