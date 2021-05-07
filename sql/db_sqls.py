def create_tables(curs):
    curs.executescript('''
                        CREATE TABLE IF NOT EXISTS rdap
                              (ipaddr TEXT NOT NULL PRIMARY KEY,
                               range_lower TEXT,
                               range_upper TEXT,
                               CIDR TEXT);
    
                        CREATE TABLE IF NOT EXISTS geoip
                              (ipaddr TEXT,
                               country TEXT,
                               city TEXT,
                               latitude REAL,
                               longitude REAL,
                               isp TEXT,
                               FOREIGN KEY (ipaddr)
                                   REFERENCES rdap (ipaddr));        
                                   ''')


def get_ips(curs):
    ip_list = curs.execute("Select ipaddr from rdap").fetchall()
    return ip_list

