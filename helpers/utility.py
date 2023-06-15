import boto3

def list_available_db(region_name,Namespace):
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
                       "Engine": Engine, "region_name": region_name, "Namespace": Namespace})
    return (dblist)