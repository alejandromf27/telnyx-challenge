import pandas as pd


def get_v_lan_df_primary(file_name, primary):
    """
    Function to get the dataFrame of VLan csv file
    :param file_name:
    :param primary:
    :return: return a dataFrame
    """
    v_lan_df = pd.read_csv(file_name)
    return v_lan_df.loc[
        v_lan_df['primary_port'] == primary
    ].reset_index(drop=True).reset_index(drop=True)


def get_request_df(request_file, is_redundant):
    """
    Function to read from the request csv file and order de result by request_id
    :param request_file: the csv file with all requests
    :param is_redundant: perform the data if we need redundant or not
    :return: the dataFrame ordered
    """
    # read from
    requests_df = pd.read_csv(request_file)
    return requests_df.loc[
        requests_df['redundant'] == is_redundant
    ].sort_values('request_id', ascending=True).reset_index(drop=True)
        

def get_redundant_df(
        json_redundant_df, v_lan_df_primary, v_lan_df_primary_port_not_available, v_lan_df_non_primary_port
):
    """
    This function will parse the redundant json dataFrame file to produce a file with two rows per request
    for redundant records matched with the vlans dataFrame per the instructions in the pdf
    :param json_redundant_df:
    :param v_lan_df_primary:
    :param v_lan_df_primary_port_not_available:
    :param v_lan_df_non_primary_port:
    :return: return a dataFrame
    """
    result_df = []
    for j_data in json_redundant_df:
        result_df += [j_data, {}]
    # matching requests with the VLan dataFrame
    for i in range(len(json_redundant_df)):
        flag = False
        # check if a minimum VLan and device has available the primary and non primary port
        # not available remove the record
        df_device_id = []
        while flag is False:
            min_v_lan_df = v_lan_df_primary[
                v_lan_df_primary['vlan_id'] == min(v_lan_df_primary['vlan_id'])
            ]
            min_device_df = min_v_lan_df[min_v_lan_df['device_id'] == min(min_v_lan_df['device_id'])]
            tmp_df = v_lan_df_non_primary_port[
                v_lan_df_non_primary_port['vlan_id'] == min_device_df.iloc[0]['vlan_id']
                ]
            df_device_id = tmp_df[
                tmp_df['device_id'] == min_device_df.iloc[0]['device_id']
            ]
            if len(df_device_id) == 0:
                v_lan_df_primary = v_lan_df_primary.drop(
                    v_lan_df_primary.index[min_device_df.index[0]]
                )
                v_lan_df_primary = v_lan_df_primary.reset_index(drop=True)
                flag = False
            elif len(df_device_id) >= 1:
                flag = True
        min_v_lan_df = v_lan_df_primary[v_lan_df_primary['vlan_id'] == min(v_lan_df_primary['vlan_id'])]
        min_device_df = min_v_lan_df[min_v_lan_df['device_id'] == min(min_v_lan_df['device_id'])]
        # complete the second dictionary
        result_df[i*2]['request_id'] = json_redundant_df[i]['request_id']
        result_df[i*2]['redundant'] = json_redundant_df[i]['redundant']
        result_df[i*2]['device_id'] = min_device_df.iloc[0]['device_id']
        result_df[i*2]['vlan_id'] = min_device_df.iloc[0]['vlan_id']
        result_df[i*2]['primary_port'] = min_device_df.iloc[0]['primary_port']
        result_df[i*2+1]['request_id'] = json_redundant_df[i]['request_id']
        result_df[i*2+1]['redundant'] = json_redundant_df[i]['redundant']
        if len(df_device_id) > 0:
            result_df[i*2+1]['device_id'] = df_device_id.iloc[0]['device_id']
            result_df[i*2+1]['vlan_id'] = df_device_id.iloc[0]['vlan_id']
            result_df[i*2+1]['primary_port'] = df_device_id.iloc[0]['primary_port']
        # remove duplicated
        v_lan_df_primary = v_lan_df_primary.drop(v_lan_df_primary.index[min_device_df.index[0]]).reset_index(drop=True)
        v_lan_df_primary_port_not_available = v_lan_df_primary_port_not_available.drop(
            v_lan_df_primary_port_not_available.index[min_device_df.index[0]]
        ).reset_index(drop=True)
        del min_v_lan_df
        del min_device_df
        print("VLan DataFrame: " + str(len(v_lan_df_primary_port_not_available)))
    return pd.DataFrame(result_df)

 
def get_non_redundant_df(json_non_redundant_df, v_lan_df_primary_port_not_available):
    """
    Function to match VLan ids to non_redundant requests
    :param json_non_redundant_df:
    :param v_lan_df_primary_port_not_available:
    :return: return a dataFrame
    """
    for i in range(len(json_non_redundant_df)):
        # find min VLan id and device id for primary available
        min_v_lan_df = v_lan_df_primary_port_not_available[
            v_lan_df_primary_port_not_available['vlan_id'] == min(v_lan_df_primary_port_not_available['vlan_id'])
        ]
        min_vlans_device_df = min_v_lan_df[min_v_lan_df['device_id'] == min(min_v_lan_df['device_id'])]
        # complete the json
        json_non_redundant_df[i]['device_id'] = min_vlans_device_df.iloc[0]['device_id']
        json_non_redundant_df[i]['vlan_id'] = min_vlans_device_df.iloc[0]['vlan_id']
        json_non_redundant_df[i]['primary_port'] = min_vlans_device_df.iloc[0]['primary_port']
        # remove primary port values not available.
        v_lan_df_primary_port_not_available = v_lan_df_primary_port_not_available.drop(
            v_lan_df_primary_port_not_available.index[min_vlans_device_df.index[0]]
        )
        v_lan_df_primary_port_not_available = v_lan_df_primary_port_not_available.reset_index(drop=True)
        del min_v_lan_df
        del min_vlans_device_df
    return pd.DataFrame(json_non_redundant_df)
