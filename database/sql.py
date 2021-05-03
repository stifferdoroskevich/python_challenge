from lookup import rdap, geoip
import sqlite3


def create_db():
    connection = sqlite3.connect("ipdata.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS rdap
                          (ipaddr TEXT NOT NULL PRIMARY KEY,
                           range_lower TEXT,
                           range_upper TEXT,
                           CIDR TEXT)                   
                           ''')
    connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS geoip
                          (ipaddr TEXT,
                           country TEXT,
                           city TEXT,
                           latitude REAL,
                           longitude REAL,
                           isp TEXT,
                           FOREIGN KEY (ipaddr)
                               REFERENCES rdap (ipaddr))
                           ''')
    connection.commit()

    connection.close()


def insertions_ip(list_of_ips):
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()

        for ip in list_of_ips:
            cursor.execute('INSERT INTO rdap VALUES (?, ?, ?, ?)', (ip, '', '', ''))
            connection.commit()
        print("IP INSERTION DONE")
    except sqlite3.Error as error:
        print("Failed to insert IP Address", error)
    finally:
        if connection:
            connection.close()


def insert_rdap():
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()
        ip_list = cursor.execute("Select ipaddr from rdap").fetchall()
        sql_update = '''UPDATE rdap
                              SET CIDR = ?,
                                  range_lower = ?, 
                                  range_upper = ?
                              WHERE ipaddr = ?;'''

        for ip in ip_list:
            data = rdap.get_rdap_info(ip[0])
            if data != None:
                cursor.execute(sql_update, (data[0], data[1], data[2], data[3]))
                connection.commit()
        print("RDAP UPDATE DONE")
    except sqlite3.Error as error:
        print("Failed to update IP Address. ->", error)
    finally:
        if connection:
            connection.close()


def insert_geo_ip():
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()
        ip_list = cursor.execute("Select ipaddr from rdap").fetchall()
        sql_insert = '''INSERT INTO geoip VALUES
                               (?, ?, ?, ?, ?, ?)
                               '''
        for ip in ip_list:
            data = geoip.get_geoip_info(ip[0])
            if data != None:
                cursor.execute(sql_insert, (data[0], data[1], data[2], data[3], data[4], data[5]))
                connection.commit()
        print("GEOIP INSERT DONE")
    except sqlite3.Error as error:
        print("Failed to insert IP Address Geo Location. ->", error)
    finally:
        if connection:
            connection.close()


def query_rdap():
    connection = sqlite3.connect("ipdata.db")
    cursor = connection.cursor()
    cursor.execute("Select * from rdap")
    result = cursor.fetchall()
    connection.close()
    return result


def query_geoip():
    connection = sqlite3.connect("ipdata.db")
    cursor = connection.cursor()
    cursor.execute("Select * from geoip")
    result = cursor.fetchall()
    connection.close()
    return result
