# import base64
# import streamlit as st
# import pandas as pd
# import os
# from dotenv import load_dotenv, set_key
# load_dotenv()
# import bingnewssearch
# st.set_page_config(page_title="Bing News Summarizer", page_icon='assets/Bing-Emblem.png', layout="centered", initial_sidebar_state="auto", menu_items=None)
# st.image('https://th.bing.com/th/id/OIP.hhzjsBv-Eokw-k8Ff2N0PgHaEp?pid=ImgDet&rs=1', width=300)
# st.title('Bing News Summarizer :newspaper:')
# st.write('This is a simple web app that uses Bing Search and Azure Open AI to search news articles and summarize them.')
# keyword = st.text_input('Enter a keyword to scrape for news articles and click the Scrape News button to summarize the news articles.')
# set_key(dotenv_path=".env", key_to_set= "keyword", value_to_set = keyword)
# st.write('You entered: ', keyword)
# scrape_btn = st.button('Search & Summarize ', help='Click to scrape news')
# if scrape_btn:
#     ## Check that text field is not empty
#     if not keyword.strip():
#         st.error('Please enter a keyword to search for news articles')
#     else:
#         with st.spinner(text = 'I\'m Searching & Scraping some news articles for you…'):
#             # my_bar = st.progress(0)
#             # for percent_complete in range(100):
#             #     time.sleep(0.1)
#             #     my_bar.progress(percent_complete + 1)
#             scrape_btn = on_click = os.system('python bingnewssearch.py')
#             st.success('Done!')
#             st.write('Here are the news articles I found for ' + keyword + ' on the Internet and summarized them for you with Azure Open AI :')
#             st.write(bingnewssearch.getnews)
#             set_key(dotenv_path=".env", key_to_set= "keyword", value_to_set = "")
            
            
import streamlit as st
import subprocess

# Set Streamlit page configuration with a modern look
st.set_page_config(page_title="Bing News Summarizer", page_icon='assets/Bing-Emblem.png', layout="wide", initial_sidebar_state="collapsed")
# Use columns to create a modern layout with an image on the left and the title on the right
col1, col2 = st.columns([1, 2])
with col1:
    st.image('https://th.bing.com/th/id/OIP.hhzjsBv-Eokw-k8Ff2N0PgHaEp?pid=ImgDet&rs=1', width=300)
with col2:
    st.title('Bing News Summarizer')
    st.image('assets/Bing-Emblem.png',width = 100)
    st.write('This is a simple web app that uses Bing Search and Azure Open AI to search news articles and summarize them.')

# Display the input for the keyword using a modern input field
keyword = st.text_input(label = 'Keyword',help='Enter a keyword to search for news articles and then click the Search & Summarize button.')

# Add some space before the button
st.write("")

# Create a modern-looking button and make it center-aligned
btn_col1, btn_col2, btn_col3 = st.columns([1, 0.5, 1])
with btn_col2:
    scrape_btn = st.button('🔍 Search & Summarize ')

# Display the entered keyword in a more subtle way
if keyword:
    st.caption(f'You entered: {keyword}')

if scrape_btn:
    # Check that the text field is not empty
    if not keyword.strip():
        st.error('Please enter a keyword to search for news articles.')
    else:
        with st.spinner(text='Searching & Scraping news articles for you...'):
            # Execute the bingnewssearch.py script with the keyword as an argument
            result = subprocess.run(['python', 'bingnewssearch.py', keyword], capture_output=True, text=True)
            if result.returncode == 0:
                # Display the result of the script execution in a modern way
                st.success('Done! Here are the news articles I found and summarized for you:')
                st.text(result.stdout , layout = centered)  # using st.text to present the data as plain text
            else:
                # Display any errors encountered during script execution
                st.error('An error occurred while searching for news articles.')
                st.code(result.stderr) 