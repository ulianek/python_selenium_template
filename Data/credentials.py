import collections

Account = collections.namedtuple('Account', 'email password username')

user = Account(email="testy.bitcraft@gmail.com", password="Hehehe25", username='')
admin = Account(email="admin@admin.admin", password="1q2w3e!Q@W#E", username='')