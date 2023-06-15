import boto3
import yaml
import os
from dbhandler.db import create_diskusage_table
from dbhandler.db import create_memusage_table


def list_available_db(region_name):
    dblist = []
    client = boto3.client('rds', region_name="us-east-1")
    response = client.describe_db_instances()
    for db_instance in response['DBInstances']:
        DBInstanceIdentifier = db_instance["DBInstanceIdentifier"]
        DBInstanceClass = db_instance["DBInstanceClass"]
        Engine = db_instance["Engine"]
        AllocatedStorage = db_instance["AllocatedStorage"]
        region_name = region_name
        dblist.append({"DBInstanceIdentifier": DBInstanceIdentifier, "AllocatedStorage": AllocatedStorage,
                       "DBInstanceClass": DBInstanceClass,
                       "Engine": Engine, "region_name": region_name})
    return (dblist)


def main():
    cwd = os.getcwd()
    rds_conf_path = cwd + '/config/rds.yaml'
    dbfile = cwd + '/rds_stat.db'

    with open(rds_conf_path, 'r') as fh:
        data = yaml.safe_load(fh)
    tmp_alldb = []

    for region in data['Regions']:
        tmp_alldb.append(list_available_db(region))
    alldb = []
    if len(tmp_alldb) > 0:
        for objlist in tmp_alldb:
            if len(objlist) > 0:
                for db in objlist:
                    alldb.append(db)

    print(alldb)
    create_diskusage_table(dbfile)
    create_memusage_table(dbfile)


if __name__ == '__main__':
    main()
