import smtplib
from email.mime.text import MIMEText
import pandas as pd
from auto_download import authorisation
import pprint
import streamlit as st
from config import APP_PASSWORD

#################################################################################################################################
# isolate emails from google sheets file

# authorising sheets api and opening registration form
sheets_client = authorisation('creds/maya_credentials.json')
sheet = sheets_client.open('Muslim Techies Registration Form (Responses)')
# print(sheet.get_worksheet(0))

# accessing sheet through drive api and return records as json string
records_data = sheet.get_worksheet(0).get_all_records()

# convert the json to dataframe
email = pd.DataFrame.from_dict(records_data)
# print(records_df.columns)
email.dropna(axis=0, how='all', inplace=True)
print(f'{len(email)} entries')
# print(len(mobile['Email Address'].unique()))
email.drop_duplicates(subset=['Email Address'], keep=False, inplace=True)

df = email
# print(df.columns)

######################################################################################################################################
# email formulation

# process for connecting to gmail
conn = smtplib.SMTP('smtp.gmail.com', 587)
password = APP_PASSWORD

# connect to personal email
conn.ehlo()
conn.starttls()

test_recipients = ['elhawlir@gmail.com', 'wiseoym@gmail.com', 'databites19@gmail.com']
recipients = []

# student emails
students = df.loc[df['What is your involvement in tech?'] == 'Student', 'Email Address']
recipients = list(students)

#melbourne-based emails

# print(recipients)

def form_email(recipient_list, msg_text, subject, sender):
    count = 0
    msg_text['Subject'] = subject
    msg_text['From'] = sender
    msg_text['To'] = ', '.join(recipient_list)
    conn.sendmail(sender, recipient_list, msg_text.as_string())
    count += 1
    print('emails sent')

##############################################################################################################
# streamlit app
title = st.title('Email sender')
sub_heading = st.write('This program only works with gmail based emails')

from_email = st.text_input('From:', value='hello@example.com')
subject_line = st.text_input('Subject:')
send_email = st.text_area('Enter the text for your email')
# email text
msg = MIMEText(send_email)

# send emails directly from terminal
# form_email(recipients, msg, subject_line, send_from)
conn.login(from_email, password)
if st.button('Send Email'):
    try:
        form_email(test_recipients, msg, subject_line, from_email)
        # form_email(recipients, msg, subject_line, from_email)
        st.write('Emails successfullly sent!')
    except:
        st.write("There's been an error")

conn.quit()

# """
# Salaam,

# If you're receiving this email, it's because you're registered as a student. While the tickets for our inaugural iftar will be $20
# a person, for our students we've created a special discount making it only $10!

# These are only in limited supply however with only 20 being given out. Make sure you get in quick before they run out!

# Buy your ticket here: www.eventbrite.com/e/152952435853/?discount=uni-student

# P.S. Unfortunately we're only running the event in Melbourne this year, but we'll work to make it a national milestone in future

# Best,
# Rashid - Team MIT
# """