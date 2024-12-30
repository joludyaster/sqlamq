from datetime import datetime
from typing import List, Any, Iterable, Literal

from sqlalchemy import create_engine, Engine, or_, and_
from sqlalchemy.orm import Session

from sqlamq.config.data import sqlalchemy_url_builder, QueryParams, FilterParams, JoinParams, OrderByParams
from sqlamq.connector import setup_logging, DatabaseMultifunctionalQuery
from sqlamq.utils.sqla_api.models.models import User, Post, Base

import random
import logging


test_users = [
    User(
        username="anthony2345",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Family",
            content="My family consists of 5 people."
        )]
    ),
    User(
        username="jake56gh",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Sport",
            content="You have to get yourself involved into sport."
        )]
    ),
    User(
        username="mot6hfg3",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Health",
            content="Take care of your health."
        )]
    ),
    User(
        username="jfg4567",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Tech",
            content="You should a little knowledge about tech in 21st century."
        )]
    ),
    User(
        username="fghdf5679",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Food",
            content="What kind of food do you like?"
        )]
    ),
    User(
        username="89kgh45",
        posts=[Post(
            post_id=random.randint(10000, 99999),
            category="Love",
            content="Love will break any circumstances."
        )]
    )
]


def execute_tests():

    # Execute logging function
    setup_logging()

    # Create an engine with database link linked to it
    engine = create_engine(sqlalchemy_url_builder(), echo=True)

    # Create all models that bounded to the engine
    Base.metadata.create_all(bind=engine)

    # with Session(engine) as session:
    #     session.add_all(test_users)
    #
    #     session.commit()

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[User],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             and_=[
    #                 and_(User.id == 3, User.created_at >= "2024-12-24 00:00:00")
    #             ]
    #         )
    #     )
    # )

    # Output:
    #
    # (User(id=3, username='mot6hfg3', created_at=datetime.datetime(2024, 12, 24, 19, 5, 33), updated_at=datetime.datetime(2024, 12, 24, 19, 5, 33)),)

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[User],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             or_=[
    #                 or_(User.username == "jfg4567", User.id == 5)
    #             ]
    #         )
    #     )
    # )

    # Output:
    #
    # (User(id=4, username='jfg4567', created_at=datetime.datetime(2024, 12, 24, 19, 5, 33), updated_at=datetime.datetime(2024, 12, 24, 19, 5, 33)),)
    # (User(id=5, username='fghdf5679', created_at=datetime.datetime(2024, 12, 24, 19, 5, 33), updated_at=datetime.datetime(2024, 12, 24, 19, 5, 33)),)

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[User],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[User.id == 1]
    #         ),
    #         exists=True
    #     )
    # )

    # Output: True

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[User],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[User.id == 1]
    #         )
    #     )
    # )

    # Output: User(id=1, username='anthony2345', created_at=datetime.datetime(2024, 12, 23, 0, 0), updated_at=datetime.datetime(2024, 12, 23, 0, 0))

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[Post],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[Post.post_id <= 50000]
    #         )
    #     )
    # )

    # Output:
    #
    # Post(id=1, post_id=47456, author_id=1, category='Family', content='My family consists of 5 people.', created_at=datetime.datetime(2024, 12, 23, 0, 0))
    # Post(id=2, post_id=31765, author_id=2, category='Sport', content='You have to get yourself involved into sport.', created_at=datetime.datetime(2024, 12, 23, 0, 0))
    # Post(id=4, post_id=42258, author_id=4, category='Tech', content='You should a little knowledge about tech in 21st century.', created_at=datetime.datetime(2024, 12, 23, 0, 0))
    # Post(id=5, post_id=23080, author_id=5, category='Food', content='What kind of food do you like?', created_at=datetime.datetime(2024, 12, 23, 0, 0))

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[Post.category, Post.author_id, Post.content, User.username],
    #     params=QueryParams(
    #         join=JoinParams(
    #             expressions=[
    #                 (Post, User.id == Post.author_id)
    #             ],
    #             select_from=[User]
    #         )
    #     )
    # )

    # Output:
    #
    # ('Family', 1, 'My family consists of 5 people.', 'anthony2345')
    # ('Sport', 2, 'You have to get yourself involved into sport.', 'jake56gh')
    # ('Health', 3, 'Take care of your health.', 'mot6hfg3')
    # ('Tech', 4, 'You should a little knowledge about tech in 21st century.', 'jfg4567')
    # ('Food', 5, 'What kind of food do you like?', 'fghdf5679')
    # ('Love', 6, 'Love will break any circumstances.', '89kgh45')

    # execute_select_queries(
    #     engine=engine,
    #     method="select",
    #     selection=[Post],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[Post.post_id >= 50000]
    #         ),
    #         order_by=OrderByParams(
    #             expressions=[Post.post_id]
    #         )
    #     )
    # )

    # Output:
    #
    # (Post(id=5, post_id=33196, author_id=5, category='Food', content='What kind of food do you like?', created_at=datetime(2024, 12, 24, 19, 5, 33)),)
    # (Post(id=2, post_id=34913, author_id=2, category='Sport', content='You have to get yourself involved into sport.', created_at=datetime.datetime(2024, 12, 24, 19, 5, 33)),)

    # execute_select_queries(
    #     engine=engine,
    #     method="update",
    #     selection=[Post],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[Post.post_id == 35445]
    #         ),
    #         order_by=OrderByParams(
    #             expressions=[Post.post_id]
    #         ),
    #         updated_values={"post_id": 235235},
    #         synchronize_session="auto"
    #     )
    # )

    # Output:
    #
    # True

    # execute_select_queries(
    #     engine=engine,
    #     method="delete",
    #     selection=[User],
    #     params=QueryParams(
    #         filter=FilterParams(
    #             expressions=[User.id == 1]
    #         )
    #     )
    # )

    # Output:
    #
    # True

    # execute_select_queries(
    #     engine=engine,
    #     method="drop",
    #     selection=[Post]
    # )


def execute_select_queries(
        engine: Engine,
        method: Literal["select", "update", "delete", "drop"],
        selection: List[Any],
        params: QueryParams = None
):
    multifunctional_query = DatabaseMultifunctionalQuery(
        engine=engine,
        method=method,
        selection=selection,
        params=params
    )

    result = multifunctional_query.query()

    if isinstance(result, Iterable):
        logging.info("Printing results...")
        for i in result:
            print(i)

    elif isinstance(result, bool):
        logging.info("Printing result...")
        print(result)


if __name__ == "__main__":
    try:
        execute_tests()
    except (KeyboardInterrupt, SystemExit):
        logging.error("Program was finished.")
