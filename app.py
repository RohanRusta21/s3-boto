# import streamlit as st
# import boto3
# from botocore.exceptions import NoCredentialsError

# def get_s3_logs(bucket_name, access_key, secret_key):
#     logs = []
#     s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

#     try:
#         response = s3.list_objects(Bucket=bucket_name)
#         for obj in response.get('Contents', []):
#             # Fetch and display logs from the S3 bucket
#             log = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
#             logs.append(log['Body'].read())
#     except NoCredentialsError:
#         st.error("Credentials not available. Make sure you have entered valid AWS access key and secret key.")
#     except Exception as e:
#         st.error(f"An error occurred: {e}")

#     return logs

# def main():
#     st.title("S3 Log Viewer")

#     # Get AWS credentials from the user
#     access_key = st.text_input("Enter AWS Access Key:")
#     secret_key = st.text_input("Enter AWS Secret Key:", type="password")

#     # Get the S3 bucket name from the user
#     bucket_name = st.text_input("Enter S3 Bucket Name:")

#     if st.button("View Logs"):
#         if bucket_name and access_key and secret_key:
#             logs = get_s3_logs(bucket_name, access_key, secret_key)
#             for log in logs:
#                 st.text(log)
#         else:
#             st.warning("Please enter all required information.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import re

def parse_log(log_entry):
    # Modified regular expression pattern to handle multiple spaces between fields
    pattern = re.compile(r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)$')

    match = pattern.match(log_entry.decode('utf-8'))

    if match:
        timestamp, client_ip, user_arn, request_id, event_type, bucket_name, \
        key, request_uri, http_status, error_code, bytes_sent, object_size, \
        total_time, turn_around_time, referrer, user_agent = match.groups()

        return {
            "Timestamp": timestamp,
            "Client IP": client_ip,
            "User ARN": user_arn,
            "Request ID": request_id,
            "Event Type": event_type,
            "Bucket Name": bucket_name,
            "Key": key,
            "Request URI": request_uri,
            "HTTP Status": http_status,
            "Error Code": error_code,
            "Bytes Sent": bytes_sent,
            "Object Size": object_size,
            "Total Time": total_time,
            "Turnaround Time": turn_around_time,
            "Referrer": referrer,
            "User Agent": user_agent,
        }
    else:
        st.text(f"Log Entry:\n{log_entry.decode('utf-8')}")
        return None


def format_log(parsed_log, raw_log_entry):
    if parsed_log:
        formatted_log = (
            f"Timestamp: {parsed_log.get('Timestamp', 'N/A')}\n"
            f"Client IP: {parsed_log.get('Client IP', 'N/A')}\n"
            f"User ARN: {parsed_log.get('User ARN', 'N/A')}\n"
            f"Request Method: {parsed_log.get('Request Method', 'N/A')}\n"
            f"Requested Resource: {parsed_log.get('Requested Resource', 'N/A')}\n"
            f"Status Code: {parsed_log.get('Status Code', 'N/A')}\n"
            f"Referrer: {parsed_log.get('Referrer', 'N/A')}\n"
            f"User Agent: {parsed_log.get('User Agent', 'N/A')}\n"
            f"Version ID: {parsed_log.get('Version ID', 'N/A')}\n"
            f"Host ID: {parsed_log.get('Host ID', 'N/A')}"
        )
        return formatted_log
    else:
        return "Invalid log entry"

def get_s3_logs(bucket_name, access_key, secret_key):
    logs = []
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        response = s3.list_objects(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            # Fetch and display logs from the S3 bucket
            log = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
            parsed_log = parse_log(log['Body'].read())
            formatted_log = format_log(parsed_log, log['Body'].read())
            logs.append(formatted_log)
    except NoCredentialsError:
        st.error("Credentials not available. Make sure you have entered valid AWS access key and secret key.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    return logs

def main():
    st.title("S3 Log Viewer")

    # Get AWS credentials from the user
    access_key = st.text_input("Enter AWS Access Key:")
    secret_key = st.text_input("Enter AWS Secret Key:", type="password")

    # Get the S3 bucket name from the user
    bucket_name = st.text_input("Enter S3 Bucket Name:")

    if st.button("View Logs"):
        if bucket_name and access_key and secret_key:
            logs = get_s3_logs(bucket_name, access_key, secret_key)
            for log in logs:
                st.text(log)
        else:
            st.warning("Please enter all required information.")

if __name__ == "__main__":
    main()

