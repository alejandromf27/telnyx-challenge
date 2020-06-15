import json
import argparse
from df_manager import (
    get_request_df, get_v_lan_df_primary, get_redundant_df, get_non_redundant_df
)

# set up script args
parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--env", type=str, default='prod')
args = parser.parse_args()

# check if environment is correct
environment = args.env
if environment not in ['test', 'prod']:
    raise Exception("Environment error. Options 'test' or 'prod' (default)")

# config files for inputs and output
REQUESTS_FILE_PATH = "data/test_requests.csv" if environment == 'test' else "data/requests.csv"
V_LAN_FILE_PATH = "data/test_vlans.csv" if environment == 'test' else "data/vlans.csv"
OUTPUT_FILE_PATH = "data/test_output.csv" if environment == 'test' else "data/output.csv"

# get requests with redundant
requests_df_with_redundant = get_request_df(REQUESTS_FILE_PATH, 1)

# get requests without redundant
requests_df_without_redundant = get_request_df(REQUESTS_FILE_PATH, 0)

# get VLan list with primary port, save 2 times to used in a non available ports
v_lan_df_with_primary_port = get_v_lan_df_primary(V_LAN_FILE_PATH, 1)
v_lan_df_primary_port_not_available = get_v_lan_df_primary(V_LAN_FILE_PATH, 1)

# get VLan list without primary port
v_lan_df_non_primary_port = get_v_lan_df_primary(V_LAN_FILE_PATH, 0)

# dataFrame to json to make it easier
json_redundant_df = json.loads(requests_df_with_redundant.to_json(orient='records'))
json_non_redundant_df = json.loads(requests_df_without_redundant.to_json(orient='records'))

# check redundant requests in the VLan dataFrame
redundant_df = get_redundant_df(
    json_redundant_df,
    v_lan_df_with_primary_port,
    v_lan_df_primary_port_not_available,
    v_lan_df_non_primary_port
)

# check non redundant requests, passing the "redundant_df"
non_redundant_df = get_non_redundant_df(
    json_non_redundant_df,
    v_lan_df_primary_port_not_available
)

# Create the final dataFrame ordered by request_id, primary_port, device_id ascending
final_output_df = redundant_df.append(
    non_redundant_df, ignore_index=True
).sort_values(
    ['request_id', 'primary_port', 'device_id'],
    ascending=[True, True, True]
).reset_index(drop=True).drop(
    ['redundant'], axis=1
)[
    ['request_id', 'device_id', 'primary_port', 'vlan_id']
]
# save the dataFrame to CSV removing the dataFrame index
final_output_df.to_csv(OUTPUT_FILE_PATH, index=False)
print("Requests Executed Successfully!!!")
exit(0)
