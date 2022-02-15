# This script is designed to be run once an hour
# it searches for the given tags over a specified
# time period. For each result, the requester email
# is extracted and appended to a spreadsheet

import configparser
import logging
import smtplib
import os
import TicketCounter as TC


config = configparser.RawConfigParser()
config.read('../src/auth.ini')
OUTPUT_FILE = config['default']['EmailList'].strip('"')
DOMAIN = config['zendesk']['Domain'].strip('"')
AUTH = config['zendesk']['Credentials'].strip('"')
SENDER = config['email']['Sender'].strip('"')
PASS = config['email']['Password'].strip('"')
RECIPIENT = config['email']['Recipient'].strip('"')
TAGS = config['mods']['SearchTags'].strip('"')

def main(logger):

    # Initialize an empty list to hold the emails
    # EmailList = []

    # logger.warning('Checking if Output File exists...')
    # if not os.path.exists(OUTPUT_FILE):
    #     logger.warning('Output File not found. Creating...')
    #     #import in csv as list
    #     # EmailList = TC.pd.DataFrame()
    #     # EmailList.to_csv(OUTPUT_FILE)
    #     logger.warning('Output File generated and ready for usage.')
    # else:
    #     logger.warning('Output File already exists. Querying new results.')

    st0, st1, xdst0, xtst0, xtst1 = TC.get_formatted_datetimes(1)
   

    # need tag(s), start & end time (defaults past hour)
    EmailList = []
    EmailList = TC.pd.DataFrame()
    TicketResults = TC.get_tickets(DOMAIN, AUTH, st0, st1, TAGS)
    for ticket in TicketResults['results']:
        EmailList = EmailList.append(TC.pd.Series(ticket['via']['source']['from']), ignore_index=True)
        print(EmailList.shape)
    try:
        # save email list to csv
        # lst = TC.get_formatted_datetimes(1)
        # lst = TC.json.loads(lst.text)
        EmailList.to_csv(OUTPUT_FILE)
        pass 
    except Exception as e:
        logger.warning('Error saving file, {}'.format(str(e)))

    try:
        logger.warning("Sending report to {}\n".format(RECIPIENT))
        #send_report(RECIPIENT, TicketCountVar, tags, delta, (SENDER, PASS))
    except Exception as e:
        logger.exception('{}\nError sending the report!'.format(str(e)))
    logger.warning('SUCCESS')



# takes the recipient email, hourly count, and frequent tags as arguments
# auth should be a tuple containing the sender email id and sender email id password
# builds a message and sends it to the recipient

def send_report(to, count, tags, delta, auth = None, subject='Email List Update!'):
    try:
        # creates SMTP session
        email = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        email.starttls()

        # authentication
        email.login(auth[0], auth[1])

        # craft the message
        message = ("Greetings Crunchyroll Humans, ")#.format(count, delta, tags)
        message = 'Subject: {}\n\n{}'.format(subject, message).encode('utf-8')

        # send the email
        email.sendmail(auth[0], to, message)

        # terminate the session
        email.quit()
    except Exception as e:
        print('ERROR: ', str(e))
        exit()
    return 0




if __name__ =="__main__":
    # TODO: set logging level based on input
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    main(logger)