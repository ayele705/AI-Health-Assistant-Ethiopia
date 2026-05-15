"""
Reminder scheduler using APScheduler.
Runs daily jobs to send SMS reminders for:
- Upcoming appointments (24h before)
- Overdue/due-soon vaccines
- Upcoming ANC visits
- Daily medication reminders
"""
import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)

_scheduler = None


def get_scheduler():
    global _scheduler
    if _scheduler is None:
        from apscheduler.schedulers.background import BackgroundScheduler
        _scheduler = BackgroundScheduler(timezone='Africa/Addis_Ababa')
    return _scheduler


def start_scheduler():
    """Start the background scheduler. Called from Django AppConfig.ready()."""
    from django.conf import settings
    if not getattr(settings, 'SCHEDULER_ENABLED', True):
        logger.info("Reminder scheduler disabled.")
        return
    scheduler = get_scheduler()
    if scheduler.running:
        return
    # Daily jobs
    scheduler.add_job(send_appointment_reminders, 'cron', hour=8, minute=0,
                      id='appointment_reminders', replace_existing=True)
    scheduler.add_job(send_vaccine_reminders,     'cron', hour=8, minute=15,
                      id='vaccine_reminders',     replace_existing=True)
    scheduler.add_job(send_anc_reminders,         'cron', hour=8, minute=30,
                      id='anc_reminders',         replace_existing=True)
    scheduler.add_job(send_medication_reminders,  'cron', hour=7, minute=0,
                      id='medication_reminders_morning', replace_existing=True)
    scheduler.add_job(send_medication_reminders,  'cron', hour=13, minute=0,
                      id='medication_reminders_noon',    replace_existing=True,
                      kwargs={'time_of_day': 'afternoon'})
    scheduler.add_job(send_medication_reminders,  'cron', hour=20, minute=0,
                      id='medication_reminders_evening', replace_existing=True,
                      kwargs={'time_of_day': 'evening'})
    scheduler.start()
    logger.info("Reminder scheduler started.")


def stop_scheduler():
    scheduler = get_scheduler()
    if scheduler.running:
        scheduler.shutdown(wait=False)


# ── Job functions ─────────────────────────────────────────────────────────────

def send_appointment_reminders():
    """Send SMS reminders for appointments due tomorrow."""
    try:
        from api.models import Appointment
        from core.sms_engine import send_sms, appointment_reminder_msg
        tomorrow = date.today() + timedelta(days=1)
        appts = Appointment.objects.filter(appointment_date=tomorrow, status='pending', patient_phone__gt='')
        count = 0
        for appt in appts:
            msg = appointment_reminder_msg(appt.patient_name, appt.facility_name,
                                           str(appt.appointment_date), appt.language)
            result = send_sms(appt.patient_phone, msg)
            logger.info(f"Appointment reminder → {appt.patient_phone}: {result['status']}")
            count += 1
        logger.info(f"Sent {count} appointment reminders.")
    except Exception as e:
        logger.error(f"Appointment reminder job failed: {e}")


def send_vaccine_reminders():
    """Send SMS reminders for vaccines due in the next 7 days."""
    try:
        from api.models import Child
        from core.vaccine_schedule import get_vaccine_schedule
        from core.sms_engine import send_sms, vaccine_reminder_msg
        today = date.today()
        in_7 = today + timedelta(days=7)
        count = 0
        for child in Child.objects.filter(phone__gt=''):
            given_ids = list(child.vaccinations.values_list('vaccine_id', flat=True))
            sched = get_vaccine_schedule(child.date_of_birth, given_ids)
            for due in sched.get('due_soon', []):
                due_date = due['due_date']
                msg = vaccine_reminder_msg(child.name, due['name'], due_date)
                result = send_sms(child.phone, msg)
                logger.info(f"Vaccine reminder → {child.phone}: {result['status']}")
                count += 1
        logger.info(f"Sent {count} vaccine reminders.")
    except Exception as e:
        logger.error(f"Vaccine reminder job failed: {e}")


def send_anc_reminders():
    """Send SMS reminders for ANC visits due in the next 14 days."""
    try:
        from api.models import PregnancyRecord
        from core.pregnancy_engine import get_anc_schedule
        from core.sms_engine import send_sms, anc_reminder_msg
        today = date.today()
        count = 0
        for preg in PregnancyRecord.objects.filter(status='active', phone__gt=''):
            completed = preg.anc_visits.count()
            sched = get_anc_schedule(preg.lmp_date, completed)
            nv = sched.get('next_visit')
            if nv and nv['days_until'] is not None and 0 <= nv['days_until'] <= 14:
                msg = anc_reminder_msg(preg.mother_name, nv['label_en'], nv['due_date'])
                result = send_sms(preg.phone, msg)
                logger.info(f"ANC reminder → {preg.phone}: {result['status']}")
                count += 1
        logger.info(f"Sent {count} ANC reminders.")
    except Exception as e:
        logger.error(f"ANC reminder job failed: {e}")


def send_medication_reminders(time_of_day: str = 'morning'):
    """Send daily medication reminders to enrolled patients."""
    try:
        from api.models import MedicationReminder
        from core.sms_engine import send_sms, medication_reminder_msg
        today = date.today()
        reminders = MedicationReminder.objects.filter(
            active=True,
            time_of_day=time_of_day,
            phone__gt='',
            start_date__lte=today,
        ).filter(end_date__isnull=True) | MedicationReminder.objects.filter(
            active=True,
            time_of_day=time_of_day,
            phone__gt='',
            start_date__lte=today,
            end_date__gte=today,
        )
        count = 0
        for r in reminders.distinct():
            msg = medication_reminder_msg(r.patient_name, r.medication_name, time_of_day, r.language)
            result = send_sms(r.phone, msg)
            logger.info(f"Med reminder → {r.phone}: {result['status']}")
            count += 1
        logger.info(f"Sent {count} medication reminders ({time_of_day}).")
    except Exception as e:
        logger.error(f"Medication reminder job failed: {e}")
