import streamlit as st
import pandas as pd

st.set_page_config(page_title='Travels and Investments', page_icon=':airplane:', layout='centered')

# Task - 1  
st.title('Travel and Investments', text_alignment='center')
st.write('Book your holidays with us anywhere, anytime when you are ready!')

st.write('### ***Welcome to our travel and Investment agency!***')

if 'initialized' not in st.session_state:
    st.session_state['initialized']  = True
    st.success('Thank you for trusting and giving us an opportunity!')


# Task - 2

# SideBar

st.sidebar.title('Categories')

level = st.sidebar.radio('User Level', ['Beginner', 'Intermediate', 'Advanced'])

continent = st.sidebar.selectbox('Target Continent', ['All', 'Africa', 'Asia', 'Europe', 'America', 'Australia'])

interest = st.sidebar.multiselect('Interests', ['Tech', 'Finance', 'Travel', 'Food'])

budget = st.sidebar.slider('Investment Budget', 0, 10000, step=100)


# SideBar Ended


# Task - 3

name = st.text_input('Enter your name ', placeholder='Shyam Patel')


projectdate = st.date_input('Project Start Date')
st.write('Selected Budget : ', budget)

df = pd.DataFrame({
    'Date' : ['2026/03/23', '2026/01/22', '2026/03/18', '2026/02/15', '2026/01/30'],
    'Continent' : ['America', 'Asia', 'Australia', 'Europe', 'Africa'],
    'Category' : ['Beginner', 'Advanced', 'Intermediate', 'Intermediate', 'Advanced'],
    'Amount' : [4500, 7000, 5000, 6000, 8500],
    'Status' : ['Pending', 'Inprogress', 'Pending', 'Pending', 'Proccessed'],
    'Growth' : ['10%', '27%', '15%', '21%', '29%']
})

if continent == 'All':
    filtered_df = df
    st.dataframe(filtered_df)
else:
    filtered_df = df[df['Continent'] == continent]
    st.dataframe(filtered_df)


# Task - 4

button = st.button('Progress Report')

# if button:
#     st.balloons()
#     st.write('Daily Budget ', budget/30)
#     st.write(f'User : {name} wants to travel to {continent} starting {projectdate}')


# Task - 5

if button:
    if name == '':
        st.error('Please fill the name field.')
    elif budget == 0:
        st.warning('Please select your relevant budget.')
    else:
        st.balloons()
        st.write('Daily Budget ', budget/30)
        st.write(f'User *{name}* wants to travel to {continent} starting {projectdate}')
    