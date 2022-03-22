from datetime import datetime


def obtain_close_date(entry: str) -> datetime:
    date_string = entry.partition("Close Date:</td><td>")[2].partition("</td></tr><tr><td>")[0].strip()
    return datetime.strptime(date_string, '%b %d, %Y')
