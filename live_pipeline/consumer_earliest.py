"""Experimenting with Kafka consuming messages in batch."""
from os import environ
import logging
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException, KafkaError

TOPIC = "lmnh"
MESSAGE_LIMIT = 100


def consume_one_message(cons: Consumer) -> None:
    """Processes one Kafka message then exits"""
    msg = cons.poll(1.0)
    if msg:
        print(msg.value().decode("utf-8"))
        return
    cons.close()


def consume_one_hundred_messages(cons: Consumer) -> None:
    """Processes one hundred Kafka message then exits"""
    message_count = 0
    max_messages = 100

    while message_count < max_messages:
        msg = cons.poll(1.0)

        if msg is None:
            print("No more messages available at the moment")
            break
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue  # Skip any messages with errors

        if msg:
            print(msg.value().decode("utf-8"))
            message_count += 1

    cons.close()


def consume_messages_with_logging(cons: Consumer, message_limit) -> None:
    """Processes and logs one out of every 20 Kafka messages"""
    consumer.subscribe([TOPIC])

    message_count = 0
    log_every = 20  # Log every 20th message

    while message_count < message_limit:
        msg = cons.poll(1.0)

        if msg is None:
            logging.debug("No more messages available at the moment.")
            # break
            continue
        elif msg.error():
            logging.error("ERROR: %s", msg.error())
            continue

        if msg:
            message_count += 1
            # Log every 20th message
            if message_count % log_every == 0:
                logging.info(f"Message {message_count}: {
                    msg.value().decode('utf-8')}")

    logging.info("Reached Message Limit (%s).", message_limit)


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


if __name__ == "__main__":

    load_dotenv()
    config_log_terminal()

    kafka_config = {
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        "security.protocol": environ["SECURITY_PROTOCOL"],
        "sasl.mechanisms": environ["SASL_MECHANISM"],
        "sasl.username": environ["USERNAME"],
        "sasl.password": environ["PASSWORD"],
        "group.id": "sigma-labs",  # change
        "enable.auto.commit": "true",
        "enable.auto.offset.store": "false",
        "auto.offset.reset": "earliest",
        "fetch.min.bytes": 1,
        "fetch.wait.max.ms": 100
    }

    logging.info("Configuring consumer")
    consumer = Consumer(kafka_config)

    # consume_messages(consumer)
    # consume_one_message(consumer)
    # consume_one_hundred_messages(consumer)

    try:
        consume_messages_with_logging(consumer, MESSAGE_LIMIT)
    except Exception as e:
        logging.error("Error with Consuming Messages: %s", e)
    finally:
        logging.info("Closing Consumer")
        consumer.close()
        logging.info("Closed Consumer")
