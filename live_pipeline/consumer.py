"""Live-data pipeline. Consuming messages from Kafka, cleaning the data and upload to database."""
import logging
import json
import argparse
from os import environ
from datetime import datetime, time, timezone
from dotenv import load_dotenv
from confluent_kafka import Consumer
import psycopg2
import psycopg2.extras

# pylint:disable=W0718
# pylint:disable=C0301


TOPIC = "lmnh"


def get_connection():
    """Connect to database"""
    load_dotenv(".env.prod")

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


def consume_messages_with_logging(cons: Consumer) -> None:
    """Processes and logs one out of every 20 Kafka messages"""

    logging.info("Connecting To Database")
    conn = get_connection()
    cursor = get_cursor(conn)
    logging.info("Connected to %s",
                 environ['DATABASE_NAME'])

    message_count = 0
    while True:
        msg = cons.poll(1.0)
        if msg is None:
            logging.debug("No more messages available at the moment.")
        elif msg.error():
            logging.error("ERROR: %s", msg.error())

        else:
            message_count += 1
            decoded_msg = msg.value().decode('utf-8')
            is_valid, validation_message = validate_consumed_messages(
                decoded_msg)
            if is_valid:
                logging.info("Message %s: %s", message_count, decoded_msg)
                upload_to_database(conn, cursor, decoded_msg)
            else:
                logging.warning("Invalid Message %s: %s - %s",
                                message_count, validation_message, decoded_msg)


def validate_timestamp(timestamp: str) -> tuple:
    """Validates timestamp is correct (not in the future and during opening times)"""
    try:
        message_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        now = datetime.now(timezone.utc)

        opening_time = time(8, 45)
        closing_time = time(18, 15)

        if not opening_time <= message_time.time() <= closing_time:
            return False, "Outside Of Museum Opening Times (8:45AM - 6:15PM)"
        if message_time > now:
            return False, "Interaction Cannot Be From The Future"
        return True, ""
    except ValueError as e:
        return False, (f"Invalid Timestamp format: {e}")


def validate_site(site: str) -> tuple:
    """Validates site value"""
    valid_sites = ['0', '1', '2', '3', '4', '5']
    return (site in valid_sites, "" if site in valid_sites else "Invalid Exhibition Site")


def validate_rating(rating: str) -> tuple:
    """Validates rating value"""
    valid_rating = ['-1', '0', '1', '2', '3', '4']
    return (rating in valid_rating, "" if rating in valid_rating else "Rating must be between -1 and 4")


def validate_request(request: str) -> tuple:
    """Validates request value (only when rating is -1)"""
    valid_request = ['0', '1']
    return (request in valid_request, "" if request in valid_request else "Request must be 0 or 1")


def validate_consumed_messages(message: str) -> tuple:
    """Validates messages consumed"""
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"

    required_keys = ['val', 'at', 'site']
    for key in required_keys:
        if key not in data:
            return False, f"Missing key: '{key}"

    at = data.get('at', '')
    site = data.get('site', '')
    val = str(data.get('val', ''))
    type_val = str(data.get('type', ''))

    is_valid, msg = validate_timestamp(at)
    if not is_valid:
        return False, msg

    is_valid, msg = validate_site(site)
    if not is_valid:
        return False, msg

    is_valid, msg = validate_rating(val)
    if not is_valid:
        return False, msg

    if val == "-1":
        is_valid, msg = validate_request(type_val)
        if not is_valid:
            return False, msg

    return True, msg


def insert_rating_interaction(cursor, conn, exhibition_id: int, val: str, at: str) -> None:
    """Add kiosk data to rating interaction table"""
    cursor.execute(
        """SELECT rating_id FROM rating WHERE rating_value = %s""", (val,))

    rating = cursor.fetchone()
    rating_id = rating[0] if rating else None

    cursor.execute("""
    INSERT INTO rating_interaction (exhibition_id, rating_id, event_at)
    VALUES (%s, %s, %s);""", (exhibition_id, rating_id, at))

    conn.commit()


def insert_request_interaction(cursor, conn, exhibition_id: int, type_val: int, at: str) -> None:
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


def upload_to_database(conn, cursor, message: str) -> None:
    """Uploads valid messages to database"""
    data = json.loads(message)

    val = str(data.get('val', ''))
    type_val = str(data.get('type', ''))
    at = data.get('at', '')
    site = data.get('site', '')

    exhibition_id = int(site) + 1
    type_val = int(float(type_val)) if type_val else None

    if int(val) in range(5):  # Assuming valid rating values are 0-4
        insert_rating_interaction(
            cursor, conn, exhibition_id, val, at)
    else:  # Insert into request_interaction table
        insert_request_interaction(
            cursor, conn, exhibition_id, type_val, at)

    logging.info("Inserted data")


def config_log_terminal() -> None:
    """Logging to the terminal"""
    logging.basicConfig(
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )


def config_log_file() -> None:
    """Logging to the file"""
    logging.basicConfig(
        filename="consumer_errors.txt",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )


def get_args() -> argparse.Namespace:
    """Command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", "-f", action="store_true",
                        help="To log invalid messages to file (optional)")

    return parser.parse_args()


def create_kafka_consumer() -> Consumer:
    """Sets up and returns a Kafka consumer"""
    kafka_config = {
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        "security.protocol": environ["SECURITY_PROTOCOL"],
        "sasl.mechanisms": environ["SASL_MECHANISM"],
        "sasl.username": environ["USERNAME"],
        "sasl.password": environ["PASSWORD"],
        "group.id": "c14-gem",
        "auto.offset.reset": "latest"
    }

    logging.info("Configuring consumer")
    consumer = Consumer(kafka_config)
    consumer.subscribe([TOPIC])
    return consumer


if __name__ == "__main__":

    load_dotenv(".env")

    args = get_args()
    if args.logs:
        config_log_file()
    else:
        config_log_terminal()

    consumer = create_kafka_consumer()

    try:
        consume_messages_with_logging(
            consumer)
    except Exception as e:
        logging.error("Error with Consuming Messages: %s", e)
    finally:
        logging.info("Closing Consumer")
        consumer.close()
        logging.info("Closed Consumer")
