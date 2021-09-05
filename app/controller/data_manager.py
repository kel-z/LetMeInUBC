import re
import json

from .. import models
from . import web


class InvalidCourseException(Exception):
    pass


class InvalidContactException(Exception):
    pass


class InvalidFormException(Exception):
    pass

def verify_course(course_string):
    if not isinstance(course_string, str):
        raise InvalidCourseException(
            'Invalid course value: course value should be string')

    course_data = course_string.split()

    if len(course_data) != 5:
        raise InvalidCourseException(
            'Invalid course value: invalid course string format')

    session = course_data[0]
    year = course_data[1]
    dept = course_data[2]
    course = course_data[3]
    section = course_data[4]

    if session not in ['W', 'S']:
        raise InvalidCourseException(
            'Invalid course value: invalid course session.')

    if len(year) != 4 or not year.isdigit():
        raise InvalidCourseException(
            'Invalid course value: invalid course year.')

    if len(dept) != 4:
        raise InvalidCourseException(
            'Invalid course value: invalid course department.')

    if len(course) != 3 or not course.isdigit():
        raise InvalidCourseException(
            'Invalid course value: invalid course number.')

    if len(section) != 3:
        raise InvalidCourseException(
            'Invalid course value: invalid course section ID.')

    return course_string.upper()


def verify_contact(contact):
    if not isinstance(contact, dict):
        raise InvalidContactException(
            'Invalid contact: contact should be dict.')

    sms = contact.get('sms')
    email = contact.get('email')

    if not sms and not email:
        raise InvalidContactException(
            'Invalid contact: missing contact information.')

    if sms:
        if len(sms) != 10 or not sms.isdigit():
            raise InvalidContactException(
                'Invalid contact: invalid SMS number.')

    if email:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise InvalidContactException(
                'Invalid contact: invalid email address.')
    else:
        raise InvalidContactException(
            'Invalid contact: must include email address.')

    return {
        'sms': sms,
        'email': email
    }


class App():
    def __init__(self):
        print("Init " + str(self))
        # self.data = {}
        # self.load_data()

    def handle_form_data(self, form_data):
        if not isinstance(form_data, dict):
            raise InvalidFormException('Invalid form data: should be dict.')

        if not isinstance(form_data.get('only_general'), bool):
            raise ValueError(
                'Invalid form data: invalid or missing only_general value.')

        try:
            course = verify_course(form_data.get('course'))
            contact = verify_contact(form_data.get('contact'))
            web.get_course_seats(course)

            if course and contact:
                model = models.Contact.objects.update_or_create(course_string=course, email=contact.get('email'), defaults={'course_string': course, 'only_general': form_data.get('only_general'), **form_data.get('contact')})

        except InvalidCourseException:
            raise

        except InvalidContactException:
            raise

        except InvalidFormException:
            raise

        except AttributeError as e:
            print(e)
            raise AttributeError("Invalid form data: Unknown error.")
