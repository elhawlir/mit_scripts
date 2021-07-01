# deployed version of community dashboard

from numpy.lib.arraysetops import isin
import pandas as pd
from auth_public import authorisation
import streamlit as st
import streamlit.components.v1 as components
import datetime
from datetime import datetime as dt
import os

# authorising sheets api and opening registration form
sheets_client = authorisation(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
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
    # return cleaned_list
    for i in range(len(mobile_list)):
        if mobile_list[i][0] != '+':
            mobile_list[i] = '+' + mobile_list[i]
    else:
        pass

    return mobile_list

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

tracking_code = """
<!-- Default Statcounter code for Community Dashboard
https://st-community-dashboard.herokuapp.com/ -->
<script type="text/javascript">
var sc_project=12559589; 
var sc_invisible=1; 
var sc_security="bfe5a5cb"; 
var sc_remove_link=1; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js" async></script>
<noscript><div class="statcounter"><img class="statcounter"
src="https://c.statcounter.com/12559589/0/bfe5a5cb/1/" alt="website
statistics"></div></noscript>
<!-- End of Statcounter Code -->
"""
components.html(tracking_code, width=200, height=200)