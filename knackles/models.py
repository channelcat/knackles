from functools import lru_cache
from itertools import chain
from types import FunctionType
from .database import databases, Database
from .fields import Field
from .util import classproperty, camel_to_snake_case

class Table:
    def __init__(self, model_class):
        self.model_class = model_class

        # Pull Model.Meta.table
        if hasattr(model_class.Meta, 'table'):
            self.name = model_class.Meta.table
        # Auto-make table name from model.py name
        else:
            self.name = camel_to_snake_case(model_class.__name__) + 's'

    async def create(self):
        await self.model_class.database.create_table(self.model_class)
    async def drop(self):
        await self.model_class.database.drop_table(self.model_class)

class Model:
    class Meta:
        @classproperty
        def database(self) -> Database:
            return databases.default

    @classproperty
    @lru_cache()
    def table(cls):
        return Table(cls)

    @classproperty
    @lru_cache()
    def fields(cls) -> list:
        fields = []
        for name, attribute in cls.__dict__.items():
            if issubclass(type(attribute), Field):
                if attribute.name is None:
                    attribute.name = name
                attribute.model_field_name = name
                fields.append(attribute)
        return fields

    @classproperty
    @lru_cache()
    def fields_dict(cls) -> dict:
        return {field.model_field_name: field for field in cls.fields}

    @classmethod
    async def create(cls, **kwargs) -> bool:
        query = generate_insert_query(cls, row=kwargs)
        print(query)
        return query

    @classproperty
    def database(cls) -> Database:
        return cls.Meta.database

    @classmethod
    def get(cls, *args, **kwargs):
        return SelectQuery().where(*args, **kwargs).one()

    @classmethod
    def where(cls, *args, **kwargs):
        return SelectQuery().where(*args, **kwargs)


from .util import Undefined


def generate_insert_query(model: Model, fields: list = None, values: list = None, row: dict = None) -> str:
    """
    Generates an insert query from a model and a data set.  Data can either be provided as a single row using `row`,
    or multi-row using `fields` and `values`.
    :param model: Model class
    :param fields: list of field string names
    :param values: list of rows, where each row is a list of values
    :param row: dictionary whose keys are fields and values are the row values
    :return: Insert query
    """
    database:Database = model.database

    # --------------------------------------------------------------- #
    #  Detect Input
    # --------------------------------------------------------------- #

    # If a row was provided, translate field -> value dict to list of fields and list of list of values
    if row:
        fields_dict = row
        values = [list(row.values())]
        fields = list(row.keys())
    else:
        fields_dict = set(fields)

    # Convert field names from model to db
    model_fields_dict = model.fields_dict
    fields = [model_fields_dict[field].name for field in fields]

    # --------------------------------------------------------------- #
    # Defaults
    # --------------------------------------------------------------- #

    # load list of default field values for this table
    defaults = []
    for field in model.fields:
        if not field.name in fields_dict:
            default = field.default
            if not default is Undefined:
                fields.append(field.name)
                default_with_func_flag = (default, type(default) is FunctionType)
                defaults.append(default_with_func_flag)

    # --------------------------------------------------------------- #
    # Fields
    # --------------------------------------------------------------- #

    fields_string = ",".join([f"{database.escape_field}{field}{database.escape_field}" for field in fields])

    # --------------------------------------------------------------- #
    # Values
    # --------------------------------------------------------------- #

    parameters = database.QueryParameters()
    row_strings = []
    for row in values:
        value_strings = []
        for value in row:
            placeholder = parameters.append(value)
            value_strings.append(placeholder)
        for default, is_function in defaults:
            if is_function:
                default = default()
            placeholder = parameters.append(default)
            value_strings.append(placeholder)
        row_strings.append(f"({','.join(value_strings)})")
    rows_string = ",".join(row_strings)

    return f'INSERT INTO {database.escape_table}{model.table.name}{database.escape_table} ' \
           f'({fields_string}) VALUES {rows_string}'