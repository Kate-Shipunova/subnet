import unittest
import subnet

class TestSubnet(unittest.TestCase):
    '''Tests for functions of subnet.py'''

    def test_search_subnet_none(self):
        '''Check search_subnet() with no arguments. Have to return "None"'''
        self.assertEqual(subnet.search_subnet(), None)

    def test_search_subnet_ipv4(self):
        '''Check search_subnet() with positive arguments. Have to return "192.168.1.0/29"'''
        self.assertEqual(subnet.search_subnet('IPv4.txt', 'ipv4'), '192.168.1.0/29')

    def test_search_subnet_ipv4_all_octets_are_different(self):
        '''Check search_subnet() with your arguments: 192.168.1.2 and 193.167.1.3. Have to return "192.0.0.0/7"'''
        self.assertEqual(subnet.search_subnet('IPv4dop.txt', 'ipv4'), '192.0.0.0/7')

    def test_search_subnet_ipv6(self):
        '''Check search_subnet() with positive arguments. Have to return "ffe0::/72"'''
        self.assertEqual(subnet.search_subnet('IPv6.txt', 'ipv6'), 'ffe0::/72')

    def test_search_subnet_ipv6_all_octets_are_different(self):
        '''Check search_subnet() with positive arguments: ffe0::1:0:0:0 and fff0::10:0:0:0. Have to return "ff00::/8"'''
        self.assertEqual(subnet.search_subnet('IPv6dop.txt', 'ipv6'), 'ff00::/8')

    def test_check_type_of_ip_positive(self):
        '''Check function check_type_of_ip(). Have to be "True" '''
        self.assertEqual(subnet.check_type_of_ip('ipv4'), True)
        self.assertEqual(subnet.check_type_of_ip('ipv6'), True)

    def test_check_type_of_ip_negative(self):
        '''Check function check_type_of_ip(). Have to be "True" '''
        self.assertEqual(subnet.check_type_of_ip('ipv2'), False)
        self.assertEqual(subnet.check_type_of_ip('ggggg'), False)

    def test_taking_kit_of_addresses(self):
        '''Check function taking_kit_of_addresses(). Have to return 2 times arr with addresses, at last time - None '''
        arr_can_to_be_ipv4 = ['192.168.1.2', '192.168.1.3', '192.168.1.5']
        arr_can_to_be_ipv6 = [
                              'ffe0::1:0:0:0',
                              'ffe0::2:0:0:0',
                              'ffe0::4:0:0:0',
                              'ffe0::8:0:0:0',
                              'ffe0::10:0:0:0',
                              'ffe0::20:0:0:0',
                              'ffe0::40:0:0:0',
                              'ffe0::80:0:0:0'
                             ]
        self.assertEqual(subnet.taking_kit_of_addresses('IPv4.txt'), arr_can_to_be_ipv4)
        self.assertEqual(subnet.taking_kit_of_addresses('IPv6.txt'), arr_can_to_be_ipv6)
        self.assertEqual(subnet.taking_kit_of_addresses('111.txt'), None)

    def test_get_addr_by_octets(self):
        '''Check function get_addr_by_octets(). Have to return 2 times positive results'''
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
        '''Check check_correct_of_addr(). Have to return 2 times True, at 4 last times False '''
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

    def test_get_mask(self):
        ''' Check function get_mask(). Have to return 2 times correct value, at last time - "0" '''
        arr_ipv4 = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '3'],
            ['192', '168', '1', '5']
        ]
        arr_bin_ipv4 = [
            ['11000000', '10101000', '00000001', '00000010'],
            ['11000000', '10101000', '00000001', '00000011'],
            ['11000000', '10101000', '00000001', '00000101']
        ]

        arr_ipv6 = [
            ['ffe0', '0', '0', '0', '1', '0', '0', '0'],
            ['ffe0', '0', '0', '0', '80', '0', '0', '0']
        ]
        arr_bin_ipv6 = [
            ['1111111111100000', '0000000000000000', '0000000000000000', '0000000000000000',
             '0000000000000001', '0000000000000000', '0000000000000000', '0000000000000000'
            ],
            ['1111111111100000', '0000000000000000', '0000000000000000', '0000000000000000',
             '0000000001010000', '0000000000000000', '0000000000000000', '0000000000000000'
            ]
        ]

        arr_zero = [
            ['192', '168', '1', '2'],
            ['192', '168', '1', '2'],
            ['192', '168', '1', '2']
        ]
        arr_zero_bit = [
            ['11000000', '10101000', '00000001', '00000010'],
            ['11000000', '10101000', '00000001', '00000010'],
            ['11000000', '10101000', '00000001', '00000010']
        ]

        mask_ipv4, arr_ipv4 = subnet.get_mask(arr_ipv4, 'ipv4')
        mask_ipv6, arr_ipv6 = subnet.get_mask(arr_ipv6, 'ipv6')
        mask_ipv4_zero, arr_zero_get = subnet.get_mask(arr_zero, 'ipv4')
        self.assertEqual(mask_ipv4, 29)
        self.assertEqual(arr_ipv4,arr_bin_ipv4)
        self.assertEqual(mask_ipv6, 72)
        self.assertEqual(arr_ipv6, arr_bin_ipv6)
        self.assertEqual(mask_ipv4_zero, 32)
        self.assertEqual(arr_zero_get, arr_zero_bit)

    def test_get_net(self):
        '''Check get_net(). All times have to be positive.'''
        arr_ipv4 = ['11000000', '10101000', '00000001', '00000010']
        arr_ipv6 = [
             '1111111111100000', '0000000000000000', '0000000000000000', '0000000000000000',
             '0000000000000001', '0000000000000000', '0000000000000000', '0000000000000000'
            ]
        self.assertEqual(subnet.get_net(arr_ipv4, 29, 'ipv4'), '192.168.1.0')
        self.assertEqual(subnet.get_net(arr_ipv6, 72, 'ipv6'), 'ffe0::')

    def test_get_result(self):
        '''Check get_result(). All times have to be positive.'''
        self.assertEqual(subnet.get_result('192.168.1.0', 29), '192.168.1.0/29')
        self.assertEqual(subnet.get_result('ffe0::', 72), 'ffe0::/72')


if __name__ == '__main__':
    unittest.main()
