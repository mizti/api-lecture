from pydantic import BaseModel

class BaseDBModel(BaseModel):
    id: int | None = None

    @classmethod
    def table_name(cls):
        raise NotImplementedError("Subclasses should implement this method so that returns DB table name.")