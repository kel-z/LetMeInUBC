import json

from schedule import Scheduler
import threading
import time

from .controller.exceptions import InvalidContactException, InvalidCourseException, InvalidFormException
from requests.exceptions import ConnectionError
from .controller import web

import os
from twilio.rest import Client 

import smtplib
from email.message import EmailMessage

#Twilio client
account_sid = '' 
auth_token = '' 
client = Client(account_sid, auth_token) 

class Refresh(object):
    def __init__(self):
        print("Init " + str(self))

    def main(self):
        from .models import Contact
        for contact in Contact.objects.raw('SELECT DISTINCT 1 id, course_string FROM app_contact'):
            try:
                self.refresh_and_notify(contact.course_string)
                time.sleep(15)
            except ConnectionError:
                # TODO: handle exception
                pass

    def refresh_and_notify(self, course):
        try:
            print('Refreshing ' + course + '...')

            # leave this commented during debugging so it doesn't actually spam ubc servers
            seats_dict = web.get_course_seats(course)

            # for testing
            # seats_dict = {
            #     'G': 1,     # general seats remaining
            #     'R': 1      # restricted seats remaining
            #     }

            if seats_dict['G'] > 0:
                print("GENERAL SEATS AVAILABLE: " + course)
                from .models import Contact
                sms_arr = []
                email_arr = []
                query = Contact.objects.raw('SELECT id, sms, email FROM app_contact WHERE course_string=\'{}\' AND only_general=TRUE'.format(course))
                for contact in query:
                    sms_arr.append(contact.sms) if contact.sms else None
                    email_arr.append(contact.email)
                contact_dict = {
                    'sms': sms_arr,
                    'email': email_arr
                    }
                notify_contacts(course, contact_dict)
                for contact in query:
                    contact.delete()
            if seats_dict['R'] + seats_dict['G'] > 0:
                print("RESTRICTED SEATS AVAILABLE: " + course)
                from .models import Contact
                sms_arr = []
                email_arr = []
                query = Contact.objects.raw('SELECT id, sms, email FROM app_contact WHERE course_string=\'{}\' AND only_general=FALSE'.format(course))
                for contact in query:
                    sms_arr.append(contact.sms) if contact.sms else None
                    email_arr.append(contact.email)
                contact_dict = {
                    'sms': sms_arr,
                    'email': email_arr
                    }
                notify_contacts(course, contact_dict)
                for contact in query:
                    contact.delete()

        except InvalidCourseException:
            print("Invalid course: " + course)
            from .models import Contact
            Contact.objects.filter(course_string=course).delete()
        except AttributeError as e:
            print(e)
            pass
        except ConnectionError:
            raise

    def debug(self):
        pass

# params: course, sms
# sends sms to a single sms (str)
def notify(course, sms):
    print(sms)
    message = client.messages.create(  
                              messaging_service_sid='', 
                              body= " "+ "LetMeInUBC:" + "There is a spot available for" + " " + course,      
                              to= '+1' + sms 
                          ) 
    print(message.sid)
    pass

def notify_email(course, email):
    msg = EmailMessage()
    msg['Subject'] = 'UBC course avalibility notification'
    msg['From'] = 'Let Me In UBC'
    msg['To'] = email
    print(email)
    msg.set_content("There is a spot available for " + course)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
 
    server.login('', '')
    server.send_message(msg)
    server.quit()
    pass

    

# params: course, contact_dict
#   - course (str) represents a course in string format (e.g. 'W 2021 CPSC 310 101')
#   - contact_dict is a dict with keys 'sms' and 'email', each containing
#     an array of phone numbers and email addresses to notify, respectively.
def notify_contacts(course, contact_dict):
    sms_array = contact_dict['sms']
    for x in sms_array:
        print("sending sms to " + x)
        notify(course, x)
    email_array = contact_dict['email']
    for y in email_array:
        print ("sending email to " + y)
        notify_email(course, y)
    pass

#____________________________
#   REFRESH FUNCTIONALITY
#____________________________
# from https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds

def beat():
    refresh.main()


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously
refresh = Refresh()


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(beat)
    scheduler.run_continuously(100)