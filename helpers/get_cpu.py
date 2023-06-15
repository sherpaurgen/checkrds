import boto3
from datetime import datetime, timedelta


def get_cpu_usage(data):
    client = boto3.client('cloudwatch', region_name=data["region_name"])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    queryparams = {
        'MetricDataQueries': [
            {
                'Id': 'rds_cpu_usage',
                'MetricStat': {
                    'Metric': {
                        'Namespace': data['Namespace'],  # AWS/EC2
                        'MetricName': 'CPUUtilization',
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
    data["cpu_usage"] = cpuusage
    return(data)
