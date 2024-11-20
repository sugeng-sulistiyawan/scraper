import requests
import pandas as pd

base_url = 'https://api-sscasn.bkn.go.id/2024/portal/spf?kode_ref_pend=5110120&pengadaan_kd=3&offset='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Referer': 'https://sscasn.bkn.go.id/',
    'Origin': 'https://sscasn.bkn.go.id'
}

all_data = []
offset = 0
items_per_page = 10
max_data = 10000

while offset < max_data:
    url = f'{base_url}{offset}'
    print(f"Requesting data from URL: {url}")
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break
    
    try:
        response_json = response.json()  # Parse JSON response
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response content: {response.text}")
        break
    
    if 'data' in response_json and 'data' in response_json['data']:
        data = response_json['data']['data']
        all_data.extend(data)  # Add data to the all_data list
        offset += items_per_page  # Increase offset by the number of items per page
    else:
        print("No more data available.")
        break

df = pd.DataFrame(all_data)

df.to_csv('data.csv', index=False)

print("Data has been successfully saved to 'data.csv")
