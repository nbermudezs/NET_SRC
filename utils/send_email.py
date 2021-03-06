__author__ = "Nestor Bermudez"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "nab6@illinois.edu"
__status__ = "Development"


import base64
import sendgrid
import sys
import os
if sys.version_info[0] < 3:
    import urllib
else:
    import urllib.request as urllib
from datetime import date
from sendgrid.helpers.mail import *


def send(root):
    template_id = os.environ.get('SENDGRID_TEMPLATE_ID')
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

    from_email = os.environ.get('SENDGRID_FROM')
    subject = 'SRC coefficients {}'.format(date.today().strftime('%Y-%m-%d'))
    to_email = os.environ.get('SENDGRID_TO')

    mail = Mail(
        from_email=from_email, subject=subject, to_emails=to_email
    )
    mail.template_id = template_id
    files = [
        'correlation_{}.txt',
        'correlation_{}.csv',
        'rankings_{}.csv',
        'correlation_PowerSeven_{}.csv',
        'correlation_Others_{}.csv',
        'rankings_PowerSeven_{}.csv',
        'rankings_Others_{}.csv',
        'KPvNET_rankings_PowerSeven_{}.csv',
        'KPvNET_rankings_Others_{}.csv',
        'KPvNET_rankings_{}.csv',
        'outliers_{}.json',
        'net-v-all.png',
        'correlation_{}.png',
    ]
    for file in files:
        filename = file.format(date.today().strftime('%Y-%m-%d'))
        with open(root + '/' + filename, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()

        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_name = FileName(filename)
        attachment.disposition = Disposition('attachment')
        mail.add_attachment(attachment)

    response = sg.send(mail)
    print(response.status_code)


def send_v3(root):
    template_id = os.environ.get('SENDGRID_TEMPLATE_ID')
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email(os.environ.get('SENDGRID_FROM'))
    subject = 'SRC coefficients {}'.format(date.today().strftime('%Y-%m-%d'))
    to_email = Email(os.environ.get('SENDGRID_TO'))

    mail = Mail(from_email, subject, to_email)
    files = [
        'correlation_{}.txt',
        'correlation_{}.csv',
        'rankings_{}.csv',
        'correlation_PowerSeven_{}.csv',
        'correlation_Others_{}.csv',
        'rankings_PowerSeven_{}.csv',
        'rankings_Others_{}.csv',
        'KPvNET_rankings_PowerSeven_{}.csv',
        'KPvNET_rankings_Others_{}.csv',
        'KPvNET_rankings_{}.csv',
        'outliers_{}.json',
        'net-v-all.png',
        'correlation_{}.png',
    ]
    for file in files:
        filename = file.format(date.today().strftime('%Y-%m-%d'))
        with open(root + '/' + filename, 'rb') as f:
            data = base64.b64encode(f.read()).decode()

        attachment = Attachment()
        attachment.content = data
        attachment.disposition = 'attachment'
        attachment.filename = filename
        mail.add_attachment(attachment)

    data = mail.get()
    data['template_id'] = template_id

    try:
        response = sg.client.mail.send.post(request_body=data)
    except urllib.HTTPError as e:
        print(e.read())
        exit()

    print(response.status_code)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = 'tmp'
    if sys.version_info[0] < 3:
        send(path)
    else:
        send_v3(path)