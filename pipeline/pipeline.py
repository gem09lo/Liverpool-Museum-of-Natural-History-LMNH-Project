"""Main pipeline. Downloads the data from S3, uploads and it into the PostgreSQL database."""
import csv
import logging
import argparse
from os import environ
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
from extract import connect_to_s3, download_files_from_s3, combine_csv_files


def get_connection():
    """Connect to database"""
    return psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_HOST"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def get_cursor(conn):
    """Returns cursor"""
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def insert_rating_interaction(cursor, conn, exhibition_id, val, at):
    """Add kiosk data to rating interaction table"""

    cursor.execute(
        """SELECT rating_id FROM rating WHERE rating_value = %s""", (val,))

    rating = cursor.fetchone()
    rating_id = rating[0] if rating else None

    cursor.execute("""
    INSERT INTO rating_interaction (exhibition_id, rating_id, event_at)
    VALUES (%s, %s, %s);""", (exhibition_id, rating_id, at))

    conn.commit()


def insert_request_interaction(cursor, conn, exhibition_id, type_val, at):
    """Add kiosk data to request interaction table"""

    cursor.execute(
        """SELECT request_id FROM request WHERE request_value = %s""", (type_val,))
    request = cursor.fetchone()
    request_id = request[0] if request else None

    cursor.execute("""
    INSERT INTO request_interaction (exhibition_id, request_id, event_at)
    VALUES (%s, %s, %s);
    """, (exhibition_id, request_id, at))

    conn.commit()


def upload_to_database(cursor, conn, csv_file_path, rows):
    """Uploads data from a CSV file to the museum database."""

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        try:
            for i, row in enumerate(csv_reader):
                if i >= rows:
                    break
                at, site, val, type_val = row

                exhibition_id = int(site) + 1
                type_val = int(float(type_val)) if type_val else None

                if int(val) in range(5):  # Assuming valid rating values are 0-4
                    insert_rating_interaction(
                        cursor, conn, exhibition_id, val, at)
                else:  # Insert into request_interaction table
                    insert_request_interaction(
                        cursor, conn, exhibition_id, type_val, at)
            logging.info("Data uploaded successfully to database")
        except psycopg2.OperationalError as e:
            logging.error("Could not upload to database: %s", e)


def config_log_file():
    """Logging to the file"""
    logging.basicConfig(
        filename="pipeline.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )


def config_log_terminal():
    """Logging to the terminal"""
    logging.basicConfig(
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )


def get_args():
    """Command line arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--bucket", "-b", required=True,
                        help="Specify the name of the S3 Bucket to connect to")
    parser.add_argument("--rows", "-r", type=int, required=True,
                        help="Specify number of rows to upload to database")  # on/off flag
    parser.add_argument("--logs", "-l", action="store_true",
                        help="To log to file")

    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":

    load_dotenv(".env.prod")

    args = get_args()
    if args.logs:
        config_log_file()
    else:
        config_log_terminal()

    logging.info("Connecting To S3 Bucket")
    s3 = connect_to_s3()

    csv_files = download_files_from_s3(
        s3, args.bucket, 'lmnh_hist_data', '.csv')

    combine_csv_files(csv_files)

    logging.info("Connecting To Database")
    connection = get_connection()
    cur = get_cursor(connection)
    logging.info("Connected to %s",
                 environ['DATABASE_NAME'])

    upload_to_database(cur, connection, 'lmnh_hist_data.csv', args.rows)

    logging.info("Closing Database Connection")
    cur.close()
    connection.close()
    logging.info("Connection Closed")
