from lookup import rdap, geoip
import sqlite3
import requests


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
    connection = ''
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM RDAP;")
        cursor.execute("COMMIT;")

        cursor.execute("BEGIN TRANSACTION;")
        for ip in list_of_ips:
            cursor.execute('INSERT INTO rdap VALUES (?, ?, ?, ?)', (ip, '', '', ''))
        cursor.execute("COMMIT;")
        print("IP INSERTION DONE")

    except sqlite3.Error as error:
        print("Failed to insert IP Address", error)
    finally:
        if connection:
            connection.close()


def insert_rdap():
    connection = ''
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()
        ip_list = cursor.execute("Select ipaddr from rdap").fetchall()
        sql_update = '''UPDATE rdap
                              SET CIDR = ?,
                                  range_lower = ?, 
                                  range_upper = ?
                              WHERE ipaddr = ?;'''

        # Session reduces by 45 % time for bulk requests
        rdap_session = requests.Session()
        with rdap_session:
            for ip in ip_list:
                data = rdap.get_rdap_info(ip[0], rdap_session)
                if data != None:
                    cursor.execute(sql_update, (data[0], data[1], data[2], data[3]))
                    connection.commit()
        print("RDAP UPDATE DONE")
    
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
    except sqlite3.Error as error:
        print(error)

    finally:
        if connection:
            connection.close()


def insert_geo_ip():
    connection = ''
    try:
        connection = sqlite3.connect("ipdata.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM GEOIP;")
        cursor.execute("COMMIT;")

        ip_list = cursor.execute("Select ipaddr from rdap").fetchall()
        sql_insert = '''INSERT INTO geoip VALUES
                               (?, ?, ?, ?, ?, ?)
                               '''

        # Session reduces by 45 % time for bulk requests
        geoip_session = requests.Session()
        with geoip_session:
            for ip in ip_list:
                data = geoip.get_geoip_info(ip[0], geoip_session)
                if data != None:
                    cursor.execute(sql_insert, (data[0], data[1], data[2], data[3], data[4], data[5]))
                    connection.commit()
        print("GEOIP INSERT DONE")

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
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


if __name__ == "__main__":
    file = "./test_data/list_of_ips.txt"
    create_db()
    insertions_ip(file)
