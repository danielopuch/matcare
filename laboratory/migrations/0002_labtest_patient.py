from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
        ('laboratory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_tests', to='patients.patient'),
        ),
        migrations.AddField(
            model_name='labtest',
            name='specimen_collection_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='specimen_type',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='uds',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='uds_substances',
            field=models.CharField(blank=True, max_length=200, default=''),
            preserve_default=False,
        ),
        # Add all the remaining fields from the model
        migrations.AddField(
            model_name='labtest',
            name='urine_creatinine',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='urine_ph',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='bac',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='lft_alt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='lft_ast',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='lft_alp',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='lft_bilirubin',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='hep_c_ab',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='hep_c_rna',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='hep_b_surface',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='hiv_ab',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='hiv_viral_load',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='cbc_hb',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='cbc_hct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='cbc_wbc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='cbc_platelets',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='serum_creatinine',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='egfr',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='sodium',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='potassium',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='chloride',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='bicarbonate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='blood_glucose',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='tsh',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='labtest',
            name='pregnancy_test',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='syphilis_screen',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='tb_screen',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='buprenorphine_levels',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='methadone_levels',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='naltrexone_levels',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='test_result_status',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labtest',
            name='lab_comments',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
