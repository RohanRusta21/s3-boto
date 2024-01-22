import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
from transformers import pipeline

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

def analyze_logs(logs):
    # Use a pre-trained model for text summarization
    summarizer = pipeline("summarization")
    solutions = []

    for log in logs:
        # Summarize each log to extract key information
        summary = summarizer(log.decode("utf-8"), max_length=100, min_length=5, length_penalty=2.0, num_beams=4, early_stopping=True)
        solutions.append(summary[0]['summary'])

    return solutions

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
            
            if logs:
                solutions = analyze_logs(logs)
                for log, solution in zip(logs, solutions):
                    st.subheader("Log:")
                    st.text(log.decode("utf-8"))
                    st.subheader("Solution:")
                    st.text(solution)
            else:
                st.warning("No logs found in the specified S3 bucket.")
        else:
            st.warning("Please enter all required information.")

if __name__ == "__main__":
    main()
