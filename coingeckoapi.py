import requests
import traceback
import locale
import time

# Set locale for thousand separators
locale.setlocale(locale.LC_ALL, '')

# Function to retrieve all cryptos name and id to map
def get_all_crypto_mapping(filename):
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        crypto_mapping = {crypto['name']: crypto['id'] for crypto in data}
        df = pd.DataFrame(list(crypto_mapping.items()), columns=['Crypto Name', 'Crypto ID'])
        return df_mapping
    else:
        print("Failed to retrieve crypto mapping. Status code:", response.status_code)


def get_crypto_data(coin_id):
    while True:
        try:
            # CoinGecko API endpoint for cryptocurrency data
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            response = requests.get(url)
            
            if response.status_code == 429:
                # Rate limit reached, wait for a while before retrying
                print("Rate limit reached. Waiting for retry...")
                time.sleep(10)  # Wait for 30 seconds before retrying
                continue
            
            response.raise_for_status()  # Raise an exception for other 4xx or 5xx status codes
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
            
            coin_data = {
                'coin_name': coin_name,
                'current_value': current_value,
                'ath': ath,
                'price_change_24h':price_change_24h,
                'market_cap':market_cap,
                'market_cap_change_24h':market_cap_change_24h,
                'twitter_followers':twitter_followers
            }

            print(f'Data successfully retrieved for {coin_name}')
            return coin_data

        except Exception as e:
            traceback.print_exc()
            print(" Error:", e)
            return {'error': str(e)}