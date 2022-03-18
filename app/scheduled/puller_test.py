from puller import make_pull
import constant


def test_make_pull():
    assert len(make_pull(constant.RSS_FEED_NEW_OP)['title'][0]) > 0, "Length of returned list should be greater than 0"


if __name__ == '__main__':
    test_make_pull()
