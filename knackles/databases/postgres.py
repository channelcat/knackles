import asyncpg
import logging

from ..database import FieldManager, DatabaseField, Database
from ..models import Model


class PostgresFields(FieldManager):

    class IntegerField(DatabaseField):
        def db_string(self):
            return 'integer'

    class CharField(DatabaseField):
        def db_string(self):
            return f'varchar({self.field.size})'




class PostgresDatabase(Database):
    escape_field = '"'
    escape_table = '"'

    class QueryParameters(list):
        def __init__(self):
            self.counter = 0

        def append(self, value):
            super().append(value)
            self.counter += 1
            return f'${self.counter}'

    def __init__(self, user: str, password: str, database: str='database', host: str='127.0.0.1', port: int=5432):
        self._connection = None
        self.connection_kwargs = {
            "user": user,
            "password": password,
            "database": database,
            "host": host,
            "port": port,
        }
        super().__init__()

    async def connection(self):
        if self._connection is None:
            self._connection = await asyncpg.connect(**self.connection_kwargs)
        return self._connection

    async def query(self, query, values=[]):
        logging.debug(f"{query} - {values}")
        connection = await self.connection()
        return await connection.fetch(query, *values)

    async def insert_query(self, query, values=[]):
        query = f'{query} RETURNING id;'
        return await self.query(query, values)

    # --------------------------------------------------------------- #
    # Table Functions
    # --------------------------------------------------------------- #

    async def create_table(self, model: Model):
        values = QueryParameters()
        fields = [PostgresFields.get(field) for field in model.fields]
        fields = [f"{self.escape_field}{db_field.field.name}{self.escape_field} {db_field.db_string()}" \
                  # TODO: Make defaults work?  We have no escape function and parameters don't work on insert
                  # f"{f' DEFAULT {db_field.field.default}' if db_field.field.default else ''}" \
                  f"{'' if db_field.field.null else ' NOT'} NULL" for db_field in fields]
        fields = ",".join(fields)
        query = f"CREATE TABLE {model.table.name} ({fields})"
        await self.query(query, values)
        return True

    async def drop_table(self, model: Model):
        await self.query(f"DROP TABLE {model.table.name}")
        return True
