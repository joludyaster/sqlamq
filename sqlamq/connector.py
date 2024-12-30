import logging
import random

import betterlogging

from sqlalchemy import create_engine, Engine, or_, and_, exists, Table, Select, select, update, delete, NullPool, text
from sqlalchemy.exc import CompileError, SQLAlchemyError
from sqlalchemy.orm import Session, DeclarativeBase, close_all_sessions

from sqlamq.utils.sqla_api.models.models import User, Base, Post
from typing import Any, Literal, Iterable, List

from sqlamq.config.data import sqlalchemy_url_builder, QueryParams


def setup_logging() -> None:
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    :return: None
    """

    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Program started!")


class DatabaseMultifunctionalQuery:
    def __init__(
            self,
            engine: Engine,
            method: Literal["select", "update", "delete", "drop"],
            selection: List[Any],
            params: QueryParams = None
    ):
        self.engine = engine
        self.method = method
        self.selection = selection
        self.params = params

    def query(self) -> bool | Iterable[Any]:

        # Check if the method is valid
        if self.method not in ["select", "update", "delete", "drop"]:
            logging.error("Invalid method. Please use 'select', 'update', or 'delete'.")
            return False

        # Ensure that the parameters for the query are provided
        if not self.params or (not self.params.filter and not self.params.join):
            if self.method == "drop":
                logging.info("Performing tables deletion...")
                return self.__query_drop()

            logging.error("No parameters for database query were provided.")
            return False

        if not self.selection:
            logging.error("No tables or models selected for querying data.")
            return False

        stmt = select(*self.selection)
        synchronize_session = self.params.synchronize_session

        # Apply filters if provided
        if self.params.filter:
            filters = self.params.filter
            if filters.or_:
                stmt = stmt.filter(or_(*filters.or_))
            if filters.and_:
                stmt = stmt.filter(and_(*filters.and_))
            if filters.expressions:
                stmt = stmt.filter(*filters.expressions)

        # Apply join expressions if provided
        if self.params.join and self.params.join.expressions:
            if self.params.join.select_from:
                stmt.select_from(*self.params.join.select_from)
            for join_args in self.params.join.expressions:
                if isinstance(join_args, tuple):
                    stmt = stmt.join(*join_args)
                else:
                    logging.error("Each join entry must be a tuple (selection, condition).")
                    return False

        # Apply order by expressions if provided
        if self.params.order_by and self.params.order_by.expressions:
            stmt = stmt.order_by(*self.params.order_by.expressions)

        # Call the appropriate query method based on the selected method
        if self.method == "select":
            logging.info("Performing selection...")
            return self.__query_select(stmt=stmt)

        elif self.method == "update":
            logging.info("Performing values update...")
            return self.__query_update(stmt=stmt, synchronize_session=synchronize_session)

        else:
            logging.info("Performing columns deletion...")
            return self.__query_delete(stmt=stmt, synchronize_session=synchronize_session)

    def __query_select(self, stmt: Select) -> bool | Iterable[Any]:
        """
        Function to select a row or a singular column from a database.

        :param stmt: The base Select statement with filters applied.
        :return: True if parameter .exists() was passed otherwise a list of rows or columns.
        """

        try:
            with Session(self.engine) as session:

                # Select all the results based on the provided filters
                if self.params.exists:
                    status = session.scalar(exists().where(stmt.whereclause).select())
                    return status
                else:
                    results = session.execute(stmt).all()
                    return results

        except CompileError as error:
            logging.error(f"An error occurred during query execution. Details: {error}")
            return False
        except Exception as exception:
            logging.error(f"Unexpected error occurred. Details: {exception}")
            return False

    def __query_update(self, stmt: Select, synchronize_session) -> bool:
        """
        Update rows in the database based on the given statement and updated values.

        :param stmt: The base Select statement with filters applied.
        :param synchronize_session: Strategy for synchronizing the session ('fetch', 'evaluate', False, 'auto').

        :return: bool: True if rows were updated, False otherwise.
        """

        try:
            # Validate that selection is not empty
            if not self.selection:
                logging.error("No tables or models selected for update.")
                return False

            updated_values = self.params.updated_values
            if not updated_values:
                logging.error("No values provided for updating columns.")
                return False

            # Create an update statement
            update_stmt = update(*self.selection).where(stmt.whereclause).values(updated_values)

            with Session(self.engine) as session:
                # Execute update statement with session synchronization
                result = session.execute(update_stmt.execution_options(synchronize_session=synchronize_session))

                # Commit changes
                session.commit()

                # Log results
                if result.rowcount >= 1:
                    logging.info(f"{result.rowcount} rows were updated successfully.")
                    return True
                else:
                    logging.info("No rows were updated. Check the provided filters and values.")
                    return False

        except CompileError as error:
            logging.error(f"SQL compilation error: {error}")
            return False
        except SQLAlchemyError as sqle:
            logging.error(f"SQLAlchemy error occurred: {sqle}")
            return False
        except Exception as exception:
            logging.error(f"Unexpected error: {exception}")
            return False

    def __query_delete(self, stmt: Select, synchronize_session) -> bool:
        """
        Deletes rows from the database based on the given statement.

        :param: stmt: The base Select statement with filters applied.
        :param: synchronize_session: Strategy for synchronizing the session ('fetch', 'evaluate', 'false', 'auto').

        :return: bool: True if rows were deleted, False otherwise.
        """

        try:
            if not self.selection:
                logging.error("No tables or models selected for deletion.")
                return False

            total_deleted = 0

            for model in self.selection:
                if issubclass(model, DeclarativeBase):
                    # Handle ORM models
                    rows_deleted = self.__delete_orm_model(model, stmt)
                    total_deleted += rows_deleted

                elif isinstance(model, Table):
                    # Handle raw SQL tables
                    rows_deleted = self.__delete_sql_table(model, stmt, synchronize_session)
                    total_deleted += rows_deleted

                # Final log
                if total_deleted > 0:
                    logging.info(f"Total of {total_deleted} rows were deleted.")
                    return True
                else:
                    logging.info("No rows were deleted. Check your filters or selection.")
                    return False

        except CompileError as error:
            logging.error(f"SQL compilation error occurred: {error}")
            return False
        except SQLAlchemyError as sqle:
            logging.error(f"SQLAlchemy error occurred: {sqle}")
            return False
        except Exception as exception:
            logging.error(f"Unexpected error: {exception}")
            return False

    def __delete_orm_model(self, model: Any, stmt: Select) -> int:
        """
        Deletes rows from an ORM model using filters from the given statement.
        """
        try:
            with Session(self.engine) as session:
                objects = session.query(model).filter(stmt.whereclause).all()
                if objects:
                    for obj in objects:
                        session.delete(obj)
                    session.commit()
                    logging.info(f"Deleted {len(objects)} rows from {model.__name__}.")
                    return len(objects)
                else:
                    logging.info(f"No rows matched the filter for model {model.__name__}.")
                    return 0
        except Exception as e:
            logging.error(f"Error deleting ORM model {model.__name__}: {e}")
            return 0

    def __delete_sql_table(self, table: Table, stmt: Select, synchronize_session: str | bool) -> int:
        """
        Deletes rows from a raw SQL table using filters from the given statement.
        """
        try:
            with Session(self.engine) as session:
                delete_stmt = delete(table).where(stmt.whereclause)
                result = session.execute(delete_stmt.execution_options(synchronize_session=synchronize_session))
                session.commit()
                if result.rowcount > 0:
                    logging.info(f"Deleted {result.rowcount} rows from {table.name}.")
                    return result.rowcount
                else:
                    logging.info(f"No rows matched the filter for table {table.name}.")
                    return 0
        except Exception as e:
            logging.error(f"Error deleting rows from table {table.name}: {e}")
            return 0

    def __query_drop(self):
        """
        Function to delete singular table or multiple tables

        :return: True if some of the tables were deleted, otherwise False
        """

        try:
            total = 0

            if len(self.selection) > 0:
                for table in self.selection:
                    try:
                        if hasattr(table, "__table__"):
                            logging.info(f"Attempting to delete table -> {table.__tablename__}")
                            table.__table__.drop(self.engine, checkfirst=True)  # Ensures table exists before dropping
                            total += 1
                        else:
                            logging.warning(f"Skipping invalid selection -> {table}")
                            continue
                    except Exception as e:
                        logging.error(f"Error while dropping table {table.__tablename__}: {e}")
                        continue

            logging.info(f"{total}/{len(self.selection)} of tables were deleted.")
            close_all_sessions()
            return True

        except CompileError as error:
            logging.error(f"SQL compilation error occurred. Details: {error}")
            return False
        except Exception as exception:
            logging.error(f"An unexpected error occurred. Details: {exception}")
            return False


def main() -> None:

    """
    Main executing file.

    :return: None
    """

    # Execute logging function
    setup_logging()

    # Create an engine with database link linked to it
    engine = create_engine(sqlalchemy_url_builder(), echo=True, poolclass=NullPool)

    # Create all models that bounded to the engine
    Base.metadata.create_all(bind=engine)

    # Example of creating a table:
    #
    # with Session(engine) as session:
    #     spongebob = User(
    #         username="anthony2345",
    #         posts=[Post(
    #             post_id=random.randint(10000, 99999),
    #             category="Family",
    #             content="My family consists of 5 people."
    #         )]
    #     ),
    #     session.add_all([spongebob])
    #
    #     session.commit()

    # Your sql selection, update or deletion...
    #
    # See example in tests.py


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error("Program was finished.")
