from functools import lru_cache

class DatabaseList(list):
    @property
    def default(self):
        try:
            return self[-1]
        except:
            raise ValueError("Database not configured yet")

databases = DatabaseList()


class Database:
    def __init__(self):
        databases.append(self)

    @property
    def escape_table(self):
        raise NotImplementedError("Escape for table name not implemented")

    @property
    def escape_field(self):
        raise NotImplementedError("Escape for field name not implemented")

    class QueryParameters(list):
        def __init__(self):
            raise NotImplementedError("Query parameters not implemented")


class FieldManager:
    @classmethod
    @lru_cache(maxsize=128)
    def get(cls, field):
        field_name = field.__class__.__name__
        try:
            db_class = getattr(cls, field_name)
        except:
            raise NotImplementedError(f"{field_name} not implemented by this databases engine yet")

        return db_class(field)


class DatabaseField:
    def __init__(self, field):
        self.field = field

    def db_string(self):
        raise NotImplementedError("create_string not implemented!")
