from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('patients', '0001_initial'),
        ('laboratory', '0002_labtest_patient'),
    ]

    operations = [
        # Create a function to add the column only if it doesn't exist
        migrations.RunSQL(
            sql="""
            PRAGMA foreign_keys=off;
            BEGIN TRANSACTION;
            
            CREATE TABLE IF NOT EXISTS "laboratory_labtest_new" (
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
                "patient_id" integer NULL REFERENCES "patients_patient" ("id") DEFERRABLE INITIALLY DEFERRED,
                "name" varchar(100) NULL
            );
            
            INSERT INTO laboratory_labtest_new 
            SELECT *, NULL as patient_id, NULL as name
            FROM laboratory_labtest 
            WHERE NOT EXISTS (SELECT 1 FROM laboratory_labtest_new WHERE laboratory_labtest_new.id = laboratory_labtest.id);
            
            DROP TABLE laboratory_labtest;
            ALTER TABLE laboratory_labtest_new RENAME TO laboratory_labtest;
            
            COMMIT;
            PRAGMA foreign_keys=on;
            """,
            reverse_sql="SELECT 1;" # No-op for reverse migration
        ),
    ]
