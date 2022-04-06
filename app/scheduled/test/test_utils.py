import string
import random
import pickle
from app.scheduled.layers.puller import make_pull
from datetime import date
from app.scheduled.layers.models import GrantEntry



def generate_random_string(num_characters: int) -> str:
    """
    Creates a random string with 20 characters.
    :return: random string with 20 characters
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(num_characters))
    return random_string


def generate_random_etag() -> str:
    """
    This method creates a a random string and stores it in mypickle.pk to be used as an etag.
    :return: random etag string with 20 characters
    """
    file_name = '../mypickle.pk'
    with open(file_name, 'wb') as etag_file:
        # dump your data into the file
        pickle.dump(generate_random_string(20), etag_file)


def create_grant_objects(url: str, previous_etag: str, is_modified: bool):
    random_etag = generate_random_string(20)
    entry_list = []
    while len(entry_list) <= 0:
        entry_list = make_pull(url, previous_etag)
    grant_list = []
    for entry in entry_list:
        grant_list.append(GrantEntry(title=entry['title'], opp_num=entry['opp_num'],
                                     content=entry['content'][0]['value'], link=entry['link'],
                                     close_date=date(2022, 8, 20), modified=is_modified,
                                     etag=random_etag))
    return grant_list, random_etag
