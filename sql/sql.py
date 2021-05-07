from lookup import rdap, geoip
from sql import db_sqls
import sqlite3
import requests


def create_db():
    connection, cursor = db_connect()
    db_sqls.create_tables(cursor)
    connection.commit()
    connection.close()


def db_connect():
    '''
    Connection to database.
    Creates ipdata.db SQLite File.
    :return:
    tuple: connection, cursor
    '''
    connection = sqlite3.connect("ipdata.db")
    cursor = connection.cursor()
    return connection, cursor


def insertions_ip(list_of_ips):
    try:
        connection, cursor = db_connect()

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
    try:
        connection, cursor = db_connect()
        ip_list = db_sqls.get_ips(cursor)
        sql_update = '''UPDATE rdap
                              SET CIDR = ?,
                                  range_lower = ?, 
                                  range_upper = ?
                              WHERE ipaddr = ?;'''

        # Session reduced by 45 % time for bulk requests
        rdap_session = requests.Session()
        with rdap_session:
            for ip in ip_list:
                data = rdap.get_rdap_info(ip[0], rdap_session)
                if data is not None:
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
    try:
        connection, cursor = db_connect()

        ip_list = db_sqls.get_ips(cursor)
        sql_insert = '''INSERT INTO geoip VALUES
                               (?, ?, ?, ?, ?, ?)
                               '''

        # Session reduced by 45 % time for bulk requests
        geoip_session = requests.Session()
        with geoip_session:
            for ip in ip_list:
                data = geoip.get_geoip_info(ip[0], geoip_session)
                if data is not None:
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
    connection, cursor = db_connect()
    cursor.execute("Select * from rdap")
    result = cursor.fetchall()
    connection.close()
    return result


def query_geoip():
    connection, cursor = db_connect()
    cursor.execute("Select * from geoip")
    result = cursor.fetchall()
    connection.close()
    return result


def clean_database():
    connection, cursor = db_connect()
    cursor.executescript("DELETE FROM RDAP; DELETE FROM GEOIP;")
    connection.close()
    return "Database Cleaned"


if __name__ == "__main__":
    file = "./test_data/list_of_ips_small.txt"
    create_db()
    insertions_ip(file)
    insert_rdap()
