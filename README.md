# AWS-lambda-function-csv-to-rds
How to utilize the features of AWS sever-less lambda functions.

Steps in bash scripts:
- Syncing logs of all regions to server machine in parallel(reading from regions.txt file).
- Deleting all-region logs from the bucket(reading from region_logs.txt file).
- Filtering logs by 'x-user_id' and moving them into separate folders.
- Replacing 'x-user_id' by 'user_id'
- Running a python script to parse the logs and save them into the CSV file with respect to the environment.
- Syncing CSV file to s3 bucket (i.e bucketalilogs)
- Cleaning work of the server machine by removing all logs and CSV files.


