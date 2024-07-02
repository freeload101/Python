import requests
import json
from datetime import datetime, timedelta

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

## This script pulls MDE info for each day for the past 30 days then will push it to Splunk 

# load the config
config = load_config('config.yml')
CLIENT_ID = config['app_id']
CLIENT_SECRET = config['app_id_secret']
TENANT_ID = config['tenant_id']
SPLUNK_HEC= config['splunk_hec']
SPLUNK_HEC_DOMAIN= config['splunk_hec_domain']

# Define constants
AUTH_URL = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
HUNTING_QUERY_URL = 'https://api.security.microsoft.com/api/advancedhunting/run'



# Get OAuth2 token
token_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://api.security.microsoft.com/.default'
}
response = requests.post(AUTH_URL, data=token_data)
response.raise_for_status()
token = response.json().get('access_token')

# Define headers
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Function to run query for a specific day
def run_query_for_day(start_date, end_date):
    query = {
       "Query": f'DeviceNetworkInfo | summarize arg_max(Timestamp, *) by DeviceId | join kind=inner (DeviceInfo) on DeviceId | where Timestamp >= datetime({start_date}) and Timestamp < datetime({end_date})| mv-expand todynamic(IPAddresses) |  extend IPAddress = parse_json(IPAddresses).IPAddress | project DeviceName, NetworkAdapterStatus, TunnelType, ConnectedNetworks, IPAddress, NetworkAdapterVendor, DeviceName1, PublicIP, OSArchitecture, OSPlatform, OSBuild, OSVersion, DeviceCategory, DeviceType, DeviceSubtype, Model, Vendor, OSDistribution, OSVersionInfo, ExposureLevel,IPAddresses'
    }
    response = requests.post(HUNTING_QUERY_URL, headers=headers, data=json.dumps(query))
    response.raise_for_status()
    return response.json()

# Define the date range (last 30 days)
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)

# Collect results
all_results = []

# Split the request into 1-day chunks
current_date = start_date
while current_date < end_date:
    next_date = current_date + timedelta(days=1)
    day_results = run_query_for_day(current_date.isoformat(), next_date.isoformat())
    all_results.extend(day_results.get('Results', []))
    current_date = next_date

# Output results to a file
with open('results.json', 'w') as file:
    json.dump(all_results, file, indent=4)


######################################################################################################## SPLIT the files into 4

# Read the original JSON file
with open('results.json', 'r') as file:
    data = json.load(file)

# Calculate the size of each chunk
chunk_size = len(data) // 4

# Split the data into four chunks
data1 = data[:chunk_size]
data2 = data[chunk_size:2*chunk_size]
data3 = data[2*chunk_size:3*chunk_size]
data4 = data[3*chunk_size:]

# Write each chunk to a new JSON file
with open('split1.json', 'w') as file:
    json.dump(data1, file, indent=4)

with open('split2.json', 'w') as file:
    json.dump(data2, file, indent=4)

with open('split3.json', 'w') as file:
    json.dump(data3, file, indent=4)

with open('split4.json', 'w') as file:
    json.dump(data4, file, indent=4)




################################################################################################## add the event tag to each file


import json

def transform_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data = json.load(file)
    transformed_data = [{"event": item} for item in data]
    with open(output_filename, 'w') as file:
        json.dump(transformed_data, file, indent=4)

file_pairs = [
    ('split1.json', 'split1_parsed.json'),
    ('split2.json', 'split2_parsed.json'),
    ('split3.json', 'split3_parsed.json'),
    ('split4.json', 'split4_parsed.json'),
]

for input_file, output_file in file_pairs:
    transform_file(input_file, output_file)


############################################################################################## push each file to Splunk use spath ...


url = "https://{SPLUNK_HEC_DOMAIN}/services/collector/event"
headers = {
    'Authorization': 'Splunk {SPLUNK_HEC}',
}

files = ['split1_parsed.json', 'split2_parsed.json', 'split3_parsed.json', 'split4_parsed.json']

for file in files:
    with open(file, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
        print(f"Response for {file}: {response.status_code}, {response.text}")
