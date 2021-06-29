from twilio.rest import Client as tw
import pandas as pd
from auth_public import authorisation
from config import ACCOUNT_SID, AUTH_TOKEN, SCRIPT_ID, TACCOUNT_SID, TAUTH_TOKEN
import streamlit as st
from datetime import datetime

# twilio account details
# Live
account_sid = ACCOUNT_SID
auth_token = AUTH_TOKEN
# Test
taccount = TACCOUNT_SID
tauth = TAUTH_TOKEN

# connecting to twilio client
# Live
client = tw(account_sid, auth_token)
# Test
tclient = tw(taccount,tauth)

# authorising sheets api and opening registration form
sheets_client = authorisation('[CREDENTIALS FILE NAME].json')
sheet = sheets_client.open('[NAME OF GOOGLE WORKSHEET]')
# print(sheet.get_worksheet(0))

# accessing sheet through drive api and return records as json string
records_data = sheet.get_worksheet(0).get_all_records()

#######################################################################################################################
# parsing sheets records

# convert the json to dataframe
mobile = pd.DataFrame.from_dict(records_data)
# print(records_df.columns)
mobile.dropna(axis=0, how='all', inplace=True)
print(f'{len(mobile)} entries')
# print(len(mobile['Email Address'].unique()))
mobile.drop_duplicates(subset=['Email Address'], keep=False, inplace=True)
print(f'There are {len(mobile)} members in the [COMMUNITY NAME] community')

# get the current time
print(datetime.now())

# saves a copy of most up to date records of our members in .csv and .xlsx format
csv_output = mobile.to_csv('outputs//[CSV FILE].csv', index=False)
xlsx_output = mobile.to_excel('outputs//[EXCEL WORKSHEET].xlsx', index=False)

##############################################################################################################
# Streamlit app layout

# create streamlit app title
title = st.title('Mass Messager')

# ensures all numbers are in suitable format to receive messages
def number_clean(series):
    empty_list = []
    for i in series:
        if (i[:2] == '61') or (i[:3] == '+61'):
            empty_list.append(i)
        else:
            i = '+61' + i
            empty_list.append(i)
    return empty_list

def clean_mobile_input(mobile_list):
    # cleaned_list = ['+' + mobile_list[i] for i in range(mobile_list) if mobile_list[i][0] != '+']
    # return cleaned_list
    for i in range(len(mobile_list)):
        if mobile_list[i][0] != '+':
            mobile_list[i] = '+' + mobile_list[i]
    else:
        pass

    return mobile_list

# input 'from' mobile number directly
from_input = st.text_input('From:', value=[TWILIO_NUMBER], max_chars=12)

# input 'to' mobile number directly
to_input = st.text_input('To:', max_chars=12)

# text input area
input_text = st.text_area('Construct Message', value='Start constructing your message', max_chars=155)

####################################################################################################################### 
# the following is for numbers directly from google sheet

print(type(mobile))
# convert mobile numbers to string
mobile['phone number'] = mobile['Mobile Number'].map(lambda x: str(x))

# student numbers
students = mobile.loc[mobile['What is your involvement in tech?'] == 'Student', 'phone number']
# print(students)

# standardise numbers so they can receive messages
mobile['phone number'] = number_clean(mobile['phone number'])
total_numbers = list(mobile['phone number'])
total_numbers = clean_mobile_input(total_numbers)
# print(total_numbers)
# print(len(total_numbers))

recipients = number_clean(students)
recipients = clean_mobile_input(recipients)
# print(len(recipients))
# print(recipients)

# basic metrics
print(f"There are {len(set(total_numbers))} unique numbers")
print(f"There are {len(mobile['Email Address'])} unique emails")

#########################################################################
# Setting up for final send

test_numbers = ['LIVE MOBILE NUMBER','+61412345678','+614000000000']
exc_students = [i for i in total_numbers if i not in recipients] # members that are not students
print(f'{len(exc_students)} non-students')
print(f'There are {len(mobile) - len(exc_students)} students')

# function that sends final message to MIT members list
def final_text(numbers_list,text):
    count = 0
    # list of numbers not to be sent messages
    leave_out = ['+61412345678','+614000000000','OTHER OPTED OUT NUMBERS']
    # filtering out the above numbers
    final_list = [number for number in numbers_list if number not in leave_out]
    # length of total numbers to be sent messges
    print('There are', len(final_list), 'total mobile numbers')
    # removing duplicate numbers
    unique_numbers = list(set(final_list))
    # displaying number of unique numbers
    print('There are', len(unique_numbers), 'unique mobile numbers')
    # returns number of duplicate numbers
    print('There are', len(final_list) - len(unique_numbers), 'duplicate mobile numbers')
    # send msg to each number individually
    for i in unique_numbers:
        # if test, use tclient
        message = client.messages.create(
            body= text,
            from_='[NAME/TWILIO NUMBER]', # to use alphanumeric id must be less than 11 characters
            to= i
        )
        print(message.sid)
        count += 1
        print(count)


# function that sends whatsapp message to members list
def whatsapp_msg(numbers_list,text):
    count = 0
    # list of numbers not to be sent messages
    leave_out = ['+61412345678','+614000000000','OTHER OPTED OUT NUMBERS']
    # filtering out the above numbers
    final_list = [number for number in numbers_list if number not in leave_out]
    # length of total numbers to be sent messges
    print('There are', len(final_list), 'total mobile numbers')
    # removing duplicate numbers
    unique_numbers = list(set(final_list))
    # displaying number of unique numbers
    print('There are', len(unique_numbers), 'unique mobile numbers')
    # returns number of duplicate numbers
    print('There are', len(final_list) - len(unique_numbers), 'duplicate mobile numbers')
    # send msg to each number individually
    for i in unique_numbers:
        message = client.messages.create(
            body= text,
            from_='whatsapp:[TWILIO NUMBER]', # using twilio sandbox
            to= f'whatsapp:{i}'
        )
        print(message.sid)
        count += 1
        print(count)

# Sends msg directly from number inputted to to_number inputted
def direct_message(from_number, to_number, text):
    message = client.messages.create(
            body= text,
            from_= from_number, # to use alphanumeric id must be less than 11 characters
            to= to_number)
    print(message.sid)

###############################################################################################################################
# send text messages directly from this local terminal

# final_text(test_numbers,text)
# final_text(list_numbers,text)
# final_text(numbers,text)

#######################################################################################################################
# sends message to pre-determined list of numbers, after you input text and press 'Send Message' button
if st.button('Send Message'):
    try:
        # final_text(play,input_text)
        final_text(test_numbers,input_text) # test list including my number
        # final_text(total_numbers,input_text) this list includes everyone
        # final_text(recipients,input_text) # this list is only students
        # final_text(exc_students,input_text) # this list of numbers excludes students
        st.write('Success!')
    except:
        st.write("There's been an error")

# sends whatsapp message to pre-determined list of numbers after you input text
if st.button('Send WhatsApp Message'):
    try:
        # whatsapp_msg(play,input_text)
        whatsapp_msg(test_numbers,input_text)
        # whatsapp_msg(list_numbers,text)
        # whatsapp_msg(numbers,input_text)
        st.write('Success!')
    except:
        st.write("There's been an error")

if st.button('Send Direct Message'):
    try:
        direct_message(from_input, to_input, input_text)
        st.write('Your message succesfully sent!')
    except:
        st.write("There's been an error")