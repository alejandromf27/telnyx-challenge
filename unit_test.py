import unittest
from df_manager import (
    get_request_df, get_v_lan_df_primary
)

REQUESTS_FILE_PATH = "data/test_requests.csv"
V_LAN_FILE_PATH = "data/test_vlans.csv"


class TestTelnyxOutput(unittest.TestCase):

    def test_df_primary(self):
        """
        Test the function for df primary port
        """
        result_df = get_v_lan_df_primary(V_LAN_FILE_PATH, 1)
        test_result = len(result_df.loc[result_df['primary_port'] != 1])
        self.assertEqual(test_result, 0)
    
    def test_non_df_primary(self):
        """
        Test the function for df primary port for non primary ports
        """
        result = get_v_lan_df_primary(V_LAN_FILE_PATH, 0)
        test_result = len(result.loc[result['primary_port'] != 0])
        self.assertEqual(test_result, 0)

    def test_request_redundant_df(self):
        """
        Test the dataFrame request function for redundant
        """
        result = get_request_df(REQUESTS_FILE_PATH, 1)
        test_result = len(result.loc[result['redundant'] != 1])
        self.assertEqual(test_result, 0)

    def test_request_non_redundant_df(self):
        """
        Test the dataFrame request function for non redundant
        """
        result = get_request_df(REQUESTS_FILE_PATH, 0)
        test_result = len(result.loc[result['redundant'] != 0])
        self.assertEqual(test_result, 0)


if __name__ == '__main__':
    unittest.main()
