import pickle

import feedparser

from app.scheduled import constant

etag_dict = {
    'new_op_etag': '',
    'mod_op_etag': ''
}


def make_pull(url: str, previous_etag: str) -> []:
    """
    make_pull receives a URL linking to an RSS feed with relevant grant data to be acquired.
    The obtained data is then filtered to only include grants relevant to Puerto Rico and
    nonprofits. Returns a map with entries for the relevant columns, each containing a list of entries
    :param previous_etag: Str representing the prev. known etag of the RSS. Used to identify if feed is already parsed.
    :param url: The url where the feed to pull is available
    :returns {}
    """
    try:
        feed = feedparser.parse(url, etag=previous_etag)
        if url is constant.RSS_FEED_NEW_OP:
            etag_dict['new_op_etag'] = feed.etag
        else:
            etag_dict['mod_op_etag'] = feed.etag

        if feed.status == 304:
            print(feed.status)
            print(feed.etag)
            return feed.feed

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


if __name__ == '__main__':
    # load your data back to memory when you need it
    with open('mypickle.pk', 'rb') as etag_file:
        etag_dict_loaded = pickle.load(etag_file)
        print(etag_dict_loaded)
        print(len(make_pull(constant.RSS_FEED_NEW_OP, etag_dict_loaded['new_op_etag'])))
        print(len(make_pull(constant.RSS_FEED_MOD_OP, etag_dict_loaded['mod_op_etag'])))

    # open a pickle file
    file_name = 'mypickle.pk'
    with open(file_name, 'wb') as etag_file:
        # dump your data into the file
        pickle.dump(etag_dict, etag_file)
