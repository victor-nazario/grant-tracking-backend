import string
import random
import pickle


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
    file_name = 'mypickle.pk'
    with open(file_name, 'wb') as etag_file:
        # dump your data into the file
        pickle.dump(generate_random_string(20), etag_file)
