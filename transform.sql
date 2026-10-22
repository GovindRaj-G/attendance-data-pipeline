USE attendance_db;

TRUNCATE TABLE clean_attendance;

INSERT INTO clean_attendance (
    employee_id,
    employee_name,
    company_name,
    attendance_date,
    attendance_status
)
SELECT
    TRIM(employee_id),
    TRIM(employee_name),
    TRIM(company_name),
    attendance_date,
    UPPER(TRIM(attendance_status))
FROM raw_attendance
WHERE employee_id IS NOT NULL
  AND TRIM(employee_id) <> ''
  AND employee_name IS NOT NULL
  AND TRIM(employee_name) <> ''
  AND company_name IS NOT NULL
  AND TRIM(company_name) <> ''
  AND UPPER(TRIM(attendance_status)) IN ('PRESENT', 'ABSENT');