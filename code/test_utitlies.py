from unittest import TestCase
import utilities as u
import pandas as pd

class TestUtilities(TestCase):
    def test__points(self):
        expected_output = 100
        actual_output = u._points(1000)
        self.assertEqual(expected_output, actual_output)

    def test__get_total_points_redeemed(self):
        transactions_ = [{'date': '2012-01-01', 'user_id': 1, 
        'value': 1572, 'point_differential': 150},
        {'date': '2012-01-02',  'user_id': 1, 'value': 1167,
        'point_differential': 110},
        {'date': '2012-01-03',  'user_id': 1,  'value': 1403,
        'point_differential': -4860 }]
        df_ = pd.DataFrame(transactions_)

        expected_output = 5000
        actual_output = u._get_total_points_redeemed(df_)
        self.assertEqual(expected_output, actual_output)

    def test_fill_missing_data(self):
        transactions_ = [{'date': '2012-01-01', 'user_id': 1,
        'value': 1572, 'point_differential': 150},
        {'date': '2012-01-02',  'user_id': 1, 'value': 1167,
        'point_differential': 110},
        {'date': '2012-01-03',  'user_id': 1,  'value': 1403, 
        'point_differential': -4860 }]
        df_ = pd.DataFrame(transactions_)

        expected_output = [400.0, 5000.0, 4142, 3]
        k = u.fill_missing_data(df_)
        actual_output = [k['total_standard_points'][0], k['total_points_redeemed'][0],
        k['value_of_purchases'][0],k['number_of_purchases'][0]]

        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()

	