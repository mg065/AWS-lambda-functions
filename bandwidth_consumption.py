import boto3
import psycopg2
from psycopg2 import Error
import pandas as pd


# Read CSV file content from S3 bucket
def read_data_from_s3(event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]

    aws_access_key = '<access-key>'
    aws_secret_key = '<secret-key>'
    s3_conn = boto3.resource('s3', aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key)

    region = '<region-link>'
    object_key = '/' + object_name
    s3path = region + bucket_name + object_key
    print(s3path)

    object_acl = s3_conn.ObjectAcl(bucket_name, object_name)
    response = object_acl.put(ACL='public-read')
    print(response)

    df = pd.read_csv(s3path)
    if len(df):
        print(len(df))
        total_bytes_rows = df.groupby(
            ['User_id', 'Project_id', 'Company_id', 'Guest_User', 'User_Role', 'State_id', 'Date'])[
                ['Bytes_Sent']].sum().reset_index()

        print(len(total_bytes_rows))
        return total_bytes_rows, object_name

    else:
        return {'total_bytes_rows': None}


def lambda_handler(event, context):
    rds_endpoint = '<db-connection-link>'
    username = '<db-username>'
    password = 'db-password'  # RDS  PostgresSQL password
    db_name = 'db-name'  # RDS PostgresSQL DB name
    port = '5432'  # it's by default
    conn = None
    try:
        print('trying to connect with the database...')

        conn = psycopg2.connect(host=rds_endpoint,
                                user=username,
                                password=password,
                                port=port,
                                database=db_name)

        print('connection built successfully!')

    except (Exception, Error) as error:
        print("Error while connecting to PostgresSQL", error)

    # getting csv file
    total_bandwidth_rows, s3_file_name = read_data_from_s3(event)

    for index, row in total_bandwidth_rows.iterrows():
        user_id = int(row[0])
        project_alphaid = row[1]
        company_id = int(row[2])
        guest_user_id = int(row[3])
        user_role_name = row[4]
        state_id = int(row[5])
        date = row[6]
        if row[7] is None:
            bytes_sent = 0
        else:
            bytes_sent = float(row[7])

        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO <table-name> (user_id, project_alphaid, company, guest_user, user_role_name, state_id, created_date, last_file_name, bandwidth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user_id, project_alphaid, company_id, guest_user_id, user_role_name, state_id, date, s3_file_name, bytes_sent))
                conn.commit()

            except Exception as e:
                print(e)
                continue

    print('Testing/Staging/local  Database table updated')