from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('consent_type', models.CharField(choices=[('user', 'User'), ('caregiver', 'Caregiver')], default='user', max_length=10)),
                ('channel', models.CharField(choices=[('app', 'App'), ('sms', 'SMS'), ('ussd', 'USSD'), ('ivr', 'IVR')], default='app', max_length=10)),
                ('language', models.CharField(default='en', max_length=5)),
                ('given', models.BooleanField(default=False)),
                ('withdrawn', models.BooleanField(default=False)),
                ('caregiver_name', models.CharField(blank=True, max_length=100)),
                ('caregiver_relationship', models.CharField(blank=True, max_length=50)),
                ('caregiver_phone', models.CharField(blank=True, max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-timestamp']},
        ),
        migrations.CreateModel(
            name='AccessibilitySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, unique=True)),
                ('channel', models.CharField(default='app', max_length=10)),
                ('language', models.CharField(default='en', max_length=5)),
                ('simple_mode', models.BooleanField(default=False)),
                ('high_contrast', models.BooleanField(default=False)),
                ('large_text', models.BooleanField(default=False)),
                ('screen_reader', models.BooleanField(default=False)),
                ('voice_input', models.BooleanField(default=False)),
                ('caregiver_mode', models.BooleanField(default=False)),
                ('disability_category', models.CharField(blank=True, max_length=50)),
                ('completed', models.BooleanField(default=False)),
                ('duration_seconds', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='AccessibilityFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('channel', models.CharField(default='app', max_length=10)),
                ('language', models.CharField(default='en', max_length=5)),
                ('disability_category', models.CharField(blank=True, max_length=50)),
                ('score_q1', models.IntegerField(default=0)),
                ('score_q2', models.IntegerField(default=0)),
                ('score_q3', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('flagged', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('channel', models.CharField(default='app', max_length=10)),
                ('urgency_level', models.CharField(max_length=30)),
                ('language', models.CharField(default='en', max_length=5)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-timestamp']},
        ),
        migrations.CreateModel(
            name='CHVSupporterRegistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('woreda', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('language', models.CharField(default='am', max_length=5)),
                ('certified', models.BooleanField(default=False)),
                ('certification_date', models.DateField(blank=True, null=True)),
                ('disability_specialties', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerRegistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('partner_type', models.CharField(choices=[('ngo', 'NGO'), ('government', 'Government'), ('donor', 'Donor'), ('telecom', 'Telecom'), ('disability_org', 'Disability Organization')], max_length=20)),
                ('contact_person', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(blank=True)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('territory', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='pending', max_length=10)),
                ('api_key', models.CharField(blank=True, max_length=64)),
                ('braille_materials_distributed', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PilotCohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('facility_id', models.CharField(blank=True, max_length=50)),
                ('chv_group', models.CharField(blank=True, max_length=100)),
                ('target_sample_size', models.IntegerField(default=100)),
                ('evaluator_email', models.EmailField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldTestChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, max_length=100)),
                ('chv_name', models.CharField(blank=True, max_length=100)),
                ('cohort', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.pilotcohort')),
                ('device_compatible', models.BooleanField(default=True)),
                ('network_condition', models.CharField(default='good', max_length=20)),
                ('user_comprehension', models.CharField(default='good', max_length=20)),
                ('adverse_event', models.BooleanField(default=False)),
                ('adverse_event_notes', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
