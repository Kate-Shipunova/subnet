import unittest
import subnet

class TestSubnet(unittest.TestCase):
    '''Tests for functions of subnet.py'''

    def test_search_subnet(self):
        '''Check function search_subnet() with no arguments. Can to return "None"'''
        self.assertEqual(subnet.search_subnet(), None)

    def test_check_type_of_ip_positive(self):
        '''Check function check_type_of_ip(). Can to be "True" '''
        self.assertEqual(subnet.check_type_of_ip('ipv4'), True)
        self.assertEqual(subnet.check_type_of_ip('ipv6'), True)

    def test_check_type_of_ip_negative(self):
        '''Check function check_type_of_ip(). Can to be "True" '''
        self.assertEqual(subnet.check_type_of_ip('ipv2'), False)
        self.assertEqual(subnet.check_type_of_ip('ggggg'), False)

    def test_taking_kit_of_addresses(self):
        '''Check function taking_kit_of_addresses(). Can to return 2 times arr with addresses, at last time - None '''
        arr_can_to_be_ipv4 = ['192.168.1.2', '192.168.1.3', '192.168.1.5']
        arr_can_to_be_ipv6 = ['ffe0::1:0:0:0', 'ffe0::2:0:0:0', 'ffe0::4:0:0:0', 'ffe0::8:0:0:0', 'ffe0::10:0:0:0', 'ffe0::20:0:0:0', 'ffe0::40:0:0:0', 'ffe0::80:0:0:0']
        self.assertEqual(subnet.taking_kit_of_addresses('IPv4.txt'), arr_can_to_be_ipv4)
        self.assertEqual(subnet.taking_kit_of_addresses('IPv6.txt'), arr_can_to_be_ipv6)
        self.assertEqual(subnet.taking_kit_of_addresses('111.txt'), None)

    def test_get_addr_by_octets(self):
        '''Check function get_addr_by_octets(). Can to return 2 times positive results'''
        arr_ipv4 = ['192.168.1.2', '192.168.1.3', '192.168.1.5']
        arr_ipv6 = [
                    'ffe0::1:0:0:0',
                    'ffe0::2:0:0:0',
                    'ffe0::4:0:0:0',
                    'ffe0::8:0:0:0',
                    'ffe0::10:0:0:0',
                    'ffe0::20:0:0:0',
                    'ffe0::40:0:0:0',
                    'ffe0::80:0:0:0'
                   ]
        arr_can_to_be_ipv4 = [
                              ['192', '168', '1', '2'],
                              ['192', '168', '1', '3'],
                              ['192', '168', '1', '5']
                              ]
        arr_can_to_be_ipv6 = [
                              ['ffe0', '0', '0', '0', '1', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '2', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '4', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '8', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '10', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '20', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '40', '0', '0', '0'],
                              ['ffe0', '0', '0', '0', '80', '0', '0', '0']
                             ]
        self.assertEqual(subnet.get_addr_by_octets(arr_ipv4, 'ipv4'), arr_can_to_be_ipv4)
        self.assertEqual(subnet.get_addr_by_octets(arr_ipv6, 'ipv6'), arr_can_to_be_ipv6)

    def test_check_correct_of_addr(self):
        '''Check check_correct_of_addr(). Can to return 2 times True, at 4 last times False '''
        arr_ipv4_pos = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '3'],
            ['192', '168', '1', '5']
        ]
        arr_ipv4_neg_count_octets = [
            ['192', '168', '1', '2'],
            ['192', '3'],
        ]
        arr_ipv4_neg_value = [
            ['192', '1688', '777', '2'],
            ['192', '3453', '192', '168'],
        ]

        arr_ipv6_pos = [
            ['ffe0', '0', '0', '0', '1', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '2', '0', '0', '0'],
        ]
        arr_ipv6_neg_count_hextets = [
            ['ffe0', '0', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '2', '0', '0', '0', '0', '2'],
        ]
        arr_ipv6_neg_value = [
            ['ffe0', '-100', '0', '0', '1', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '265535', '0', '0', '0'],
        ]

        self.assertEqual(subnet.check_correct_of_addr(arr_ipv4_pos, 'ipv4'), True)
        self.assertEqual(subnet.check_correct_of_addr(arr_ipv6_pos, 'ipv6'), True)
        self.assertEqual(subnet.check_correct_of_addr(arr_ipv4_neg_count_octets, 'ipv4'), False)
        self.assertEqual(subnet.check_correct_of_addr(arr_ipv6_neg_count_hextets, 'ipv6'), False)
        self.assertEqual(subnet.check_correct_of_addr(arr_ipv4_neg_value, 'ipv4'), False)
        self.assertEqual(subnet.check_correct_of_addr(arr_ipv6_neg_value, 'ipv6'), False)

    def test_search_octet_with_host(self):
        ''' Check function check_correct_of_addr(). Can to return 2 times correct value, at last time - None'''
        arr_ipv4 = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '3'],
            ['192', '168', '1', '5']
        ]
        arr_ipv6 = [
            ['ffe0', '0', '0', '0', '1', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '40', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '80', '0', '0', '0']
        ]
        arr_incorrect = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '2'],
            ['192', '168', '1', '2']
        ]
        self.assertEqual(subnet.search_octet_with_host(arr_ipv4), 3)
        self.assertEqual(subnet.search_octet_with_host(arr_ipv6), 4)
        self.assertEqual(subnet.search_octet_with_host(arr_incorrect), None)

    def test_search_max_num_in_octets(self):
        ''' Check search_max_num_in_octets(). All times can to be positive.'''
        arr_ipv4 = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '3'],
            ['192', '168', '1', '5']
        ]
        arr_ipv6 = [
            ['ffe0', '0', '0', '0', '1', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '2', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '4', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '8', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '10', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '20', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '40', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '80', '0', '0', '0']
        ]
        self.assertEqual(subnet.search_max_num_in_octets(arr_ipv4, 3), 5)
        self.assertEqual(subnet.search_max_num_in_octets(arr_ipv6, 4), 80)

    def test_get_mask(self):
        '''Check get_mask(). All times can to be positive.'''
        self.assertEqual(subnet.get_mask(5, 'ipv4', 3),('/29', ['0', '0', '0', '0', '0', '1', '0', '1'], 3))
        self.assertEqual(subnet.get_mask(80, 'ipv6', 4),
                         ('/72', ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0'], 56))

    def test_get_net_octet(self):
        '''Check get_net_octet(). All times can to be positive.'''
        self.assertEqual(subnet.get_net_octet(['0', '0', '0', '0', '0', '1', '0', '1'], 3, 'ipv4'), '0')
        self.assertEqual(subnet.get_net_octet(
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0'],
            56, 'ipv6'), '0')

    def test_get_result(self):
        '''Check get_result(). All times can to be positive.'''
        self.assertEqual(subnet.get_result(['192', '168', '1', '2'], '0', 3, '/29', 'ipv4'),
                         '192.168.1.0/29')
        self.assertEqual(subnet.get_result(['ffe0', '0', '0', '0', '1', '0', '0', '0'], '0', 4, '/72', 'ipv6'),
                         'ffe0::/72')


if __name__ == '__main__':
    unittest.main()
