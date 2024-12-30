<div align="center" dir="auto">
<pre>
███████╗ ██████╗ ██╗      █████╗ ███╗   ███╗ ██████╗ 
██╔════╝██╔═══██╗██║     ██╔══██╗████╗ ████║██╔═══██╗
███████╗██║   ██║██║     ███████║██╔████╔██║██║   ██║
╚════██║██║▄▄ ██║██║     ██╔══██║██║╚██╔╝██║██║▄▄ ██║
███████║╚██████╔╝███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══▀▀═╝ 
-------------------------------------------------------
                 SQLAlchemy database connector and multifunction query                 
</pre>
</div>

SQLAMQ - is a Python based application that connects to the various of supported databases by [SQLAlchemy](https://www.sqlalchemy.org/): 

- [SQLite](https://www.sqlite.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [MySQL](https://www.mysql.com/)
- [MariaDB](https://mariadb.org/)
- [MS-SQL](https://www.microsoft.com/en-ca/sql-server/sql-server-downloads)

And performs different query selection in one function depending on passed arguments:

- [Select](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)
- [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update)
- [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete)
- [Drop](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.drop)

## How to run?

Application requires [Python](https://www.python.org/downloads/) 3.9+ < [Python](https://www.python.org/) 3.13 installed on your local machine.

> Create virtual environment to install all needed dependencies:

Manually:

```python
python -m venv .venv
```

Or you can use your IDE to install it automatically as for example PyCharm does.

> Install all needed dependencies:

```python
pip install -r requirements.txt
```

> Change .env settings:

```python
DB_TYPE=DB_TYPE
DB_NAME=DB_NAME
DB_PASSWORD=DB_PASSWORD
DB_TABLE_NAME=DB_TABLE_NAME
DB_HOST=DB_HOST
DB_PORT=DB_PORT
```

- `DB_TYPE` - type of the database (postgresql, mysql, sqlite etc.).
- `DB_NAME` - username of the database.
- `DB_PASSWORD` - password of the database.
- `DB_TABLE_NAME` - table name of the database.
- `DB_HOST` - host of the database.
- `DB_PORT` - port of the database.

### Example of usage:

```python
engine = create_engine(sqlalchemy_url_builder(), echo=True, poolclass=NullPool)

Base.metadata.create_all(bind=engine)

multifunctional_query = DatabaseMultifunctionalQuery(
    engine=engine,
    method="select",
    selection=[User],
    params=QueryParams(
        filter=FilterParams(
            expressions=[User.id == 1]
        )
    )
)

result = multifunctional_query.query()

if isinstance(result, Iterable):
    logging.info("Printing results...")
    for i in result:
        print(i)

elif isinstance(result, bool):
    logging.info("Printing result...")
    print(result)
```

## Supported by the application databases:

- [SQLite](https://www.sqlite.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [MySQL](https://www.mysql.com/)
- [MariaDB](https://mariadb.org/) (in progress...)
- [MS-SQL](https://www.microsoft.com/en-ca/sql-server/sql-server-downloads) (in progress...)

## Supported query methods:

- Params
  - [filter](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.filter)
    - [or_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_)
    - [and_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
    - expressions
  - [exits](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists)
  - [join](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.join)
    - expressions
    - [select_from](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from)
  - [synchronize_session](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#selecting-a-synchronization-strategy)
  - [updated_values](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update.params.values)
  - [order_by](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)
    - expressions

## Example of usage of query methods:

### Filter

> [or_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) - takes a list of [or_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) expressions as an argument:

```python
...
params=QueryParams(
    filter=FilterParams(
        or_=[
            or_(User.username == "jfg4567", User.id == 5)
        ]
    )
)
```

> [and_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) - takes a list of [and_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) expressions as an argument:

```python
...
params=QueryParams(
    filter=FilterParams(
        and_=[
            and_(User.id == 3, User.created_at >= "2024-12-24 00:00:00")
        ]
    )
)
```

> expressions - takes a list of a single expression, for multiple ones [or_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) and [and_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) exist:

```python
...
params=QueryParams(
    filter=FilterParams(
        expressions=[User.id == 1]
    )
)
```

### Exists

> [exits](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists) - takes a bool value as an arguments (False or True):

```python
...
params=QueryParams(
    filter=FilterParams(
        expressions=[User.id == 1]
    ),
    exists=True
)
```

### Join

> expressions - takes a list of tuple expression (Table, statement):

> [select_from](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) - takes a list of Tables inside to choose data from:

```python
...
params=QueryParams(
    join=JoinParams(
        expressions=[
            (Post, User.id == Post.author_id)
        ],
        select_from=[User]
    )
)
```

### Synchronize Session

> [synchronize_session](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#selecting-a-synchronization-strategy) - takes either an str argument or bool, used for updating a deleting data:

```python
...
method="update",
...
params=QueryParams(
    filter=FilterParams(
        expressions=[Post.post_id == 35445]
    ),
    order_by=OrderByParams(
        expressions=[Post.post_id]
    ),
    updated_values={"post_id": 235235},
    synchronize_session="auto"
)
```

### Updated values

> [updated_values](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update.params.values) - takes a dictionary of {column: value} that needs to be updated, can accept multiple values:

```python
...
method="update",
...
params=QueryParams(
    filter=FilterParams(
        expressions=[Post.post_id == 35445]
    ),
    updated_values={"post_id": 235235},
)
```

### Order by

> [order_by](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) - takes a list of expressions:

```python
...
params=QueryParams(
    ...
    order_by=OrderByParams(
        expressions=[Post.post_id]
    )
)
```
