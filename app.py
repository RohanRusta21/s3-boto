import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_logs(bucket_name, access_key, secret_key):
    logs = []
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        response = s3.list_objects(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            # Fetch and display logs from the S3 bucket
            log = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
            logs.append(log['Body'].read())
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
