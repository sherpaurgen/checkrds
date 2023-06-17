import boto3
from datetime import datetime,timedelta

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
def get_rdsmemory_usage(data):
    Namespace = "FreeStorageSpace"
    client = boto3.client('cloudwatch',region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_memory_usage',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'FreeableMemory',
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': data['DBInstanceIdentifier']
                            }
                        ]
                    },
                    'Period': 120,  # Fetch data in 120-second intervals
                    'Stat': 'Average',  # Compute the average CPU usage
                },
            },
        ],
        'StartTime': start_time,
        'EndTime': end_time,
    }
    response = client.get_metric_data(**queryparams)
    if response["MetricDataResults"][0]["Values"]:
        cpuusage = response["MetricDataResults"][0]["Values"][0]
    data["mem_usage"] = cpuusage
    return (data)


