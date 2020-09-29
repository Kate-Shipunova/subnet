from sys import argv as arg                                     # for working with args of CLI
import time


def search_subnet(file=None, type=None):
    ''' The function defines the min subnet for received IP-addresses (IPv4 or IPv6).

    Tre function is called with two arguments of CLI.
    Arguments of CLI:
    sys.argv[1] is file name with IP-addresses
    sys.argv[2] is type of IP-addresses (IPv4 or IPv6)
    Only for testing introduced positional arguments with values == None.
    The received data is checked for correctness.
    If the check fails, the function exists and returns the None.
    Else, data processing is performed using auxiliary functions:
    - check_type_of_ip(type_of_ip);
    - taking_kit_of_addresses(file_name);
    - get_addr_by_octets(addresses, type_of_ip);
    - check_correct_of_addr(addresses, type_of_ip);
    - get_mask(addresses, type_of_ip);
    - get_net(bit_addr, mask_int, type_of_ip);
    - get_result(net, mask_int)
    The maximum number of bits for net from the received set is determined.
    The mask is calculated.
    Tre network  is calculated.
    Result of this function is min subnet for received addresses.
    The algorithm takes into account the type of received addresses.
    :return: a str with min subnet for received addresses.

    '''

    # 1 - check sys.argv of CLI:
    if file == None and type == None:
        if len(arg) != 3:                                           # check count of sys.argv, can be 3
            print("The number of parameters does not correspond to the required for this function!")
            return

        file_name: str = arg[1]
        type_of_ip: str = arg[2].lower()                            # for register insensitive

    elif file != None and type != None:
        file_name: str = file
        type_of_ip: str = type.lower()

    else:
        print("The function did not receive parameters!")
        return

    # 2 - checking type of IP-addresses
    if not check_type_of_ip(type_of_ip):
        return

    # 3 - reading file and taking a kit of addresses
    addresses: list = taking_kit_of_addresses(file_name)       # for IP-addresses from file
    if not addresses:
        return

    # 4 - getting addresses by octets for next step
    addresses: list = get_addr_by_octets(addresses, type_of_ip)

    # 5 - checking correct of addresses from file
    if not check_correct_of_addr(addresses, type_of_ip):
        print('These addresses are incorrect!')
        return

    # 6 - getting mask for these addresses
    mask_int, bit_addr = get_mask(addresses, type_of_ip)
    if (mask_int == 32 and type_of_ip == 'ipv4') or (mask_int == 128 and type_of_ip == 'ipv6'):
        print("All addresses are equal. I can't find the min subnet")
        return

    # 7 - getting net
    net = get_net(bit_addr[0], mask_int, type_of_ip)

    # 8 - getting result
    return get_result(net, mask_int)


def check_type_of_ip(type_of_ip: str):                         # for step 2 - check type of IP-addresses
    if type_of_ip != 'ipv4' and type_of_ip != 'ipv6':
        print("Incorrect type of IP-addresses!")
        return False                                           # type: bool

    return True                                                # type: bool


def taking_kit_of_addresses(file_name: str):                   # for step 3
    arr: list = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                line = line.replace('\n', '')                  # for taking only address
                arr.append(line)

    except FileNotFoundError:
        print(f'No such file or directory: "{file_name}"')
        return                                                 # return None

    return arr                                                 # type: list


def get_addr_by_octets(arr_with_addr: list, type_of_ip: str):  # for step 4   type of arr_with_addr: list[str]
    addr_by_octets: list = []

    if type_of_ip == 'ipv4':
        for addr in arr_with_addr:
            addr_by_octets.append(addr.split('.'))            # [['192', '168', '1', '2' ],...]

    else:                                                     # if type_of_ip == 'ipv6'
        for addr in arr_with_addr:
            arr: list = addr.split(':')                       # ['ffe0', '', '80', '0', '0', '0']

            count_zero_for_addr: int = 8 - len(arr) + 1       # count zero for '::' or ''
            zero_arr: list = []
            for i in range(count_zero_for_addr):
                zero_arr += '0'                               # ['0', '0', '0']

            for i in range(len(arr)):                         # replacing '' with zero_arr
                if arr[i] == '':
                    arr[i:i:1] = zero_arr
                    arr.remove('')
                    addr_by_octets.append(arr)                # [['ffe0', '0', '0', '0', '1', '0', '0', '0' ], ...]
                    break

    return addr_by_octets                                     # type: list


def check_correct_of_addr(addr: list, type_of_ip: str):           # for step 5, type of addr: list[list[str]]

    if type_of_ip == 'ipv4':
        for i in range(len(addr)):
            count_of_octets: int = len(addr[i])
            if count_of_octets != 4:                              # count of octets for IPv4 can to be only = 4
                return False
            for j in range(count_of_octets):
                if int(addr[i][j]) < 0 or int(addr[i][j]) > 255:  # value of octet can to be only '0 - 255'
                    return False

    else:                                                         # if type_of_ip == 'ipv6'
        for i in range(len(addr)):
            if len(addr[i]) != 8:                                 # count of hextets for IPv6 can to be only = 8
                return False

            for j in range(len(addr[i])):
                if not addr[i][j].isdigit():                      # if the element is hex form
                    num_from_hex: int = int(addr[i][j], 16)
                else:
                    num_from_hex: int = int(addr[i][j])

                if num_from_hex < 0 or num_from_hex > 65535:      # value of hextet can to be only '0 - 65535'
                    return False

    return True


def get_mask(arr_with_addr: list, ip: str):                       # for step 6
    bin_addr = []

    if ip == 'ipv4':                                              # getting address in bin-notation for next step
        for i in range(len(arr_with_addr)):
            addr = []
            for j in range(len(arr_with_addr[i])):
                buf = str(bin(int(arr_with_addr[i][j])))[2:]      # for delete 'ob'
                if len(buf) != 8:
                    before_zero = 8 - len(buf)
                    for zero in range(before_zero):
                        buf = '0' + buf                           # filling addresses with '0'
                addr.append(buf)
            bin_addr.append(addr)

        count_bit_for_net = 0
        for j in range(len(bin_addr[0])):                         # counter of identical bits in addresses for mask
            for k in range(len(bin_addr[0][0])):
                for i in range(len(bin_addr)-1):

                    if bin_addr[i][j][k] == bin_addr[i+1][j][k] and i == len(bin_addr)-2:
                        count_bit_for_net += 1
                    elif bin_addr[i][j][k] != bin_addr[i+1][j][k]:

                        return (count_bit_for_net, bin_addr)       # type:  int, list

    else:                                                          # if type_of_ip == 'ipv6'
        for i in range(len(arr_with_addr)):
            addr = []
            for j in range(len(arr_with_addr[i])):

                if not arr_with_addr[i][j].isdigit():
                    buf = str(bin(int(arr_with_addr[i][j], 16)))[2:]

                else:
                    buf = str(bin(int(arr_with_addr[i][j])))[2:]

                if len(buf) != 16:
                    before_zero = 16 - len(buf)
                    for zero in range(before_zero):
                        buf = '0' + buf                             # filling addresses with '0'

                addr.append(buf)
            bin_addr.append(addr)

        count_bit_for_net = 0                                       # counter of identical bits in addresses for mask
        for j in range(len(bin_addr[0])):
            for k in range(len(bin_addr[0][0])):
                for i in range(len(bin_addr) - 1):

                    if bin_addr[i][j][k] == bin_addr[i + 1][j][k] and i == len(bin_addr) - 2:
                        count_bit_for_net += 1
                    elif bin_addr[i][j][k] != bin_addr[i + 1][j][k]:
                        count_bit_for_net -= count_bit_for_net % 4  # because it is 'ipv6'

                        return (count_bit_for_net, bin_addr)        # type:  int, list

    return (count_bit_for_net, bin_addr)  # type:  int, list


def get_net(bin_addr: list, count_net: int, ip: str):  # for step 7
    count = 0
    addr_net = []

    for i in range(len(bin_addr)):
        bin_addr[i] = list(bin_addr[i])

        for j in range(len(bin_addr[i])):
                count += 1
                if count_net < count:                 # this count the address is filled with '0' for get net
                    bin_addr[i][j] = '0'
        addr_net.append(''.join(bin_addr[i]))

    if ip == 'ipv4':
        for i in range(len(addr_net)):
            addr_net[i] = str(int(addr_net[i], 2))

        return '.'.join(addr_net)                     # type: str

    else:                                             # if type_of_ip == 'ipv6'
        net: str = ''
        flag = False                                  # use this flag only one time for take '::'

        for i in range(len(addr_net)):                # collecting address for 'ipv6'-type
            hex_num = hex(int(addr_net[i], 2))[2::]

            if hex_num.isdigit():
                hex_num = str(int(hex_num, 16))       # because we have number in hex-notation, for get int in result

            if hex_num != '0' and i == 0:                                 # for the first number
                net += hex_num
            elif hex_num != '0' and i != 0 and net[len(net)-1] != ':':    # count of hextets != 0 > 1
                net += (':' + hex_num)
            elif hex_num != '0' and i != 0 and net[len(net)-1] == ':':    # for exclude 'ffeo::' + ':7' -> 'ffeo:::7'
                net += hex_num
            elif hex_num == '0' and flag == False:                        # if we meet '0' at the first time
                net += '::'
                flag = True
            elif hex_num == '0' and (net[len(net)-1] != ':'):             # if we already have '::'
                net += (':' + hex_num)

        return net                                                       # type: str


def get_result(net: str, count_net: int):          # for step 8
    return net + '/' + str(count_net)              # format of subnet, return type: str


if __name__ == '__main__':
    start = time.perf_counter()
    print(search_subnet())
    print(f'The search_subnet() takes {round(time.perf_counter() - start, 9)} sec.')
