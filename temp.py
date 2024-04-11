import requests
import pandas as pd

def save_crypto_mapping_as_csv(filename):
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        crypto_mapping = {crypto['name']: crypto['id'] for crypto in data}
        df = pd.DataFrame(list(crypto_mapping.items()), columns=['Crypto Name', 'Crypto ID'])
        df.to_csv(filename, index=False)
        print("Crypto mapping saved successfully as", filename)
    else:
        print("Failed to retrieve crypto mapping. Status code:", response.status_code)

# Example usage
save_crypto_mapping_as_csv("crypto_mapping.csv")
