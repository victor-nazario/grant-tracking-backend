from datetime import datetime
from typing import Union


def obtain_close_date(entry: str) -> Union[datetime, None]:
    """
    Given a string description for a grant entry, this function returns a datetime
    obtained from its body, if the date cannot be parsed successfully a None type will be returned
    :type entry: str
    :returns a datetime object representing the date or None if not able to parse
    """
    try:
        unprocessed = entry.partition("Close Date:</td><td>")[2].partition("</td></tr><tr><td>")[0]
        date_string = unprocessed[0:13].strip()
        return datetime.strptime(date_string, '%b %d, %Y')
    except ValueError:
        return None
