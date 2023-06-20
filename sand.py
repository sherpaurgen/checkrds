import boto3
from datetime import datetime,timedelta

def getTargetResponseTime():
    cloudwatch = boto3.client('cloudwatch',region_name='us-east-1')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)
    dimensions = [
        {
            "Name": "LoadBalancer",
            "Value": "app/myLoadbalancer1/c0389851c55b8fa4"
        },
    ]

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='TargetResponseTime',
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=600,
        Statistics=['Average']
    )
    print(f"{response}\n\n")

getTargetResponseTime()