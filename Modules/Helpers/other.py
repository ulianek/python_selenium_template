import os
from pathlib import Path

def get_new_email():
    email = Path(os.path.abspath('../../Modules/Forms/emails')).read_text().rstrip()
    increase_email_counter(email)
    return email


def increase_email_counter(email):
    file = open(os.path.abspath('../../Modules/Forms/emails'), "w")
    actual_counter = int(find_between(email, '+', '@'))
    actual_counter = actual_counter + 1
    file.write('testy34578+' + str(actual_counter) + '@gmail.com')
    file.close()

# os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + 'Forms/emails'
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""