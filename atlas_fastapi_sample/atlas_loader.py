import sys
from sqlmodel import SQLModel

# THE MISSING PIECE: Import your actual model classes here!
# Replace 'your_app.models' with the actual path to your models file.
# This registers the models in the SQLModel metadata.
from app.models import User, Post  # <-- Adjust this import to match your project

def dump_atlas_sql():
    print("CREATE SCHEMA IF NOT EXISTS app;")

    from sqlalchemy import create_mock_engine

    def dump(sql, *multiparams, **params):
        statement = str(sql.compile(dialect=engine.dialect))
        if statement.strip():
            print(f"{statement.strip()};")

    engine = create_mock_engine("postgresql://", dump)
    
    for table in SQLModel.metadata.tables.values():
        table.schema = "app"
        
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    dump_atlas_sql()