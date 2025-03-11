# pylint: skip-file

import pytest
from unittest.mock import patch, MagicMock, mock_open
import psycopg2
from pipeline import (
    get_connection, get_cursor, insert_rating_interaction,
    insert_request_interaction, upload_to_database, config_log_file, config_log_terminal
)


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("DATABASE_USERNAME", "test_user")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_NAME", "test_db")


@patch("psycopg2.connect")
def test_get_connection(mock_connect, mock_env):
    """Test get_connection function"""
    get_connection()
    mock_connect.assert_called_once_with(
        user="test_user",
        host="localhost",
        database="test_db"
    )


@patch("psycopg2.connect")
def test_get_cursor(mock_connect, mock_env):
    """Test get_cursor function"""
    conn = get_connection()
    cursor = get_cursor(conn)
    assert cursor is not None
    assert mock_connect().cursor.called


# Mocking a CSV file and testing upload_to_database
@patch("builtins.open", new_callable=mock_open, read_data="at,site,val,type\n2024-10-01,1,3,\n2024-10-01,2,-1,0.0")
@patch("pipeline.insert_rating_interaction")
@patch("pipeline.insert_request_interaction")
def test_upload_to_database(mock_request_interaction, mock_rating_interaction, mock_open):
    """Test uploading rating and request interaction"""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()

    upload_to_database(mock_cursor, mock_conn, 'mock_csv_file.csv', 10)

    assert mock_rating_interaction.called
    assert mock_request_interaction.called


@patch("logging.basicConfig")
def test_config_log_file(mock_logging):
    """Test logging configuration for log file"""
    config_log_file()
    mock_logging.assert_called_once_with(
        filename="pipeline.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=20
    )


@patch("logging.basicConfig")
def test_config_log_terminal(mock_logging):
    """Test logging configuration for terminal"""
    config_log_terminal()
    mock_logging.assert_called_once_with(
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=20
    )
