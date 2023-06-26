#!/monitoringScripts/VENVT/bin/python
import sys
import sqlite3
import os

script_home = os.path.dirname(os.path.abspath(__file__))
dbpath = script_home+"/../rds_stat.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

LoadBalancerName=sys.argv[1]
region_name=sys.argv[2]

# Define the query to select the latest record -only1 row
query = "SELECT avg_response_time FROM elbresponsetime WHERE LoadBalancerName = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows = cursor.execute(query, (LoadBalancerName,region_name))
for row in rows:
    avg_response_time = row[0]

if avg_response_time >= 5:
    print(f"CRITICAL - cpu usage is above threshold {avg_response_time} sec" )
    sys.exit(2)
elif avg_response_time >= 6:
    print(f"WARNING - cpu usage is approaching threshold {avg_response_time}" )
    sys.exit(1)
else:
    print(f"OK - cpu usage is within limits {avg_response_time} sec")
    sys.exit(0)
