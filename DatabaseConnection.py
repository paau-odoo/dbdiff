import sqlalchemy as db
from sqlalchemy import select, func, Table


class DatabaseConnection:
    def __init__(self, dbname: str) -> None:
        self.engine = db.create_engine(f"postgresql:///{dbname}")
        self.metadata = db.MetaData()
        self.metadata.reflect(bind=self.engine)
        self.tables = self.metadata.tables.items()
        self.table_info = self.init_info()

    def init_info(self) -> dict:
        with self.engine.connect() as conn:
            table_info = {}
            for table_name, table in self.tables:
                q = select(func.count()).select_from(table)
                ct = conn.execute(q).scalar_one()
                table_info[table_name] = {"pg_table": table, "records": ct}

        return table_info

    def get_newest_records(self, n, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)

        q = select(table).order_by(table.c.id.desc()).limit(n)

        with self.engine.connect() as conn:
            r = conn.execute(q).all()
            print(r)

    def get_ids(self, table_name) -> set:
        table = Table(table_name, self.metadata, autoload_with=self.engine)

        q = select(table.c.id)

        with self.engine.connect() as conn:
            r = conn.execute(q).scalars().all()
            return set(r)
