import requests
import locale
import json 
import pandas as pd
import time
import pandas as pd

# Set locale for thousand separators
locale.setlocale(locale.LC_ALL, '')

# Function to retrieve cryptocurrency data
def get_crypto_data(coin_id):
    try:
        # CoinGecko API endpoint for cryptocurrency data
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        
        # Extracting additional data
        coin_name = data['name']
        current_value = locale.format_string("%.2f", data['market_data']['current_price']['usd'], grouping=True)
        ath = locale.format_string("%.2f", data['market_data']['ath']['usd'], grouping=True)
        price_change_24h = data['market_data']['price_change_percentage_24h']
        market_cap = locale.format_string("%.2f", data['market_data']['market_cap']['usd'], grouping=True)
        market_cap_change_24h = data['market_data']['market_cap_change_percentage_24h']
        
        # Extracting developer and community data
        community_data = data['community_data']
        twitter_followers = community_data['twitter_followers']
        
        return [coin_name, current_value, ath, price_change_24h, market_cap, market_cap_change_24h, twitter_followers]
            
    except Exception as e:
        print(" Error:", e)
        return None, None, None, None

if __name__ == "__main__":
    # coin_id = input("Enter the cryptocurrency ID (e.g., bitcoin): ").lower()
    
    coins = [
        'aqtis',
        'arc',
        'chaingpt',
        'dexcheck',
        'geojam',
        'cryptogpt-token',
        'data-lake',
        'paal-ai',
    ]

    coin_data = {}
    for coin in coins:
        print(f'Retrieving data for {coin}')
        coin_data[coin] = get_crypto_data(coin)
        time.sleep(1)

    try:
        df = pd.DataFrame(coin_data, index=['Name', 'Current Value (USD)', 'All-Time High (USD)', 'Price Change (24h)', 'Market Cap (USD)', 'Market Cap Change (24h)', 'Twitter Followers'])
    except ValueError as e:
        print("Error:", e)
        # Truncate values if they're longer than the index
        data_truncated = {key: value[:7] for key, value in coin_data.items()}
        df = pd.DataFrame(data_truncated, index=['Name', 'Current Value (USD)', 'All-Time High (USD)', 'Price Change (24h)', 'Market Cap (USD)', 'Market Cap Change (24h)', 'Twitter Followers'])
        # Or, fill missing values with NaN
        # df = pd.DataFrame(coin_data, index=['Name', 'Current Value (USD)', 'All-Time High (USD)', 'Price Change (24h)', 'Market Cap (USD)', 'Market Cap Change (24h)', 'Twitter Followers'])
        # df = df.reindex(columns=df.columns[:7])
        # Transpose the DataFrame to have coins as columns
    df = df.T

    # Write DataFrame to CSV
    df.to_csv("crypto_data.csv")