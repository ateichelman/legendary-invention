from __future__ import print_function
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date, timedelta
import base64
import email
from email import policy
from apiclient import errors


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    https://developers.google.com/gmail/api/quickstart/python
    Show basic usage of API.
    List users Gmail labels
    """

    creds = None
    # token.pickle stores user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no creds, have user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES
			)
            creds = flow.run_local_server(port=0)
        # Save creds for the next run!
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # call gmail api
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    today = date.today()
    yesterday = today - timedelta(1)

    query = "before: {0} after: {1}".format(today.strftime('%Y/%m/%d'),
                                            yesterday.strftime('%Y/%m/%d'))

    # messages.list returns an array of message objects that only
    # have the id field (for some reason).
    resp = service.users().messages().list(userId='me', q=query).execute()
    messages = resp.get('messages', [])

    if not messages:
        print('No messages found!')
    else:
        print("{0} new Messages: ".format(len(messages)))
        for message in messages:
            # For each message id, retrieve the actual message object via
            # messages.get.
            # https://docs.python.org/3/library/email.parser.html
            # https://docs.python.org/3/library/email.message.html#email.message.EmailMessage
            try:
                thisMes = service.users().messages().get(userId='me', id=message['id'], format="raw").execute()
                msg_str = base64.urlsafe_b64decode(thisMes['raw'].encode('ASCII'))
                mime_msg = email.message_from_bytes(msg_str, policy=policy.default)
                # print(mime_msg['subject'])
                # print(mime_msg.get_body(preferencelist=('plain')))
                # Instead of just printing, lets send to a "processBody" function...


                # Diagnostic Code:
                # for part in mime_msg.walk():
                #     print(part.get_content_type())
                # print(mime_msg.keys())

                # if 'Mime-Version' in mime_msg:
                emailBody = mime_msg.get_body(preferencelist=('related', 'html', 'plain')).as_string()
                # print(emailBody)
                processBody(emailBody)
            except KeyError as error:
                print('A Key error has occured: %s' % error)


    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels: ')
    #     for label in labels:
    #         print(label['name'])

    # Regex attempts
    # (href=)+(3D)?"[^"]+"

def processBody( text ):
    urls = re.findall(r'(?:href=(?:3D)?")(.*?)"', text)
    print('Found URL in emails: ', urls)

if __name__ == '__main__':
    main()
