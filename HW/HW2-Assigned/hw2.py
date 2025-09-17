import json

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd

from user_definition import *


def retrieve_data_from_gcs(service_account_key: str,
                           project_id: str,
                           bucket_name: str,
                           file_name_prefix: str
                           ) -> dict:
    """
    Retrieve file contents from all files starting with 'file_name_prefix'
    in "bucket_name" and returns a dictionary including "results",
    "job_titles", and"company_dict"

    Args:
        service_account_key (str) : path of service account key file(.json)
        project_id (str) : GCP Project ID where bucket is located
        bucket_name (str) : bucket name
        file_name_prefix (str) : prefix of files to retrieve data.
                                 (Ex."job_search/")

    Returns:
        dict: in a following format
            {"results": a list including "results" from all the files
                        starting with file_name_prefix,
             "job_titles": a list including unique "job_title"s
                           from all the files starting with file_name_prefix,
             "company_dict": a dictionary including all "company_dict"s
                            from all the files starting with file_name_prefix
            }
    """
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=file_name_prefix)

    results = []
    job_titles = set()
    company_dict = {}

    for blob in blobs:
        print(f"blob name: {blob.name}")
        content = json.loads(blob.download_as_string())
        results.extend(content.get("results", []))
        job_titles.update([content.get("job_title")])
        company_dict.update(content.get("company_dict", {}))

    return {
        "results": results,
        "job_titles": sorted(job_titles),
        "company_dict": company_dict
    }


if __name__ == '__main__':
    # Title should be comma separated strings of job titles in ascending order.
    # Company list on the side bar should include unique names
    # in ascending order.
    # The dataframe should be filtered based on the selection on the sidebar.
    # The dataframe should only include unique values.
    # The dataframe should have date, title, and link columns where link
    # should be a hyperlink.
    gcs_data = retrieve_data_from_gcs(service_account_file_path,
                                      project_id,
                                      bucket_name,
                                      file_name_prefix)

    df = pd.DataFrame(gcs_data["results"])

    title_string = ""
    for title in gcs_data["job_titles"]:
        title_string += (str(title) + ", ")
    title_string = title_string[:-2]

    st.title(title_string + " Job Listings")

    st.sidebar.markdown("Filter by Company")
    checked_companies = []
    for company in (gcs_data["company_dict"]):
        if st.sidebar.checkbox(company):
            checked_companies.append(company)

    if checked_companies:
        filtered_rows = []
        for i, row in df.iterrows():
            for company in checked_companies:
                company_url = gcs_data["company_dict"][company]
                if company_url in row['link']:
                    filtered_rows.append(row)
                    break
        filtered_df = pd.DataFrame(filtered_rows)
    else:
        filtered_df = df.copy()

    filtered_df = filtered_df.drop_duplicates(subset=['date', 'title', 'link'])

    st.dataframe(
        filtered_df[["date", "title", "link"]],
        column_config={"link": st.column_config.LinkColumn("link")}
    )
