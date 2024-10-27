import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to HDB Resale Helper! 👋")

st.sidebar.success("Select a demo above.")

with st.expander("Important notice"):
    st.write('''
       IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

        Always consult with qualified professionals for accurate and personalized advice.
    ''')

st.markdown(
"""
This is a HDB Resale helper. 

**👈 Select a demo from the sidebar** to see some examples of what they can do**

## Project Scope
The goal of this project is to help both buyer and sellers in the HDB resale market via the use of:


## Objectives
1. An AI chatbot that consolidates essential data from HDB's website, gathering information on eligibility criteria, policies, financing options, and other key resources to provide users with a comprehensive and easily accessible platform for housing information.

2. Another AI helper that uses historical data (2020 onwards) to help buyers or sellers better understand what price they can sell/buy their flat with some given criteria (town, storey, budget, flat type) 

## Data Sources
All data sources are publicly available.
- [Resale terms and conditions](https://www.hdb.gov.sg/cs/infoweb/e-resale/resale-purchase-of-an-hdb-resale-flat)
- [HDB Flat Portal Terms and Conditions for Resale Flat Listing Service](https://homes.hdb.gov.sg/home/terms-and-conditions)
- [Helping First-time Homebuyers Afford a Resale Flat](https://www.hdb.gov.sg/about-us/news-and-publications/publications/hdbspeaks/Helping-First-time-Homebuyers-Afford-a-Resale-Flat)
- [HDB's Application page and child pages](https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/application)
- [data.gov.sg](https://data.gov.sg/datasets?topics=housing&page=1&resultId=d_8b84c4ee58e3cfc0ece0d773c8ca6abc)


## Features
#### Resale ChatBot
- Users do not need to thrawl through all the HDB pages to look for the data that they want
- step-by-step guide for purchasing a resale HDB
- Document Assistance and Checklists
    - Offers checklists and documents for each stage of the buying/selling process.
- Users can understand the estimated timelines and milestones in the process.

### HDB Resale estimator
- Gives users a better understanding of how much they can sell/buy a resale HDB given some criteria
 
"""
)