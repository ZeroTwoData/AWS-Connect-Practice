import boto3
import time
import datetime

# AWS Connect client
connect_client = boto3.client('connect')

# Define the instance ID and report name
instance_id = 'your-instance-id'
report_name = 'your-report-name'

# Specify the time range for the report (e.g., last 7 days)
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=7)

# Generate a unique report identifier
report_id = f"report-{int(time.time())}"

# Request the report
response = connect_client.start_report_generation(
    InstanceId=instance_id,
    ReportName=report_name,
    StartTime=start_time.timestamp(),
    EndTime=end_time.timestamp(),
    Filters={
        'Queues': ['queue-name'],
        # Add other filters as needed
    },
    ReportId=report_id
)

# Wait for the report to complete
while True:
    status_response = connect_client.get_report_generation({
        'InstanceId': instance_id,
        'ReportId': report_id
    })
    status = status_response['Report']['Status']
    
    if status == 'COMPLETE':
        break
    
    time.sleep(10)

# Retrieve the report contents
report_response = connect_client.get_report_generation({
    'InstanceId': instance_id,
    'ReportId': report_id
})
report_url = report_response['Report']['ReportUrl']

# Download the report
# You can use libraries like requests to download the report
import requests

report_data = requests.get(report_url).content

# Save report data to a CSV or Excel file
# You can use libraries like pandas to handle data and file formats
import pandas as pd

# Assuming the report is in CSV format
report_df = pd.read_csv(io.StringIO(report_data.decode('utf-8')))
report_df.to_csv('report.csv', index=False)

# Alternatively, if the report is in Excel format
report_df.to_excel('report.xlsx', index=False)
