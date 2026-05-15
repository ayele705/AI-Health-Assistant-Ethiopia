"""
Migration: Phase 5 — New task types
Adds: MentalHealthScreening, ChronicDiseaseRecord, ChronicDiseaseReading,
      StockShortageReport, FeedbackRating
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rural_enhancements'),
    ]

    operations = [
        # ── Mental Health Screening ───────────────────────────────────────────
        migrations.CreateModel(
            name='MentalHealthScreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('language', models.CharField(default='en', max_length=5)),
                ('phq2_scores', models.JSONField(default=list)),
                ('gad2_scores', models.JSONField(default=list)),
                ('phq2_total', models.IntegerField(default=0)),
                ('gad2_total', models.IntegerField(default=0)),
                ('phq2_positive', models.BooleanField(default=False)),
                ('gad2_positive', models.BooleanField(default=False)),
                ('referred', models.BooleanField(default=False)),
                ('kebele', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        # ── Chronic Disease ───────────────────────────────────────────────────
        migrations.CreateModel(
            name='ChronicDiseaseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_identifier', models.CharField(db_index=True, max_length=100)),
                ('patient_name', models.CharField(blank=True, max_length=100)),
                ('patient_phone', models.CharField(blank=True, max_length=20)),
                ('condition', models.CharField(choices=[('hypertension', 'Hypertension'), ('diabetes', 'Diabetes')], max_length=20)),
                ('kebele', models.CharField(blank=True, max_length=100)),
                ('language', models.CharField(default='en', max_length=5)),
                ('medication_name', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChronicDiseaseReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='readings', to='api.chronicdiseaserecord')),
                ('reading_type', models.CharField(choices=[('bp', 'Blood Pressure'), ('glucose', 'Blood Glucose')], max_length=10)),
                ('reading_date', models.DateField()),
                ('systolic', models.IntegerField(blank=True, null=True)),
                ('diastolic', models.IntegerField(blank=True, null=True)),
                ('glucose_mgdl', models.FloatField(blank=True, null=True)),
                ('fasting', models.BooleanField(default=True)),
                ('stage_or_status', models.CharField(blank=True, max_length=30)),
                ('urgent', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('recorded_by', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        # ── Supply Chain ──────────────────────────────────────────────────────
        migrations.CreateModel(
            name='StockShortageReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kebele', models.CharField(db_index=True, max_length=100)),
                ('hew_name', models.CharField(blank=True, max_length=100)),
                ('report_data', models.JSONField(default=dict)),
                ('urgent', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        # ── Feedback & Ratings ────────────────────────────────────────────────
        migrations.CreateModel(
            name='FeedbackRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('helpful', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('feature_used', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
