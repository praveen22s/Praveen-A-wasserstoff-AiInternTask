from sqlalchemy import inspect
from backend.db.db import engine

def inspect_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("📋 Tables found in the database:")
    for table in tables:
        print(f"\n🔍 Table: {table}")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")

if __name__ == "__main__":
    inspect_schema()
