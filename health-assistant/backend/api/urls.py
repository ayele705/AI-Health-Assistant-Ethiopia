from django.urls import path
from . import views
from . import accessibility_views as av
from . import language_views as lv
from . import ussd_views
from . import calendar_views
from . import referral_views
from . import trad_medicine_views
from . import emergency_views
from . import translation_views as tv
from . import mental_health_views as mhv
from . import nutrition_views as nv
from . import chronic_disease_views as cdv
from . import supply_chain_views as scv
from . import feedback_views as fv

urlpatterns = [
    # Core chat & assessment
    path('chat/start/', views.chat_start, name='chat-start'),
    path('chat/<str:session_id>/message/', views.chat_message, name='chat-message'),
    path('assess/', views.quick_assess, name='quick-assess'),
    path('safe-response/', views.safe_response, name='safe-response'),

    # Knowledge base
    path('tips/', views.health_tips, name='health-tips'),
    path('facilities/', views.facilities, name='facilities'),
    path('conditions/', views.conditions_list, name='conditions'),

    # Consultations & appointments
    path('consultations/', views.consultations_list, name='consultations'),
    path('appointments/', views.appointments_list, name='appointments-list'),
    path('appointments/book/', views.book_appointment, name='book-appointment'),

    # Phase 1 — Medication lookup
    path('medications/', views.medication_search, name='medication-search'),
    path('medications/<str:med_id>/', views.medication_detail, name='medication-detail'),

    # Phase 1 — Nearest facility finder
    path('facilities/nearest/', views.nearest_facilities, name='nearest-facilities'),
    path('facilities/live/', views.nearby_facilities_live, name='nearby-facilities-live'),

    # Phase 1 — Enhanced differential diagnosis
    path('differential/', views.differential_diagnosis, name='differential-diagnosis'),

    # Phase 2 — Growth monitoring
    path('children/register/', views.child_register, name='child-register'),
    path('children/<str:child_id>/growth/', views.child_growth_history, name='child-growth-history'),
    path('children/<str:child_id>/growth/add/', views.growth_record_add, name='growth-record-add'),
    path('growth/assess/', views.growth_assess, name='growth-assess'),

    # Phase 2 — Vaccination tracker
    path('children/<str:child_id>/vaccines/', views.vaccine_schedule_view, name='vaccine-schedule'),
    path('children/<str:child_id>/vaccines/add/', views.vaccine_record_add, name='vaccine-record-add'),

    # Phase 2 — Pregnancy follow-up
    path('pregnancy/register/', views.pregnancy_register, name='pregnancy-register'),
    path('pregnancy/<str:record_id>/schedule/', views.pregnancy_schedule, name='pregnancy-schedule'),
    path('pregnancy/<str:record_id>/anc/add/', views.anc_visit_add, name='anc-visit-add'),

    # Phase 2 — HEW checklists
    path('hew/checklists/', views.hew_checklist_types, name='hew-checklist-types'),
    path('hew/checklists/<str:visit_type>/', views.hew_checklist_get, name='hew-checklist-get'),
    path('hew/checklists/submit/', views.hew_checklist_submit, name='hew-checklist-submit'),

    # Phase 3 — SMS inbound webhook & manual send
    path('sms/inbound/', views.sms_inbound, name='sms-inbound'),
    path('sms/send/', views.sms_send, name='sms-send'),
    path('sms/logs/', views.sms_log_list, name='sms-logs'),

    # Phase 3 — Medication reminders
    path('reminders/', views.reminder_list, name='reminder-list'),
    path('reminders/subscribe/', views.reminder_subscribe, name='reminder-subscribe'),
    path('reminders/<int:reminder_id>/unsubscribe/', views.reminder_unsubscribe, name='reminder-unsubscribe'),

    # Phase 3 — Manual trigger & danger alerts
    path('appointments/<int:appt_id>/remind/', views.send_appointment_reminder_now, name='appt-remind'),
    path('sms/danger-alert/', views.send_danger_alert, name='danger-alert'),

    # Phase 4 — Analytics dashboard
    path('analytics/', views.analytics_dashboard, name='analytics-dashboard'),
    path('analytics/consultations/', views.analytics_consultations, name='analytics-consultations'),
    path('analytics/growth/', views.analytics_growth, name='analytics-growth'),
    path('analytics/vaccinations/', views.analytics_vaccinations, name='analytics-vaccinations'),
    path('analytics/pregnancies/', views.analytics_pregnancies, name='analytics-pregnancies'),

    # Phase 4 — Outbreak detection
    path('outbreak/alerts/', views.outbreak_alerts, name='outbreak-alerts'),
    path('outbreak/trend/<str:condition_id>/', views.disease_trend, name='disease-trend'),

    # Phase 4 — DHIS2 reporting
    path('dhis2/export/', views.dhis2_export, name='dhis2-export'),
    path('dhis2/push/', views.dhis2_push, name='dhis2-push'),

    # Consent
    path('accessibility/consent/', av.consent_script, name='consent-script'),
    path('accessibility/consent/submit/', av.consent_submit, name='consent-submit'),
    path('accessibility/consent/<str:session_id>/withdraw/', av.consent_withdraw, name='consent-withdraw'),

    # Accessibility session tracking
    path('accessibility/session/start/', av.accessibility_session_start, name='a11y-session-start'),
    path('accessibility/session/<str:session_id>/complete/', av.accessibility_session_complete, name='a11y-session-complete'),

    # Feedback
    path('accessibility/feedback/', av.submit_feedback, name='a11y-feedback'),

    # IVR & SMS channels
    path('channels/ivr/', av.ivr_inbound, name='ivr-inbound'),
    path('channels/sms/', av.sms_inbound, name='sms-inbound'),

    # CHV registry
    path('accessibility/chv/', av.chv_lookup, name='chv-lookup'),
    path('accessibility/chv/register/', av.chv_register, name='chv-register'),

    # Partner registry
    path('accessibility/partners/', av.partner_list, name='partner-list'),
    path('accessibility/partners/register/', av.partner_register, name='partner-register'),

    # Pilot & field testing
    path('pilot/cohorts/', av.pilot_cohorts, name='pilot-cohorts'),
    path('pilot/checklist/', av.field_checklist_submit, name='field-checklist'),

    # Dashboard KPIs
    path('accessibility/kpis/', av.accessibility_kpis, name='a11y-kpis'),
    path('accessibility/kpis/export/', av.accessibility_kpis_csv, name='a11y-kpis-csv'),

    # Localization
    path('accessibility/ivr-menu/', av.ivr_menu_text, name='ivr-menu'),
    path('accessibility/languages/', av.supported_languages, name='supported-languages'),

    # Rural Community Enhancements — Language Packs
    path('language-packs/', lv.language_pack_list, name='language-pack-list'),
    path('language-packs/<str:lang>/bundle/', lv.language_pack_bundle, name='language-pack-bundle'),

    # Rural Community Enhancements — USSD/IVR
    path('ussd/', ussd_views.ussd_webhook, name='ussd-webhook'),
    path('ivr/', ussd_views.ivr_webhook, name='ivr-webhook'),
    path('ussd/sessions/', ussd_views.ussd_session_list, name='ussd-sessions'),

    # Rural Community Enhancements — Community Calendar
    path('calendar/', calendar_views.calendar_list, name='calendar-list'),
    path('calendar/create/', calendar_views.calendar_create, name='calendar-create'),
    path('calendar/<int:event_id>/', calendar_views.calendar_update, name='calendar-update'),
    path('calendar/<int:event_id>/remind/', calendar_views.calendar_remind, name='calendar-remind'),

    # Rural Community Enhancements — Referral Tracker
    path('referrals/', referral_views.referral_list, name='referral-list'),
    path('referrals/create/', referral_views.referral_create, name='referral-create'),
    path('referrals/<str:referral_id>/outcome/', referral_views.referral_outcome, name='referral-outcome'),
    path('referrals/report/', referral_views.referral_report, name='referral-report'),

    # Rural Community Enhancements — Traditional Medicine
    path('trad-medicine/', trad_medicine_views.trad_medicine_search, name='trad-medicine-search'),
    path('trad-medicine/check-interactions/', trad_medicine_views.check_interactions, name='trad-medicine-interactions'),
    path('trad-medicine/<str:remedy_id>/', trad_medicine_views.trad_medicine_detail, name='trad-medicine-detail'),

    # Rural Community Enhancements — Emergency Contacts & Alerts
    path('emergency-contacts/', emergency_views.contact_list, name='emergency-contact-list'),
    path('emergency-contacts/create/', emergency_views.contact_create, name='emergency-contact-create'),
    path('emergency-contacts/<int:contact_id>/', emergency_views.contact_delete, name='emergency-contact-delete'),
    path('emergency-alert/send/', emergency_views.send_alert, name='emergency-alert-send'),
    # TTS proxy
    path('tts/', views.tts_proxy, name='tts-proxy'),
    # STT proxy (server-side fallback for browsers without Web Speech API)
    path('stt/', views.stt_proxy, name='stt-proxy'),

    # ── Translation (hybrid: cache + Google Translate API) ────────────────────
    path('translate/', tv.translate_text, name='translate'),
    path('translate/languages/', tv.supported_translation_languages, name='translate-languages'),
    path('translate/cache/', tv.translation_cache_stats, name='translate-cache-stats'),
    path('translate/cache/clear/', tv.translation_cache_clear, name='translate-cache-clear'),

    # ── Phase 5: Mental Health Screening ──────────────────────────────────────
    path('mental-health/questions/', mhv.mental_health_questions, name='mh-questions'),
    path('mental-health/screen/', mhv.mental_health_screen, name='mh-screen'),
    path('mental-health/crisis/', mhv.mental_health_crisis, name='mh-crisis'),

    # ── Phase 5: Nutrition Counseling ─────────────────────────────────────────
    path('nutrition/iycf/', nv.iycf_guidance, name='iycf-guidance'),
    path('nutrition/micronutrients/', nv.micronutrient_guidance_view, name='micronutrient-guidance'),
    path('nutrition/therapeutic/', nv.therapeutic_feeding_view, name='therapeutic-feeding'),
    path('nutrition/assess/', nv.nutrition_risk_assess, name='nutrition-assess'),

    # ── Phase 5: Chronic Disease Management ───────────────────────────────────
    path('chronic/bp/', cdv.bp_assess, name='bp-assess'),
    path('chronic/glucose/', cdv.glucose_assess, name='glucose-assess'),
    path('chronic/reminder/', cdv.adherence_reminder_view, name='adherence-reminder'),
    path('chronic/checklist/', cdv.chronic_disease_checklist_view, name='chronic-checklist'),
    path('chronic/patients/', cdv.chronic_patient_list, name='chronic-patient-list'),
    path('chronic/patients/register/', cdv.chronic_patient_register, name='chronic-patient-register'),
    path('chronic/patients/<str:patient_id>/readings/', cdv.chronic_readings_list, name='chronic-readings'),
    path('chronic/patients/<str:patient_id>/readings/add/', cdv.chronic_reading_add, name='chronic-reading-add'),

    # ── Phase 5: Supply Chain / Stock Tracking ────────────────────────────────
    path('supply/list/', scv.supply_list, name='supply-list'),
    path('supply/report/', scv.stock_report, name='stock-report'),
    path('supply/check/', scv.stock_level_check, name='stock-level-check'),
    path('supply/reports/', scv.shortage_report_list, name='shortage-report-list'),

    # ── Phase 5: Feedback & Ratings ───────────────────────────────────────────
    path('feedback/', fv.submit_feedback_rating, name='feedback-submit'),
    path('feedback/stats/', fv.feedback_stats, name='feedback-stats'),
]
