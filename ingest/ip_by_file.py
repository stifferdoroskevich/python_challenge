import re


def ip_parser(filename):
    '''
    Search ips in a file, using regex and append to a list
    :param filename: str

    :return: ips_list: list
    Returns list of valid ip addresses
    '''

    try:
        with open(filename) as file:
            text = file.read()
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e
    else:
        ips_list = []
        raw_ip_list = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

        #validation of ip range 0-255
        validation = ("^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
                      "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")

        for match in raw_ip_list:
            if re.search(validation, match):
                ips_list.append(match)
        return ips_list


if __name__ == "__main__":
    test_data = "./test_data/list_of_ips_small.txt"
    print(ip_parser(test_data))
