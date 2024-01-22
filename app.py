import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_logs(bucket_name):
    logs = []
    s3 = boto3.client('s3')

    try:
        response = s3.list_objects(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            # Fetch and display logs from the S3 bucket
            log = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
            logs.append(log['Body'].read().decode('utf-8'))
    except NoCredentialsError:
        st.error("Credentials not available. Make sure you have configured your AWS credentials.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    return logs

def main():
    st.title("S3 Log Viewer")

    # Get the S3 bucket name from the user
    bucket_name = st.text_input("Enter S3 Bucket Name:")
    
    if st.button("View Logs"):
        if bucket_name:
            logs = get_s3_logs(bucket_name)
            for log in logs:
                st.text(log)
        else:
            st.warning("Please enter an S3 bucket name.")

if __name__ == "__main__":
    main()
