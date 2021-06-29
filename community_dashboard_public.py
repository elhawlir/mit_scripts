from numpy.lib.arraysetops import isin
import pandas as pd
from auto_download import authorisation
import streamlit as st
from app_example import number_clean, clean_mobile_input
import datetime
from datetime import datetime as dt

# authorising sheets api and opening registration form
sheets_client = authorisation('google_credentials.json')
sheet = sheets_client.open('Muslim Techies Registration Form (Responses)')
# print(sheet.get_worksheet(0))

# accessing sheet through drive api and return records as json string
records_data = sheet.get_worksheet(0).get_all_records()

#######################################################################################################################
# parsing sheets records
# convert the json to dataframe
df = pd.DataFrame.from_dict(records_data)
df.dropna(axis=0, how='all', inplace=True) # remove empty records
df.drop_duplicates(subset=['Email Address'], keep=False, inplace=True) # remove duplicates

# convert mobile numbers to string
df['phone number'] = df['Mobile Number'].map(lambda x: str(x))
df['phone number'] = number_clean(df['phone number'])
# print(df['phone number'][:20])
total_numbers = list(df['phone number'])
total_numbers = clean_mobile_input(total_numbers)

# student numbers
students = df.loc[df['What is your involvement in tech?'] == 'Student', 'phone number']
# print(students)
recipients = number_clean(students)
recipients = clean_mobile_input(recipients)
# print(recipients)

test_numbers = ['+61425777848','+61412345678','+614000000000']
exc_students = [i for i in total_numbers if i not in recipients] # members that are not students

###################################################################
# streamlit output of community metrics

title = st.title('Muslims in Tech Community Breakdown')

# get the current date and time
st.write(f'As of {datetime.date.today()} (today)')
# st.write(dt.now().strftime('%H:%M'))

# total number of members in the community
st.write(f'There are {len(df)} members in the MIT community')

# number of students
st.write(f'{len(exc_students)} non-students and {len(df) - len(exc_students)} students')

###############################################################################
# complete df that we will query
search_df = df

state_options = ['ACT', 'New South Wales', 'Northern Territory', 'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia']

# Choose State from drop down list
state_header = st.subheader('State Breakdown')
drop_down = st.selectbox('Choose a State:', state_options)
if not drop_down:
    print(st.error("Please select a State"))  

def state_search(state, state_df):

    state_df['postcode'] = state_df['Postcode/Zipcode'].map(lambda x: str(x))

    if state == 'New South Wales':
        result = state_df[(state_df['postcode'].str[0] == '2') | (state_df['State/Territory'] == state)]
    if state == 'ACT':
        result = state_df[(state_df['postcode'].str[:2].isin(['26','29'])) | (state_df['State/Territory'] == state)]
    if state == 'Northern Territory':
        result = state_df[(state_df['postcode'].str[:2] == '08') | (state_df['State/Territory'] == state)]
    if state == 'Queensland':
        result = state_df[(state_df['postcode'].str[0] == '4') | (state_df['State/Territory'] == state)]
    if state == 'South Australia':
        result = state_df[(state_df['postcode'].str[0] == '5') | (state_df['State/Territory'] == state)]
    if state == 'Tasmania':
        result = state_df[(state_df['postcode'].str[0] == '7') | (state_df['State/Territory'] == state)]
    if state == 'Victoria':
        result = state_df[(state_df['postcode'].str[0] == '3') | (state_df['State/Territory'] == state)]
    if state == 'Western Australia':
        result = state_df[(state_df['postcode'].str[0] == '6') | (state_df['State/Territory'] == state)]

    return f'{len(result)} members in {state}'

st.write(state_search(drop_down, search_df))