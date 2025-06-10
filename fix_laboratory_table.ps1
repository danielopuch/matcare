$env:PYTHONPATH = "d:\Git\matcare"
cd d:\Git\matcare

Write-Host "Creating a proper migration for the laboratory app's LabTest model..." -ForegroundColor Green

# Generate SQL for laboratory_labtest table
$sql = @"
-- Create a new table with all fields
CREATE TABLE "laboratory_labtest_new" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "specimen_collection_datetime" datetime NULL,
    "specimen_type" varchar(20) NOT NULL,
    "uds" varchar(20) NOT NULL,
    "uds_substances" varchar(200) NOT NULL,
    "urine_creatinine" real NULL,
    "urine_ph" real NULL,
    "bac" real NULL,
    "lft_alt" real NULL,
    "lft_ast" real NULL,
    "lft_alp" real NULL,
    "lft_bilirubin" real NULL,
    "hep_c_ab" varchar(20) NOT NULL,
    "hep_c_rna" varchar(100) NOT NULL,
    "hep_b_surface" varchar(20) NOT NULL,
    "hiv_ab" varchar(20) NOT NULL,
    "hiv_viral_load" varchar(100) NOT NULL,
    "cbc_hb" real NULL,
    "cbc_hct" real NULL,
    "cbc_wbc" real NULL,
    "cbc_platelets" real NULL,
    "serum_creatinine" real NULL,
    "egfr" real NULL,
    "sodium" real NULL,
    "potassium" real NULL,
    "chloride" real NULL,
    "bicarbonate" real NULL,
    "blood_glucose" real NULL,
    "tsh" real NULL,
    "pregnancy_test" varchar(20) NOT NULL,
    "syphilis_screen" varchar(20) NOT NULL,
    "tb_screen" varchar(20) NOT NULL,
    "buprenorphine_levels" varchar(100) NOT NULL,
    "methadone_levels" varchar(100) NOT NULL,
    "naltrexone_levels" varchar(100) NOT NULL,
    "test_result_status" varchar(20) NOT NULL,
    "lab_comments" text NOT NULL,
    "patient_id" integer NULL REFERENCES "patients_patient" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Copy data from old table to new table
INSERT INTO "laboratory_labtest_new" ("id", "specimen_collection_datetime", "specimen_type", "uds", "uds_substances",
                                  "urine_creatinine", "urine_ph", "bac", "lft_alt", "lft_ast", "lft_alp", "lft_bilirubin",
                                  "hep_c_ab", "hep_c_rna", "hep_b_surface", "hiv_ab", "hiv_viral_load", "cbc_hb", "cbc_hct", 
                                  "cbc_wbc", "cbc_platelets", "serum_creatinine", "egfr", "sodium", "potassium", "chloride", 
                                  "bicarbonate", "blood_glucose", "tsh", "pregnancy_test", "syphilis_screen", "tb_screen", 
                                  "buprenorphine_levels", "methadone_levels", "naltrexone_levels", "test_result_status", 
                                  "lab_comments", "patient_id")
SELECT "id", "specimen_collection_datetime", "specimen_type", "uds", "uds_substances",
       "urine_creatinine", "urine_ph", "bac", "lft_alt", "lft_ast", "lft_alp", "lft_bilirubin",
       "hep_c_ab", "hep_c_rna", "hep_b_surface", "hiv_ab", "hiv_viral_load", "cbc_hb", "cbc_hct", 
       "cbc_wbc", "cbc_platelets", "serum_creatinine", "egfr", "sodium", "potassium", "chloride", 
       "bicarbonate", "blood_glucose", "tsh", "pregnancy_test", "syphilis_screen", "tb_screen", 
       "buprenorphine_levels", "methadone_levels", "naltrexone_levels", "test_result_status", 
       "lab_comments", "patient_id"
FROM "laboratory_labtest";

-- Drop old table
DROP TABLE "laboratory_labtest";

-- Rename new table to original name
ALTER TABLE "laboratory_labtest_new" RENAME TO "laboratory_labtest";
"@

# Save SQL to a file
$sql | Out-File -FilePath "fix_laboratory_table.sql" -Encoding utf8

# Execute the SQL to fix the table
Write-Host "Executing SQL to fix the laboratory_labtest table..." -ForegroundColor Green
sqlite3 db.sqlite3 < fix_laboratory_table.sql

Write-Host "Running migrations to ensure everything is up to date..." -ForegroundColor Green
python manage.py migrate

Write-Host "Database fix completed!" -ForegroundColor Green
