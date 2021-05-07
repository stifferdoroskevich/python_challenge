import requests


def get_rdap_info(ip, session):
    rdap_request = session.get(f"http://rdap.arin.net/registry/ip/{ip}")

    if rdap_request.ok:
        data_dict = rdap_request.json()
        return data_dict


if __name__ == '__main__':
    test_ip = '45.170.129.202'
    s = requests.Session()
    print(get_rdap_info(test_ip, s))
