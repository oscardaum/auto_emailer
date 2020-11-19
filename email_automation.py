#https://realpython.com/python-send-email/#sending-multiple-personalized-emails
#https://docs.python.org/3/library/email.examples.html

'''
Takes in user password and sends email
    Parameters:
        password: gmail password of sender
        [TO DO]: get user email
    Return:
        sends email to given users/BCC(ers)

written by Oscar Daum and Gloria Sun

Notable Resources used:
    for general code: https://realpython.com/python-send-email/#sending-multiple-personalized-emails
    for multiple users/html text: https://docs.python.org/3/library/email.examples.html


To Do:
    format html:
    find way to use securely: https://realpython.com/python-send-email/#sending-multiple-personalized-emails, \
    https://developers.google.com/gmail/api/quickstart/python
    import csv with users to send to: https://realpython.com/python-send-email/#sending-multiple-personalized-emails
    format name instead of email appearing as sender
    automate it


    lines to change: 38
'''


import email, smtplib, ssl
import csv
from email.headerregistry import Address
from email.utils import make_msgid
from email.message import EmailMessage

sender_email = "hoohacks.sponsorship@gmail.com"
password = input("Type your password and press enter: ")
sender_name = input("sender name: ")

with open("template.txt") as f:
    template = f.read()

with open("template-noname.txt") as f:
    template_noname = f.read()

def message(name, email, company):
    msg = EmailMessage()
    msg['Subject'] = "HooHacks Sponsorship Opportunities for " + company
    msg['From'] = sender_name + " <hoohacks.sponsorship@gmail.com>"
    msg['To'] = email
    msg['Cc'] = "hackathon.virginia@gmail.com"
    msg['Bcc'] = ""
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    if(name == ""):
        msg.add_alternative(template_noname.format(company=company, sender_name=sender_name), subtype='html')
    else:
        msg.add_alternative(template.format(name = name, company = company, sender_name = sender_name), subtype='html')
    # note that we needed to peel the <> off the msgid for use in the html.
    return msg


# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    with open("Sponsorship List 1.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for email, name, company in reader:
            print(f"Sending email to {name}")
            # Send email here
            server.login(sender_email, password)
            server.send_message(message(name, email, company))
