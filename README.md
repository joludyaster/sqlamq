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

# How to run?

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

To be continued...
