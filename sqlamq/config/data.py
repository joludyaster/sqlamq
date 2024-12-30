from dataclasses import dataclass
from typing import Any, List, Dict, Optional
from dotenv import load_dotenv

import os

load_dotenv()


@dataclass
class FilterParams:
    or_: Optional[List[Any]] = None
    and_: Optional[List[Any]] = None
    expressions: Optional[Any] = None


@dataclass
class JoinParams:
    expressions: Optional[List[tuple]] = None
    select_from: Optional[List[Any]] = None


@dataclass
class OrderByParams:
    expressions: Optional[List[Any]] = None


@dataclass
class QueryParams:
    filter: Optional[FilterParams] = None
    exists: Optional[bool] = False
    join: Optional[JoinParams] = None
    synchronize_session: Optional[str] = False
    updated_values: Optional[Dict[str, Any]] = None
    order_by: Optional[OrderByParams] = None


def sqlalchemy_url_builder(
        db_type=os.getenv("DB_TYPE"),
        db_name=os.getenv("DB_NAME"),
        db_password=os.getenv("DB_PASSWORD"),
        db_table_name=os.getenv("DB_TABLE_NAME"),
        db_host=os.getenv("DB_HOST"),
        db_port=os.getenv("DB_PORT")
) -> bool | str:
    """
    Function to generate sqlalchemy link to connect to the database later on.

    It uses environmental variables as arguments in the function already,
    so you don't have to pass anything.

    :param db_type: Type of the database (PostgreSQL, SQLite3, Oracle, MySQL etc.).
    :param db_name: Name of the database (username to be more specific).
    :param db_password: Password of the database.
    :param db_table_name: Selection name of the database.
    :param db_host: Host of the database (localhost by default).
    :param db_port: Port of the database (5432 by default).

    :return: Sqlalchemy path/status of successful link build.
    """

    host = "localhost"
    port = 5432

    if db_type == "sqlite":
        return f"{db_type}:///./{db_table_name}.db"

    if db_type and db_name and db_password and db_table_name:
        if db_host:
            host = db_host
        if port:
            port = db_port

        if db_type == "postgresql":
            return f"{db_type}+psycopg2://{db_name}:{db_password}@{host}:{port}/{db_table_name}"

        if db_type == "mysql":
            return f"{db_type}+mysqlconnector://{db_name}:{db_password}@{host}:{port}/{db_table_name}"

    return False
