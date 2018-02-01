import os
from pathlib import Path

emails_path = os.path.abspath('../Data/emails.txt')
email_name = "testy34578+"

def get_new_email():
    email = Path(emails_path).read_text().rstrip()
    increase_email_counter(email)
    return email


def increase_email_counter(email):
    file = open(emails_path, "w")
    actual_counter = int(find_between(email, '+', '@'))
    actual_counter = actual_counter + 1
    file.write(email_name + str(actual_counter) + '@gmail.com')
    file.close()

# os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + 'Forms/emails'
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""