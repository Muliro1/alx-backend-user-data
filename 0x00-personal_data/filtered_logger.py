#!/usr/bin/env python3
""" doc doc doc """
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Replace sensitive information in the given message.

    Replace any information that matches the following pattern:
        field=.*?;(where field is one of the given fields)
    with the given redaction.

    :param fields: a list of fields to filter
    :param redaction: the value to replace the filtered fields with
    :param message: the original message
    :param separator: the separator used in the message
    :return: the filtered message
    """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    A logging formatter that redacts sensitive information from log messages.

    Attributes:
        REDACTION (str): the value to replace filtered fields with
        FORMAT (str): the format of the log message
        SEPARATOR (str): the separator used in the log message
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the given fields to filter.

        :param fields: a list of fields to filter
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, replacing any sensitive information with
        the redaction.

        :param record: the log record to format
        :return: the formatted log message
        """
        org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, org, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Return a logger with a handler that redacts sensitive information
    from log messages.

    The logger is named "user_data" and logs messages with level
    INFO or higher. The logger does not propagate messages to its
    parent loggers.

    The handler is a StreamHandler that writes messages to
    sys.stdout. The handler uses a RedactingFormatter to format the
    messages, which replaces sensitive information with a redaction.

    :return: a logger with a handler that redacts sensitive information
    """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(sh)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Return a connection to the database.

    The connection is made with the following parameters:
        - user: PERSONAL_DATA_DB_USERNAME (default: root)
        - password: PERSONAL_DATA_DB_PASSWORD (default: "")
        - host: PERSONAL_DATA_DB_HOST (default: localhost)
        - database: PERSONAL_DATA_DB_NAME

    :return: the connection to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )


def main() -> None:
    """Main function.

    Connect to the database and log the contents of the users table.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    log = get_logger()
    for row in cursor:
        data = []
        for desc, value in zip(cursor.description, row):
            pair = f"{desc[0]}={str(value)}"
            data.append(pair)
        row_str = "; ".join(data)
        log.info(row_str)

    # Close the cursor and database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
