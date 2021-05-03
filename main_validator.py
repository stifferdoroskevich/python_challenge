from ingest import ip_by_file
from database import sql


returned_list = ip_by_file.ip_parser('./test_data/list_of_ips_small.txt')
sql.create_db()
sql.insertions_ip(returned_list)
sql.insert_rdap()
sql.insert_geo_ip()
print(sql.query_rdap())
print(sql.query_geoip())
