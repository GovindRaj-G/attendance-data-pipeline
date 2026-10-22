import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Define paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "attendance.csv"
TRANSFORM_SQL_FILE = PROJECT_DIR / "transform.sql"

# 2. Read the source file
print("Step 1: Reading CSV source file...")
df = pd.read_csv(CSV_FILE)

# 3. Check required columns
required_columns = [
    "employee_id",
    "employee_name",
    "company_name",
    "attendance_date",
    "attendance_status",
]
missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

# 4. Clean strings and validate mandatory fields
for column in ["employee_id", "employee_name", "company_name"]:
    df[column] = df[column].astype("string").str.strip()

if df[["employee_id", "employee_name", "company_name"]].isna().any().any():
    raise ValueError("Required fields contain missing values")

if df[["employee_id", "employee_name", "company_name"]].eq("").any().any():
    raise ValueError("Required fields contain blank values")

# 5. Connect to MySQL using environment variables
user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASSWORD", "root")
host = os.environ.get("DB_HOST", "localhost")
database = "attendance_db"

connection_url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_url)

# 6. Task 1: Ingest raw records
print("Step 2: Ingesting data into raw_attendance...")
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE raw_attendance"))
    df.to_sql(
        "raw_attendance",
        con=connection,
        if_exists="append",
        index=False,
    )
print(f"-> Ingested {len(df)} rows into raw_attendance.")

# 7. Task 2: Execute SQL transformation automatically
print("Step 3: Running SQL transformation logic...")
with open(TRANSFORM_SQL_FILE, "r") as f:
    sql_script = f.read()

# Split statements by semicolon and run each
statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

with engine.begin() as connection:
    for stmt in statements:
        # Skip pure comments or USE statements if any
        if stmt.upper().startswith("USE "):
            continue
        connection.execute(text(stmt))

print("-> Transformation executed successfully.")

# 8. Task 3: Data Quality Check & Verification
print("Step 4: Running automated data quality checks...")
with engine.connect() as connection:
    raw_cnt = connection.execute(text("SELECT COUNT(*) FROM raw_attendance")).scalar()
    clean_cnt = connection.execute(text("SELECT COUNT(*) FROM clean_attendance")).scalar()

print(f"-> Verification: {raw_cnt} raw rows loaded, {clean_cnt} clean rows produced.")
print("\nPipeline finished successfully from start to finish!")