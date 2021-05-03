import requests


def get_geoip_info(ip, session):
    geoip_request = session.get(f"http://ipwhois.app/json/{ip}")
    # geoip_request = requests.get(f"http://api.ipgeolocationapi.com/geolocate/{ip}")  (Alternative)

    if geoip_request.ok:
        data_dict = geoip_request.json()
        city = data_dict['city']

        if city:
            country = data_dict['country']
            latitude = data_dict['latitude']
            longitude = data_dict['longitude']
            isp = data_dict['isp']
            return [ip, country, city, latitude, longitude, isp]

        return [ip, '', '', '', '', '']


if __name__ == "__main__":
    test_ip = "45.170.129.202"
    s = requests.Session()
    print(get_geoip_info(test_ip, s))
