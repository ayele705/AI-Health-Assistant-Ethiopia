"""
Accessibility, consent, pilot, and partner models.
"""
from django.db import models


class ConsentLog(models.Model):
    CONSENT_TYPE = [('user', 'User'), ('caregiver', 'Caregiver')]
    CHANNEL = [('app', 'App'), ('sms', 'SMS'), ('ussd', 'USSD'), ('ivr', 'IVR')]

    session_id = models.CharField(max_length=100, db_index=True)
    consent_type = models.CharField(max_length=10, choices=CONSENT_TYPE, default='user')
    channel = models.CharField(max_length=10, choices=CHANNEL, default='app')
    language = models.CharField(max_length=5, default='en')
    given = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    caregiver_name = models.CharField(max_length=100, blank=True)
    caregiver_relationship = models.CharField(max_length=50, blank=True)
    caregiver_phone = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Consent {self.session_id} [{self.consent_type}] given={self.given}"


class AccessibilitySession(models.Model):
    """Tracks accessibility modes used per consultation session."""
    session_id = models.CharField(max_length=100, unique=True)
    channel = models.CharField(max_length=10, default='app')
    language = models.CharField(max_length=5, default='en')
    simple_mode = models.BooleanField(default=False)
    high_contrast = models.BooleanField(default=False)
    large_text = models.BooleanField(default=False)
    screen_reader = models.BooleanField(default=False)
    voice_input = models.BooleanField(default=False)
    caregiver_mode = models.BooleanField(default=False)
    disability_category = models.CharField(max_length=50, blank=True)
    completed = models.BooleanField(default=False)
    duration_seconds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class AccessibilityFeedback(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    channel = models.CharField(max_length=10, default='app')
    language = models.CharField(max_length=5, default='en')
    disability_category = models.CharField(max_length=50, blank=True)
    score_q1 = models.IntegerField(default=0)   # ease of use 1-5
    score_q2 = models.IntegerField(default=0)   # language clarity 1-5
    score_q3 = models.IntegerField(default=0)   # overall satisfaction 1-5
    comment = models.TextField(blank=True)
    flagged = models.BooleanField(default=False)  # score avg < 3
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def average_score(self):
        return round((self.score_q1 + self.score_q2 + self.score_q3) / 3, 2)


class EmergencyAuditLog(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    channel = models.CharField(max_length=10, default='app')
    urgency_level = models.CharField(max_length=30)
    language = models.CharField(max_length=5, default='en')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class CHVSupporterRegistry(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    woreda = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    language = models.CharField(max_length=5, default='am')
    certified = models.BooleanField(default=False)
    certification_date = models.DateField(null=True, blank=True)
    disability_specialties = models.JSONField(default=list)  # e.g. ['blind', 'deaf']
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.region}) certified={self.certified}"


class PartnerRegistry(models.Model):
    PARTNER_TYPE = [
        ('ngo', 'NGO'),
        ('government', 'Government'),
        ('donor', 'Donor'),
        ('telecom', 'Telecom'),
        ('disability_org', 'Disability Organization'),
    ]
    STATUS = [('active', 'Active'), ('pending', 'Pending'), ('inactive', 'Inactive')]

    name = models.CharField(max_length=200)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    territory = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    api_key = models.CharField(max_length=64, blank=True)
    braille_materials_distributed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} [{self.partner_type}]"


class PilotCohort(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    facility_id = models.CharField(max_length=50, blank=True)
    chv_group = models.CharField(max_length=100, blank=True)
    target_sample_size = models.IntegerField(default=100)
    evaluator_email = models.EmailField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cohort: {self.name} (target={self.target_sample_size})"


class FieldTestChecklist(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    chv_name = models.CharField(max_length=100, blank=True)
    cohort = models.ForeignKey(PilotCohort, null=True, blank=True, on_delete=models.SET_NULL)
    device_compatible = models.BooleanField(default=True)
    network_condition = models.CharField(max_length=20, default='good')  # good/poor/offline
    user_comprehension = models.CharField(max_length=20, default='good')  # good/partial/poor
    adverse_event = models.BooleanField(default=False)
    adverse_event_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
