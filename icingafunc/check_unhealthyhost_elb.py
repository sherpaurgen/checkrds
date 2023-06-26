#!/monitoringScripts/VENVT/bin/python
import sys
import sqlite3
import os

script_home = os.path.dirname(os.path.abspath(__file__))
dbpath = script_home+"/../rds_stat.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

LoadBalancerName = sys.argv[1]
region_name = sys.argv[2]

# Define the query to select the latest record -only1 row
query = "SELECT unhealthycount FROM elbtargetgroup WHERE LoadBalancerName = ? and region_name = ?  ORDER BY id DESC LIMIT 1;"
rows = cursor.execute(query, (LoadBalancerName,region_name))
for row in rows:
    unhealthycount = row[0]

if unhealthycount >= 2:
    print(f"CRITICAL - Number of unhealthy hosts is above threshold {unhealthycount}" )
    sys.exit(2)
elif unhealthycount >= 1:
    print(f"WARNING - Number of unhealthy hosts is above threshold {unhealthycount}" )
    sys.exit(1)
else:
    print(f"OK - unhealthy hosts not found")
    sys.exit(0)
