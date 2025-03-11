"""Connects to s3 bucket and extracts relevant json and csv files."""
import os
import logging
from boto3 import client
from dotenv import load_dotenv, dotenv_values


# pylint:disable=W0718


def connect_to_s3():
    """Connects to S3 using credentials from .env file"""
    try:
        config = dotenv_values()

        s3 = client("s3", aws_access_key_id=config["ACCESS_KEY_ID"],
                    aws_secret_access_key=config["SECRET_ACCESS_KEY"])

        logging.info("Connected To S3 Bucket Successfully")
        return s3
    except Exception as e:
        logging.error("Connection To S3 Bucket Failed: %s", e)
        return e


def download_files_from_s3(s3, bucket_name, file_prefix, file_extension):
    """Downloads files from an S3 bucket"""
    bucket = s3.list_objects(Bucket=bucket_name)

    contents = bucket.get("Contents", [])

    files_needed = []

    try:
        for file in contents:
            data = file["Key"]
            if data.startswith(file_prefix) and data.endswith(file_extension):
                files_needed.append(data)

        for file in files_needed:
            s3.download_file(bucket_name,
                             file, file)
        logging.info("Files Downloaded Successfully")
        return files_needed
    except Exception as e:
        logging.error("Files Download Failed: %s", e)
        return files_needed


def combine_csv_files(csv_files):
    """Combines downloaded CSV files into a single file 'lmnh_hist_data.csv'"""
    with open('lmnh_hist_data.csv', 'w', encoding='utf-8') as output_file:
        output_file.write("at,site,val,type\n")

    try:
        for filename in csv_files:
            with open(filename, 'r', encoding='utf-8') as open_csv:
                first_row = True
                for line in open_csv:
                    if first_row:
                        first_row = False
                        continue

                    with open('lmnh_hist_data.csv', 'a', encoding='utf-8') as output_file:
                        output_file.write(line)

            os.remove(filename)
        logging.info("CSV Files Combined Successfully")
    except Exception as e:
        logging.error("CSV Files Combine Failed: %s", e)


if __name__ == "__main__":
    load_dotenv()

    client = connect_to_s3()

    all_csv_files = download_files_from_s3(
        client, "sigma-resources-museum", 'lmnh_hist_data', '.csv')
    json_files = download_files_from_s3(
        client, "sigma-resources-museum", 'lmnh_exhibition', '.json')

    combine_csv_files(all_csv_files)
