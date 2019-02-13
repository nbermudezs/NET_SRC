__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import os
import pandas as pd
import sendgrid
import urllib.request as urllib
from datetime import date
from sendgrid.helpers.mail import *


def can_read(filepath):
    cols = ['Sagarin_RK', 'Pomeroy_RK', 'BPI_RK', 'RPI', 'NET Rank', 'Conf']
    try:
        df = pd.read_csv(filepath)
        for col in cols:
            if col not in df.columns:
                return False
    except:
        return False
    return True


def send_error_email():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email(os.environ.get('SENDGRID_FROM'))
    subject = 'Error in SRC coefficients calculation - {}'.format(date.today().strftime('%Y-%m-%d'))
    to_email = Email(os.environ.get('SENDGRID_TO_DEVELOPER'))
    content = Content('text/plain', 'There was an error in today\' correlation analysis. Please have a look.')
    mail = Mail(from_email, subject, to_email, content)

    data = mail.get()
    try:
        response = sg.client.mail.send.post(request_body=data)
    except urllib.HTTPError as e:
        print(e.read())
        exit()


if __name__ == '__main__':
    import sys
    filepath = sys.argv[1]

    if not can_read(filepath):
        send_error_email()
