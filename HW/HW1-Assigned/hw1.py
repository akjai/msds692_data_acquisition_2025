import pickle

import pandas as pd
import requests
import streamlit as st

from user_definition import *


def retrieve_data_from_urls(url_list: list) -> list:
    """
    Read data from url_list and return
    a list of unique dictionaries
    which includes all the data from url in url_list.
    """
    response = requests.get(url_list[0])
    data = pickle.loads(response.content)

    unique_data = []
    for item in data:
        if item not in unique_data:
            unique_data.append(item)

    return unique_data


def filter_by_company(data: pd.DataFrame, company_dictionary: dict)\
        -> pd.DataFrame:
    """
    For the given data (data frame) and company_dictionary,
    create checkboxes and return a new dataframe
    which only includes data being checked.
    """
    checked_urls = []
    for company in company_dictionary:
        with st.sidebar:
            if st.checkbox(company):
                checked_urls.append(company_dictionary[company])
    if not checked_urls:
        return pd.DataFrame(columns=data.columns)
    filtered_df = data[data['link'].str.contains('|'.join(checked_urls))]
    return filtered_df


if __name__ == '__main__':
    # Add title
    print(retrieve_data_from_urls(url_list))

    st.title( + " Job Listings")

    # Add data
    data = retrieve_data_from_urls(url_list)
    df = pd.DataFrame(data)

    # Add sidebar label
    st.sidebar.markdown("Filter by Company")

    # Filter data
    filtered_data = filter_by_company(df, company_dictionary)

    st.dataframe(
        filtered_data[['date', 'title', 'link']],
        column_config={"link": st.column_config.LinkColumn("link")}
    )
