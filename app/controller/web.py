import requests
import random

from bs4 import BeautifulSoup
from .exceptions import InvalidCourseException

URL_TEMPLATE = 'https://courses.students.ubc.ca/cs/courseschedule?' \
               'sesscd={}&pname=subjarea&tname=subj-section&sessyr={}&dept={}&course={}&section={}'


def get_course_page_url(course):
    return URL_TEMPLATE.format(*course.split())


# From https://www.jcchouinard.com/random-user-agent-with-python-and-beautifulsoup/
def get_ua():
    ua_strings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 "
        "Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 "
        "Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    ]
    return random.choice(ua_strings)


def get_course_seats(course):
    try:
        headers = {'User-Agent': get_ua()}
        r = requests.get(get_course_page_url(course), headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        seats_dict = {}
        for row in soup.find('table', attrs={'class': '\'table'}).contents:
            try:
                seats_dict[row.td.text[0]] = int(row.strong.text)
            except AttributeError:
                pass
            except ValueError:
                pass
        return seats_dict
    except AttributeError:
        if soup.find('div', attrs={'role': 'main'}).text.find("The requested section is either no longer offered"):
            raise InvalidCourseException(
                "Invalid course: section does not exist.")
        raise AttributeError(str(soup.contents))

    except requests.exceptions.ConnectionError:
        raise
