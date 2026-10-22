# End-to-End Attendance Data Pipeline (ELT)

An automated ingestion and transformation pipeline that loads daily attendance CSV records into MySQL, validates schema and mandatory fields using Python, and applies cleaning, standardization, and business rules via SQL.

## Architecture

[CSV Source Data]
│
▼ (Python / Pandas / SQLAlchemy)
[MySQL: raw_attendance]
│
▼ (SQL Business Logic / Transformations)
[MySQL: clean_attendance]
│
▼
[Automated Quality Checks & Metrics]


## Tech Stack

- **Language:** Python
- **Libraries:** Pandas, SQLAlchemy, PyMySQL
- **Database:** MySQL
- **Tooling:** VS Code, MySQL Workbench, Git

## Project Structure

```text
attendance_pipeline/
├── data/
│   └── attendance.csv       # Source attendance data
├── src/
│   └── pipeline.py          # Unified ingestion, transformation & verification script
├── transform.sql            # SQL transformation & business validation logic
├── requirements.txt         # Project dependencies
├── .gitignore               # Environment and cache ignore rules
└── README.md                # Project documentation
Data Transformation Rules
The transformation script enforces the following quality checks:

Trimming: Strips unnecessary whitespace from employee IDs, names, and company names.

Standardization: Converts attendance statuses into standard uppercase (PRESENT, ABSENT).

Filtering: Rejects null values, empty strings, and statuses outside approved company attendance codes.

How to Run
Clone the repository:

Bash
git clone [https://github.com/GovindRaj-G/attendance-data-pipeline.git](https://github.com/GovindRaj-G/attendance-data-pipeline.git)
cd attendance-data-pipeline
Set up virtual environment:

Bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Set MySQL environment variables:

PowerShell
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_HOST="localhost"
Run the pipeline:

Bash
python src/pipeline.py

3. Click the green **Commit changes...** button at the top right, then click **Commit changes** in the pop-up modal.

Your repository will display formatted documentation on its homepage.

---

### Sync the New File to Local VS Code

To pull the `README.md` down into your local project folder in VS Code, run:

```powershell
git pull
