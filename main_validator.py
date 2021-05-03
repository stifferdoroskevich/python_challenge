from ingest import ip_by_file
from sql import sql
import argparse


def options_selector():
    while True:
        decision = input("""
            1. Populate Database with small dataset
            2. Populate Database with full dataset
            3. Populate Database with file
            4. Return All IP Rdap Information
            5. Return All IP Geolocation
            (Answer with the number option)\n
            """)
        if decision in '12345':
            return decision
        elif decision == 'exit':
            break
        else:
            print("\nPlease insert a valid option or type 'exit' to end")


def main():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--file', action='store', type=str)
    args = my_parser.parse_args()

    decision = ''

    if args.file:
        sql.create_db()
        file_dir = 'test_data/' + args.file
        with open(file_dir, 'r'):
            returned_list = ip_by_file.ip_parser(file_dir)
            sql.insertions_ip(returned_list)
            sql.insert_rdap()
            sql.insert_geo_ip()
    else:
        print('\nWelcome to IP Validator 0.1 !\n What do you want to do today?')
        decision = options_selector()

    if decision == "1":
        returned_list = ip_by_file.ip_parser('./test_data/list_of_ips_small.txt')
        sql.create_db()
        sql.insertions_ip(returned_list)
        sql.insert_rdap()
        sql.insert_geo_ip()
    elif decision == "2":
        returned_list = ip_by_file.ip_parser('./test_data/list_of_ips.txt')
        sql.create_db()
        sql.insertions_ip(returned_list)
        sql.insert_rdap()
        sql.insert_geo_ip()
    elif decision == "3":
        print("Put the file inside 'test_data' folder and run python main_validator.py --file [name_of_file]")
    elif decision == "4":
        print(sql.query_rdap())
    elif decision == "5":
        print(sql.query_geoip())


if __name__ == "__main__":
    main()
