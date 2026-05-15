from django.db import models
from .accessibility_models import (  # noqa: F401 — register with Django ORM
    ConsentLog, AccessibilitySession, AccessibilityFeedback,
    EmergencyAuditLog, CHVSupporterRegistry, PartnerRegistry,
    PilotCohort, FieldTestChecklist,
)


class Consultation(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, blank=True)
    region = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=5, default='en')
    symptoms = models.JSONField(default=list)
    assessment_result = models.JSONField(null=True, blank=True)
    urgency_level = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.session_id} — {self.urgency_level}"


class HealthFacility(models.Model):
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    woreda = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.region})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=20, blank=True)
    facility_id = models.CharField(max_length=50)
    facility_name = models.CharField(max_length=200)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    urgency_level = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} @ {self.facility_name} on {self.appointment_date}"


# ── Phase 2: Community Health Worker Tools ────────────────────────────────────

class Child(models.Model):
    """Registered child for growth monitoring and vaccination tracking."""
    child_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10)  # male / female
    mother_name = models.CharField(max_length=100, blank=True)
    kebele = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (DOB: {self.date_of_birth})"


class GrowthRecord(models.Model):
    """Single growth measurement for a child."""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='growth_records')
    date_measured = models.DateField()
    age_months = models.FloatField()
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    muac_cm = models.FloatField(null=True, blank=True)   # mid-upper arm circumference
    oedema = models.BooleanField(default=False)
    nutrition_status = models.CharField(max_length=30, blank=True)  # SAM / MAM / normal
    recorded_by = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child.name} — {self.date_measured} — {self.nutrition_status}"


class VaccinationRecord(models.Model):
    """Vaccination event for a child."""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_id = models.CharField(max_length=50)   # e.g. bcg, opv_0, dpt_hepb_hib_1
    vaccine_name = models.CharField(max_length=100)
    date_given = models.DateField()
    dose_number = models.IntegerField(default=1)
    facility = models.CharField(max_length=200, blank=True)
    given_by = models.CharField(max_length=100, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child.name} — {self.vaccine_name} — {self.date_given}"


class PregnancyRecord(models.Model):
    """Pregnancy follow-up record for a woman."""
    STATUS_CHOICES = [('active', 'Active'), ('delivered', 'Delivered'), ('closed', 'Closed')]
    record_id = models.CharField(max_length=50, unique=True)
    mother_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    kebele = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    lmp_date = models.DateField()           # last menstrual period
    edd = models.DateField(null=True, blank=True)  # estimated due date
    gravida = models.IntegerField(default=1)  # number of pregnancies
    parity = models.IntegerField(default=0)   # number of deliveries
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    risk_factors = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mother_name} — EDD: {self.edd}"


class ANCVisit(models.Model):
    """Single antenatal care visit."""
    pregnancy = models.ForeignKey(PregnancyRecord, on_delete=models.CASCADE, related_name='anc_visits')
    visit_number = models.IntegerField()
    visit_date = models.DateField()
    gestational_age_weeks = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    bp_systolic = models.IntegerField(null=True, blank=True)
    bp_diastolic = models.IntegerField(null=True, blank=True)
    fundal_height_cm = models.FloatField(null=True, blank=True)
    fetal_heart_rate = models.IntegerField(null=True, blank=True)
    iron_folic_given = models.BooleanField(default=False)
    tt_vaccine_given = models.BooleanField(default=False)
    danger_signs = models.JSONField(default=list)
    facility = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pregnancy.mother_name} — ANC {self.visit_number} — {self.visit_date}"


class HEWChecklist(models.Model):
    """HEW home visit checklist submission."""
    VISIT_TYPES = [
        ('newborn', 'Newborn Care'),
        ('sick_child', 'Sick Child'),
        ('postnatal', 'Postnatal'),
        ('antenatal', 'Antenatal'),
        ('family_planning', 'Family Planning'),
        ('nutrition', 'Nutrition'),
    ]
    visit_type = models.CharField(max_length=30, choices=VISIT_TYPES)
    hew_name = models.CharField(max_length=100, blank=True)
    kebele = models.CharField(max_length=100, blank=True)
    household_id = models.CharField(max_length=50, blank=True)
    visit_date = models.DateField()
    checklist_data = models.JSONField(default=dict)  # all checklist answers
    action_taken = models.TextField(blank=True)
    referral_needed = models.BooleanField(default=False)
    referral_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visit_type} — {self.kebele} — {self.visit_date}"


# ── Phase 3: SMS & Reminders ──────────────────────────────────────────────────

class MedicationReminder(models.Model):
    """Daily SMS medication reminder subscription."""
    TIME_CHOICES = [('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')]
    patient_name   = models.CharField(max_length=100)
    phone          = models.CharField(max_length=20)
    medication_name = models.CharField(max_length=200)
    condition      = models.CharField(max_length=100, blank=True)
    time_of_day    = models.CharField(max_length=20, choices=TIME_CHOICES, default='morning')
    language       = models.CharField(max_length=5, default='en')
    start_date     = models.DateField()
    end_date       = models.DateField(null=True, blank=True)
    active         = models.BooleanField(default=True)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} — {self.medication_name} ({self.time_of_day})"


class SMSLog(models.Model):
    """Log of all sent and received SMS messages."""
    DIRECTION_CHOICES = [('outbound', 'Outbound'), ('inbound', 'Inbound')]
    STATUS_CHOICES    = [('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed'), ('simulated', 'Simulated'), ('received', 'Received')]
    direction   = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    phone       = models.CharField(max_length=20)
    message     = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    message_id  = models.CharField(max_length=100, blank=True)
    sms_type    = models.CharField(max_length=50, blank=True)  # appointment/vaccine/anc/medication/chat
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direction} → {self.phone} [{self.status}]"


# ── Rural Community Enhancements ──────────────────────────────────────────────

class EmergencyContact(models.Model):
    """Emergency contact registered by a user (up to 5 per user)."""
    user_identifier = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.relationship}) — {self.phone}"


class EmergencyAlertLog(models.Model):
    """Log of every emergency alert sent."""
    user_identifier = models.CharField(max_length=100, db_index=True)
    condition_summary = models.TextField()
    urgency_level = models.CharField(max_length=30)
    contacts_notified = models.JSONField(default=list)
    location_text = models.CharField(max_length=200, blank=True)
    nearest_facility = models.CharField(max_length=200, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert {self.user_identifier} — {self.sent_at} — cancelled={self.cancelled}"


class CalendarEvent(models.Model):
    """Community health calendar event for a kebele."""
    EVENT_TYPES = [
        ('vaccination_day', 'Vaccination Day'),
        ('chw_visit', 'CHW Visit'),
        ('anc_clinic', 'ANC Clinic'),
        ('health_education', 'Health Education Session'),
        ('other', 'Other'),
    ]
    kebele = models.CharField(max_length=100, db_index=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    event_date = models.DateField(db_index=True)
    title_en = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True)
    title_ti = models.CharField(max_length=200, blank=True)
    title_om = models.CharField(max_length=200, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_type} — {self.kebele} — {self.event_date}"


class PersonalReminder(models.Model):
    """Personal reminder for a calendar event."""
    CHANNEL_CHOICES = [('sms', 'SMS'), ('in_app', 'In-App')]
    user_identifier = models.CharField(max_length=100, db_index=True)
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE,
                                        related_name='reminders')
    phone = models.CharField(max_length=20, blank=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='sms')
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder {self.user_identifier} — {self.remind_at} — sent={self.sent}"


class Referral(models.Model):
    """Patient referral created by a CHW."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('attended', 'Attended'),
        ('not_attended', 'Not Attended'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ]
    referral_id = models.CharField(max_length=50, unique=True)
    patient_identifier = models.CharField(max_length=100, db_index=True)
    patient_name = models.CharField(max_length=100, blank=True)
    patient_phone = models.CharField(max_length=20, blank=True)
    chw_identifier = models.CharField(max_length=100, db_index=True)
    destination_facility = models.CharField(max_length=200)
    reason = models.TextField()
    referral_date = models.DateField()
    expected_visit_date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    outcome_notes = models.TextField(blank=True)
    outcome_recorded_at = models.DateTimeField(null=True, blank=True)
    sms_reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Referral {self.referral_id} — {self.patient_name} → {self.destination_facility}"


class TraditionalRemedy(models.Model):
    """Ethiopian traditional remedy entry."""
    EVIDENCE_CHOICES = [
        ('documented', 'Documented'),
        ('traditional', 'Traditional'),
        ('unverified', 'Unverified'),
    ]
    remedy_id = models.CharField(max_length=50, unique=True)
    local_names = models.JSONField(default=dict)   # {"am": "...", "om": "...", "en": "..."}
    common_use_en = models.TextField()
    common_use_am = models.TextField(blank=True)
    active_compounds = models.TextField(blank=True)
    safety_notes_en = models.TextField(blank=True)
    safety_notes_am = models.TextField(blank=True)
    known_interactions = models.JSONField(default=list)  # list of medication IDs
    serious_adverse_effect = models.BooleanField(default=False)
    evidence_level = models.CharField(max_length=20, choices=EVIDENCE_CHOICES, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.remedy_id} — {self.local_names.get('en', '')}"


class USSDSessionLog(models.Model):
    """Anonymised USSD/IVR session log."""
    session_hash = models.CharField(max_length=64, unique=True)  # SHA-256 of AT session ID
    service_code = models.CharField(max_length=20, blank=True)
    language_selected = models.CharField(max_length=5, blank=True)
    symptom_selected = models.CharField(max_length=50, blank=True)
    urgency_result = models.CharField(max_length=30, blank=True)
    sms_sent = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"USSD {self.session_hash[:8]}… — {self.language_selected} — {self.urgency_result}"


# ── Phase 5: New Task Types ───────────────────────────────────────────────────

class MentalHealthScreening(models.Model):
    """PHQ-2 / GAD-2 mental health screening record."""
    session_id   = models.CharField(max_length=100, db_index=True)
    language     = models.CharField(max_length=5, default='en')
    phq2_scores  = models.JSONField(default=list)   # [int, int]
    gad2_scores  = models.JSONField(default=list)   # [int, int]
    phq2_total   = models.IntegerField(default=0)
    gad2_total   = models.IntegerField(default=0)
    phq2_positive = models.BooleanField(default=False)
    gad2_positive = models.BooleanField(default=False)
    referred     = models.BooleanField(default=False)
    kebele       = models.CharField(max_length=100, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MH Screen {self.session_id} — PHQ2:{self.phq2_total} GAD2:{self.gad2_total}"


class ChronicDiseaseRecord(models.Model):
    """Chronic disease follow-up record (hypertension / diabetes)."""
    CONDITION_CHOICES = [('hypertension', 'Hypertension'), ('diabetes', 'Diabetes')]
    patient_identifier = models.CharField(max_length=100, db_index=True)
    patient_name       = models.CharField(max_length=100, blank=True)
    patient_phone      = models.CharField(max_length=20, blank=True)
    condition          = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    kebele             = models.CharField(max_length=100, blank=True)
    language           = models.CharField(max_length=5, default='en')
    medication_name    = models.CharField(max_length=200, blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} — {self.condition}"


class ChronicDiseaseReading(models.Model):
    """Single BP or glucose reading for a chronic disease patient."""
    READING_TYPES = [('bp', 'Blood Pressure'), ('glucose', 'Blood Glucose')]
    patient    = models.ForeignKey(ChronicDiseaseRecord, on_delete=models.CASCADE,
                                    related_name='readings')
    reading_type = models.CharField(max_length=10, choices=READING_TYPES)
    reading_date = models.DateField()
    # BP fields
    systolic   = models.IntegerField(null=True, blank=True)
    diastolic  = models.IntegerField(null=True, blank=True)
    # Glucose fields
    glucose_mgdl = models.FloatField(null=True, blank=True)
    fasting      = models.BooleanField(default=True)
    # Assessment
    stage_or_status = models.CharField(max_length=30, blank=True)
    urgent          = models.BooleanField(default=False)
    notes           = models.TextField(blank=True)
    recorded_by     = models.CharField(max_length=100, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.patient_name} — {self.reading_type} — {self.reading_date}"


class StockShortageReport(models.Model):
    """Health post stock shortage report submitted by a HEW."""
    kebele      = models.CharField(max_length=100, db_index=True)
    hew_name    = models.CharField(max_length=100, blank=True)
    report_data = models.JSONField(default=dict)
    urgent      = models.BooleanField(default=False)
    resolved    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock Report — {self.kebele} — {self.created_at.date()} — urgent={self.urgent}"


class FeedbackRating(models.Model):
    """Patient/user feedback rating on guidance quality."""
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    session_id   = models.CharField(max_length=100, db_index=True)
    rating       = models.IntegerField(choices=RATING_CHOICES)
    helpful      = models.BooleanField(default=True)
    comment      = models.TextField(blank=True)
    language     = models.CharField(max_length=5, default='en')
    feature_used = models.CharField(max_length=50, blank=True)  # chat/voice/ussd/etc.
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating}/5 — {self.feature_used} — {self.session_id[:8]}"
