from collections import defaultdict
from pathlib import Path
import sqlite3
import streamlit as st
import altair as alt
import pandas as pd
import locale
import json 
import pandas as pd
import time
import traceback

import coingeckoapi as api

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Inventory tracker',
    page_icon=':shopping_bags:', # This is an emoji shortcode. Could be a URL too.
)

st.title('Crypto data retriever')

st.info('''
    Upload your Excel file below to fill the data.
''')

uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)

if uploaded_file is not None:
    try:
        # Get the mapping
        # df_coin_mapping = api.get_all_crypto_mapping()
        df_coin_mapping = pd.read_csv('./crypto_mapping.csv')
        print(df_coin_mapping)

        df_coin_list = pd.read_csv(uploaded_file)

        data = {}

        # Loop on every coin to get
        for index, coin_to_get in df_coin_list.iterrows():
            print(coin_to_get['Ticker'])  # Assuming 'Ticker' is the column name in df_coin_list

            # Search for exact matching cryptocurrency name in df_coin_mapping
            exact_match = df_coin_mapping[df_coin_mapping['Crypto Name'] == coin_to_get['Ticker']]

            # Check if an exact match is found
            if not exact_match.empty:
                # Get the corresponding ID
                crypto_id = exact_match.iloc[0]['Crypto ID']
                print("Exact Match Found - Crypto ID:", crypto_id)

                # Now you can query the API with the crypto_id
                # Perform your API query here with crypto_id
                data[coin_to_get['Ticker']] = api.get_crypto_data(crypto_id)

            else:
                # If no exact match is found, search for partial matching cryptocurrency name in df_coin_mapping
                partial_match = df_coin_mapping[df_coin_mapping['Crypto Name'].str.contains(coin_to_get['Ticker'], case=False)]

                # Check if a partial match is found
                if not partial_match.empty:
                    # Get the corresponding ID
                    crypto_id = partial_match.iloc[0]['Crypto ID']
                    print("Partial Match Found - Crypto ID:", crypto_id)

                    # Now you can query the API with the crypto_id
                    # Perform your API query here with crypto_id
                    data[coin_to_get['Ticker']] = api.get_crypto_data(crypto_id)

                else:
                    data[coin_to_get['Ticker']] = api.get_crypto_data(crypto_id)
                    print("No match found for", coin_to_get['Ticker'])

        st.json(data)

    except Exception as ex:
        traceback.print_exc()
