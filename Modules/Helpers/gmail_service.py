# Importing required libraries
import base64
import datetime
import os
import re

import dateutil.parser as parser
import time
from googleapiclient import discovery
from bs4 import BeautifulSoup
from httplib2 import Http
from oauth2client import file, client, tools
import pytz

# Creating a storage.JSON file with authentication details

STOAREGE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/Accesses/storage.json'
CLIENT_SECRET = os.path.dirname(os.path.abspath(__file__)) + '/Accesses/client_secret.json'
LINK_REGEX = '.http://.*'


def init_gmail_service():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # we are using modify and not readonly, as we will be marking the messages Read
    store = file.Storage(STOAREGE_PATH)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    return GMAIL


def get_unread_messages(gmail_service):
    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    # Getting all the unread messages from Inbox
    # labelIds can be changed accordingly
    unread_msgs = gmail_service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

    # We get a dictonary. Now reading values for the key 'messages'
    try:
        mssg_list = unread_msgs['messages']
        return mssg_list
    except:
        return list()


def get_subject(headr):
    for one in headr:  # getting the Subject
        if one['name'] == 'Subject':
            msg_subject = one['value']
            return msg_subject
            # temp_dict['Subject'] = msg_subject
        else:
            pass
    return ''


def get_date(headr):
    for two in headr:  # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.replace(tzinfo=pytz.utc))
            return m_date
            # temp_dict['Date'] = str(m_date)
        else:
            pass
    return ''


def get_sender(headr):
    for three in headr:  # getting the Sender
        if three['name'] == 'From':
            msg_from = three['value']
            return msg_from
        else:
            pass
    return ''


def get_message_body(payld):
    try:

        # Fetching message body
        mssg_parts = payld['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        part_body = part_one['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8

        return clean_two  # it's from oryginal code
    except:
        return ''


def mark_message_as_read(GMAIL, user_id, m_id):
    GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()


def get_link(subject_title, date_from, mark_as_read=True):
    user_id = "me"
    GMAIL = init_gmail_service()
    mssg_list = get_unread_messages(GMAIL)

    for mssg in mssg_list[:2]:
        temp_dict = {}
        m_id = mssg['id']  # get id of individual message
        message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        msg_subject = get_subject(headr)
        msg_date = get_date(headr)
        msg_sender = get_sender(headr)
        msg_body = get_message_body(payld)

        if msg_date < date_from:
            break

        if subject_title not in msg_subject:
            break

        link = re.findall(LINK_REGEX, msg_body.decode())[0]

        if link is not None:
            if mark_as_read is True:
                GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()
            return link.replace("\"", "")


def get_link_from_mail(mail_title, mark_as_read=True):
    utc = pytz.UTC
    date = datetime.now(pytz.timezone('UTC'))
    count = 0
    link = None
    while (count < 20 and link is None):
        link = get_link(mail_title,date, mark_as_read)
        count += 1
        time.sleep(2)
    return link
