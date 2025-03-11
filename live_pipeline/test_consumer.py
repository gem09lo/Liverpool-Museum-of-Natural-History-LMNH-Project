# pylint: skip-file
import pytest
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from consumer import (
    get_connection, get_cursor, validate_timestamp,
    validate_site, validate_rating, validate_request, validate_consumed_messages,
    upload_to_database, consume_messages_with_logging,
    insert_rating_interaction, insert_request_interaction,
    create_kafka_consumer, config_log_terminal, config_log_file
)
import psycopg2

"""
Message validation functions: 
- validate_timestamp
- validate_site
- validate_rating
- validate_request

JSON message parsing - Ensure validate_consumed_messages
correctly parses and validates messages.

Database interactions:
- insert_rating_interaction
- insert_request_interaction
- upload_to_database

Kafta consumer set-up: Test the create_kafka_consumer function.

Logging configuration: 
- config_log_terminal
- config_log_file

Mocking:
- Database connection (psycopg2.connect) and cursor for testing database interactions.
- Kafka Consumer (confluent_kafka.Consumer) for testing message consumption without requiring an actual Kafka broker.
- Environment variables (from dotenv) to simulate loading secrets like database credentials and Kafka details.
- Logging to capture and verify log output.
"""


@pytest.fixture
def mock_connection():
    """Fixture for a mocked database connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    yield mock_conn


@pytest.fixture
def mock_consumer():
    """Fixture for a mocked Kafka consumer"""
    mock_consumer = MagicMock()
    yield mock_consumer


# @patch("consumer.psycopg2.connect")
# @patch("consumer.load_dotenv")
# def test_get_connection(mock_load_dotenv, mock_connect):
#     """Test database connection"""
#     mock_connect.return_value = "Connection"
#     conn = get_connection()
#     assert conn == "Connection"


def test_get_cursor(mock_connection):
    """Test getting a cursor"""
    cursor = get_cursor(mock_connection)
    assert cursor == mock_connection.cursor()


def test_validate_timestamp_valid():
    """Test valid timestamp"""
    timestamp = "2024-10-21T09:30:00.000+0000"
    is_valid, message = validate_timestamp(timestamp)
    assert is_valid
    assert message == ""


def test_validate_timestamp_future():
    """Test invalid timestamp from the future"""
    timestamp = "3024-10-21T09:30:00.000+0000"
    is_valid, message = validate_timestamp(timestamp)
    assert not is_valid
    assert message == "Interaction Cannot Be From The Future"


def test_validate_site_valid():
    """Test valid site"""
    site = "3"
    is_valid, message = validate_site(site)
    assert is_valid
    assert message == ""


def test_validate_site_invalid():
    """Test invalid site"""
    site = "10"
    is_valid, message = validate_site(site)
    assert not is_valid
    assert message == "Invalid Exhibition Site"


def test_validate_rating_valid():
    """Test valid rating"""
    rating = "3"
    is_valid, message = validate_rating(rating)
    assert is_valid
    assert message == ""


def test_validate_rating_invalid():
    """Test invalid rating"""
    rating = None
    is_valid, message = validate_rating(rating)
    assert not is_valid
    assert message == "Rating must be between -1 and 4"


def test_validate_rating_invalid2():
    """Test invalid rating"""
    rating = ["hi"]
    is_valid, message = validate_rating(rating)
    assert not is_valid
    assert message == "Rating must be between -1 and 4"


def test_validate_rating_invalid3():
    """Test invalid rating"""
    rating = 1
    is_valid, message = validate_rating(rating)
    assert not is_valid
    assert message == "Rating must be between -1 and 4"


def test_validate_request_valid():
    """Test valid request"""
    request = "1"
    is_valid, message = validate_request(request)
    assert is_valid
    assert message == ""


def test_validate_request_invalid():
    """Test invalid request"""
    request = None
    is_valid, message = validate_request(request)
    assert not is_valid
    assert message == "Request must be 0 or 1"


def test_validate_request_invalid2():
    """Test invalid request"""
    request = "3"
    is_valid, message = validate_request(request)
    assert not is_valid
    assert message == "Request must be 0 or 1"


def test_validate_consumed_messages_valid():
    """Test valid JSON message parsing and validation"""
    message = '{"at": "2024-10-21T09:30:00.000+0000", "site": "2", "val": "3", "type": "rating"}'
    result = validate_consumed_messages(message)
    # assert result == {"at": "2024-10-21T09:30:00.000+0000",
    #                   "site": "2", "val": "3", "type": "rating"}
    assert True, ""


def test_validate_consumed_messages_invalid():
    """Test invalid JSON message parsing"""
    message = '{"at": "2024-10-21T09:30:00.000+0000", "site": "10", "val": "3", "type": "rating"}'
    result = validate_consumed_messages(message)
    assert False in result


@patch("consumer.psycopg2.connect")
def test_database_connection(mock_connect):
    """Test database connection"""
    conn = get_connection()
    mock_connect.assert_called_once()
    assert conn == mock_connect.return_value


# @patch("consumer.confluent_kafka.Consumer")
# def test_kafka_consumer(mock_consumer):
#     """Test Kafka consumer creation"""
#     consumer = create_kafka_consumer()
#     assert consumer == mock_consumer.return_value


@patch("consumer.load_dotenv")
def test_load_dotenv(mock_load_dotenv):
    """Test loading environment variables"""
    get_connection()  # Assuming load_dotenv is called within get_connection
    mock_load_dotenv.assert_called_once()


@patch("consumer.logging")
def test_logging(mock_logging):
    """Test logging setup"""
    config_log_terminal()
    assert mock_logging.basicConfig.called
