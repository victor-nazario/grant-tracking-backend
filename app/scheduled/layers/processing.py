from datetime import datetime
from typing import Union


def obtain_close_date(entry: str) -> Union[int, None]:
    """
    Given a string description for a grant entry, this function returns a datetime
    obtained from its body, if the date cannot be parsed successfully a None type will be returned
    :type entry: str
    :returns a datetime object representing the date or None if not able to parse
    """
    try:
        unprocessed = entry.partition("Close Date:</td><td>")[2].partition("</td></tr><tr><td>")[0]
        date_string = unprocessed[0:13].strip()
        dt = datetime.strptime(date_string, '%b %d, %Y')
        return int(dt.timestamp())
    except ValueError:
        return None


def erase_b_tags(opportunity_number: str):
    try:
        return opportunity_number.partition('<b>')[2].partition('</b>')[0]
    except ValueError:
        return None
