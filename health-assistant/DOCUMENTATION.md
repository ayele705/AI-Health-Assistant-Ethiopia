AI-Based Health Assistant for Rural Ethiopia
Full Project Documentation

Prepared by: Health Assistant Development Team
Version: 1.0
Date: May 2026


TABLE OF CONTENTS

1. Project Overview
2. System Architecture
3. Technology Stack
4. Project Structure
5. Backend Setup and Installation
6. Frontend Setup and Installation
7. Environment Configuration
8. API Reference
9. Core Modules
10. Database Models
11. Multilingual Support
12. SMS and Notifications
13. Validation System
14. Running the Application
15. Deployment Notes


1. PROJECT OVERVIEW

The AI-Based Health Assistant is a web and mobile application designed to improve healthcare access for rural communities in Ethiopia. The system provides intelligent symptom assessment, health education, appointment scheduling, medication reminders, pregnancy follow-up, child growth monitoring, and emergency alerts through a conversational interface.

The system is built to work in low-bandwidth environments and supports four languages: English, Amharic, Oromo (Afaan Oromoo), and Tigrinya. It is designed for use by rural community members, Health Extension Workers (HEWs), and Community Health Volunteers (CHVs).

Key capabilities of the system include the following. The symptom checker allows users to describe their symptoms and receive a preliminary health assessment with urgency classification. The health education module provides tips and information on common diseases, nutrition, maternal health, and child care. The appointment booking feature allows patients to schedule visits at nearby health facilities. The growth monitoring module tracks child weight, height, and MUAC measurements and classifies nutritional status. The pregnancy follow-up module manages antenatal care schedules and flags danger signs. The medication reminder system sends daily SMS reminders to patients on chronic medications. The emergency alert system notifies registered contacts when a user reports a danger sign. The chronic disease management module supports hypertension and diabetes follow-up with blood pressure and glucose tracking. The mental health screening module uses PHQ-2 and GAD-2 tools to screen for depression and anxiety. The USSD interface allows feature phone users to access the system without a smartphone. The traditional medicine module provides information on Ethiopian traditional remedies and flags interactions with modern medications. The supply chain module helps HEWs report stock shortages at health posts. The referral tracker allows CHWs to create and follow up on patient referrals. The analytics dashboard provides consultation statistics, outbreak alerts, and DHIS2 export.


2. SYSTEM ARCHITECTURE

The system follows a three-tier client-server architecture.

The presentation tier consists of a React.js web application that serves as the main user interface. It communicates with the backend through a REST API. The application supports voice input through the Web Speech API and falls back to a server-side speech-to-text proxy for browsers that do not support it natively.

The application tier is a Django REST Framework backend that hosts all business logic. It includes the AI symptom engine, the NLP chatbot, the SMS engine, the scheduler for reminders, and all API endpoints. The backend runs on Python 3 and uses SQLite as the database in development.

The data tier uses SQLite for development and can be configured to use PostgreSQL for production. A translation cache database stores pre-built translations to reduce API calls.

The integration layer connects to Africa's Talking for SMS delivery, Google Places API for real-time facility search, Google Cloud Translation API for multilingual support, DHIS2 for national health data reporting, and ElevenLabs or Google TTS for voice output.


3. TECHNOLOGY STACK

Backend Technologies:
- Python 3.10 or higher
- Django 4.2.7 (web framework)
- Django REST Framework 3.14.0 (API layer)
- APScheduler 3.10.4 (background task scheduling for reminders)
- Africa's Talking SDK 1.2.7 (SMS gateway)
- SpeechRecognition 3.10.4 (server-side speech to text)
- Google Cloud Translate 3.15.3 (translation service)
- python-dotenv 1.0.0 (environment variable management)
- django-cors-headers 4.3.1 (cross-origin resource sharing)

Frontend Technologies:
- React 18.2.0 (user interface framework)
- React Leaflet 4.2.1 with Leaflet 1.9.4 (interactive maps for facility finder)
- TensorFlow.js 4.22.0 (client-side ML capabilities)
- react-scripts 5.0.1 (Create React App build tooling)

Database:
- SQLite (development, included with Python)
- PostgreSQL (recommended for production)

External Services:
- Africa's Talking (SMS delivery)
- Google Places API (nearby facility search)
- Google Cloud Translation API (multilingual translation)
- DHIS2 (national health information system integration)
- ElevenLabs (high-quality text-to-speech, optional)


4. PROJECT STRUCTURE

The project is organized as follows:

health-assistant/
    backend/
        api/                        API views, models, validators, and URL routing
            migrations/             Database migration files
            models.py               All Django database models
            views.py                Main API endpoint handlers
            validators.py           Input validation functions
            urls.py                 URL routing for all endpoints
            emergency_views.py      Emergency contact and alert endpoints
            chronic_disease_views.py  Hypertension and diabetes endpoints
            feedback_views.py       User feedback and rating endpoints
            referral_views.py       Patient referral tracking endpoints
            mental_health_views.py  PHQ-2 and GAD-2 screening endpoints
            nutrition_views.py      Nutrition assessment endpoints
            calendar_views.py       Community health calendar endpoints
            ussd_views.py           USSD interface endpoints
            translation_views.py    Translation API endpoints
            language_views.py       Language detection endpoints
            supply_chain_views.py   Stock shortage reporting endpoints
            trad_medicine_views.py  Traditional medicine endpoints
            accessibility_views.py  Accessibility settings endpoints
        core/                       Core AI and business logic engines
            chatbot.py              Conversational symptom assessment chatbot
            symptom_engine.py       Symptom-to-condition matching engine
            knowledge_base.py       Disease knowledge base loader
            pregnancy_engine.py     ANC schedule and danger sign detection
            growth_engine.py        Child growth and nutrition assessment
            chronic_disease_engine.py  BP and glucose assessment
            mental_health_engine.py PHQ-2 and GAD-2 screening logic
            emergency_engine.py     Emergency alert sending logic
            sms_engine.py           SMS message templates and sending
            sms_chat.py             Inbound SMS conversation handler
            reminder_scheduler.py   Background scheduler for reminders
            localization.py         Multilingual string management
            translation_service.py  Google Translate integration
            geolocation.py          Nearest facility finder
            places_engine.py        Google Places API integration
            safety.py               Safety thresholds and disclaimers
            consent.py              Informed consent scripts
            nutrition_engine.py     Nutrition guidance engine
            medication_engine.py    Medication search and lookup
            analytics_engine.py     Dashboard statistics
            outbreak_detector.py    Disease spike detection
            dhis2_reporter.py       DHIS2 data export and push
            supply_chain_engine.py  Stock management logic
            trad_medicine_engine.py Traditional remedy lookup
            hew_checklists.py       HEW home visit checklists
            vaccine_schedule.py     Child vaccination schedule
            ussd_engine.py          USSD state machine
        config/
            settings.py             Django project settings
            urls.py                 Root URL configuration
        data/                       Knowledge base JSON files and translation cache
        scripts/                    Utility scripts for data loading
        manage.py                   Django management command entry point
        requirements.txt            Python dependencies
        .env                        Environment variables (not committed to git)
        .env.example                Template for environment variables
    frontend/
        src/                        React source code
        public/                     Static assets
        package.json                Node.js dependencies and scripts
        build/                      Production build output


5. BACKEND SETUP AND INSTALLATION

Step 1: Ensure Python 3.10 or higher is installed on your system. You can verify this by running "python --version" in your terminal.

Step 2: Navigate to the backend directory.
    cd health-assistant/backend

Step 3: Create a virtual environment to isolate project dependencies.
    python -m venv venv

Step 4: Activate the virtual environment.
    On Windows:   venv\Scripts\activate
    On Mac/Linux: source venv/bin/activate

Step 5: Install all required Python packages.
    pip install -r requirements.txt

Step 6: Copy the environment variables template and fill in your values.
    copy .env.example .env

Step 7: Run database migrations to create all tables.
    python manage.py migrate

Step 8: Load the initial knowledge base data if available.
    python manage.py loaddata data/knowledge_base.json

Step 9: Start the development server.
    python manage.py runserver

The backend will be available at http://127.0.0.1:8000


6. FRONTEND SETUP AND INSTALLATION

Before starting, you must fix the PowerShell execution policy on Windows. Open PowerShell and run the following command once:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then proceed with the following steps.

Step 1: Ensure Node.js version 16 or higher is installed. Download from https://nodejs.org

Step 2: Navigate to the frontend directory.
    cd health-assistant/frontend

Step 3: Install all Node.js dependencies.
    npm install

Step 4: Start the development server.
    npm start

The frontend will open automatically at http://localhost:3000 and will proxy API requests to the backend at http://localhost:8000.

To create a production build, run:
    npm run build

The optimized build files will be placed in the build/ folder.


7. ENVIRONMENT CONFIGURATION

The backend uses a .env file for all configuration. Copy .env.example to .env and set the following values:

SECRET_KEY
    A long random string used by Django for cryptographic signing. Generate one at https://djecrety.ir or use any random string generator. This must be kept secret in production.
    Example: SECRET_KEY=your-very-long-random-secret-key-here

DEBUG
    Set to True during development to see detailed error pages. Set to False in production.
    Example: DEBUG=True

ALLOWED_HOSTS
    Comma-separated list of hostnames that can access the server. Use * for development.
    Example: ALLOWED_HOSTS=*

AT_USERNAME and AT_API_KEY
    Africa's Talking credentials for SMS delivery. Register at https://africastalking.com to get a free sandbox account. Use "sandbox" as the username for testing.
    Example: AT_USERNAME=sandbox
    Example: AT_API_KEY=your-api-key-here

SMS_ENABLED
    Set to True to send real SMS messages. Set to False to simulate SMS (messages are logged but not sent). Keep False during development to avoid charges.
    Example: SMS_ENABLED=False

SCHEDULER_ENABLED
    Set to True to enable the background scheduler that sends daily medication reminders and appointment reminders. Set to False to disable.
    Example: SCHEDULER_ENABLED=True

GOOGLE_PLACES_API_KEY
    Optional. Used for real-time nearby health facility search. Get a free key from Google Cloud Console by enabling the Places API. Free tier allows 28,500 requests per month. If not set, the system falls back to the built-in knowledge base.
    Example: GOOGLE_PLACES_API_KEY=AIzaSy...

GOOGLE_TRANSLATE_API_KEY
    Optional. Used for translating content into Amharic, Oromo, and Tigrinya. Get a key from Google Cloud Console by enabling the Cloud Translation API. Free tier allows 500,000 characters per month. If not set, the system uses hardcoded translations.
    Example: GOOGLE_TRANSLATE_API_KEY=AIzaSy...

DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD, DHIS2_ORG_UNIT, DHIS2_DATASET_UID
    Credentials for pushing data to Ethiopia's national DHIS2 health information system. The default values point to the DHIS2 demo server for testing.

ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID
    Optional. Used for high-quality text-to-speech. If not set, the system falls back to Google Translate TTS.


8. API REFERENCE

All API endpoints are prefixed with /api/v1/

Symptom Assessment Endpoints:

POST /api/v1/chat/start/
    Start a new symptom assessment conversation.
    Request body: { "language": "en" }
    Response: { "session_id": "...", "message": "...", "language": "en" }

POST /api/v1/chat/message/{session_id}/
    Send a message in an ongoing conversation.
    Request body: { "message": "I have a headache" }
    Response: { "message": "...", "done": false }

POST /api/v1/quick-assess/
    Direct symptom assessment without conversation.
    Request body: { "symptoms": ["fever", "cough"], "age": 25, "sex": "female", "language": "am" }
    Response: { "conditions": [...], "urgency": "visit_health_center", "message": "..." }

POST /api/v1/differential-diagnosis/
    Enhanced diagnosis with confidence scores and treatment information.
    Request body: { "symptoms": [...], "age": int, "sex": str, "language": str }

Appointment Endpoints:

POST /api/v1/appointments/book/
    Book an appointment at a health facility.
    Required fields: patient_name, facility_id, facility_name, appointment_date (YYYY-MM-DD)
    Optional fields: patient_phone, appointment_time, reason, urgency_level, language

GET /api/v1/appointments/
    List appointments. Query parameter: facility_id

Facility Finder Endpoints:

GET /api/v1/facilities/nearest/?lat={lat}&lon={lon}
    Find nearest health facilities to GPS coordinates.
    Optional parameters: radius_km, facility_type, limit

GET /api/v1/facilities/nearby-live/?lat={lat}&lon={lon}
    Real-time facility search using Google Places API.
    Optional parameters: radius_m, facility_type

Child Health Endpoints:

POST /api/v1/chw/children/register/
    Register a new child for growth monitoring.
    Required fields: date_of_birth
    Optional fields: name, sex, mother_name, kebele, region, phone

POST /api/v1/chw/children/{child_id}/growth/
    Add a growth measurement for a child.
    Optional fields: weight_kg, height_cm, muac_cm, oedema, date_measured

GET /api/v1/chw/children/{child_id}/growth/history/
    Get growth history for a child.

GET /api/v1/chw/children/{child_id}/vaccines/
    Get vaccination schedule and status.

POST /api/v1/chw/children/{child_id}/vaccines/record/
    Record a vaccine given to a child.

Pregnancy Endpoints:

POST /api/v1/chw/pregnancy/register/
    Register a new pregnancy.
    Required fields: lmp_date (YYYY-MM-DD, last menstrual period)
    Optional fields: mother_name, age, phone, kebele, region, gravida, parity

GET /api/v1/chw/pregnancy/{record_id}/schedule/
    Get ANC schedule and status.

POST /api/v1/chw/pregnancy/{record_id}/anc-visit/
    Record an ANC visit.
    Optional fields: bp_systolic, bp_diastolic, weight_kg, visit_date, danger_signs

Chronic Disease Endpoints:

POST /api/v1/chronic/patients/register/
    Register a chronic disease patient.
    Required fields: condition (hypertension or diabetes)

POST /api/v1/chronic/patients/{patient_id}/readings/
    Add a BP or glucose reading.
    Required fields: reading_type (bp or glucose)
    For BP: systolic, diastolic
    For glucose: glucose_mgdl, fasting

POST /api/v1/chronic/bp-assess/
    Assess a blood pressure reading.
    Request body: { "systolic": 140, "diastolic": 90, "language": "am" }

POST /api/v1/chronic/glucose-assess/
    Assess a blood glucose reading.
    Request body: { "glucose_mgdl": 180, "fasting": true, "language": "am" }

SMS Endpoints:

POST /api/v1/sms/inbound/
    Receive inbound SMS from Africa's Talking webhook.

POST /api/v1/sms/send/
    Manually send an SMS.
    Request body: { "phone": "+251912345678", "message": "...", "sms_type": "manual" }

POST /api/v1/reminders/subscribe/
    Subscribe a patient to daily medication reminders.
    Required fields: patient_name, phone, medication_name

Emergency Endpoints:

POST /api/v1/emergency/contacts/
    Register an emergency contact (maximum 5 per user).
    Required fields: user_identifier, name, phone

POST /api/v1/emergency/alert/
    Send emergency SMS to all registered contacts.
    Required fields: user_identifier, condition_summary

Mental Health Endpoints:

GET /api/v1/mental-health/questions/?language=am
    Get PHQ-2 and GAD-2 screening questions.

POST /api/v1/mental-health/screen/
    Submit screening scores and get interpretation.
    Request body: { "phq2_scores": [1, 2], "gad2_scores": [0, 1], "language": "am" }

Analytics Endpoints:

GET /api/v1/analytics/dashboard/?days=30
    Full analytics dashboard with all statistics.

GET /api/v1/analytics/outbreak-alerts/?region=Oromia
    Run outbreak detection and return active alerts.

GET /api/v1/dhis2/export/?period=202401&org_unit=ImspTQPwCqd
    Export data in DHIS2 format.

Translation Endpoints:

POST /api/v1/translate/
    Translate text to a target language.
    Request body: { "text": "Hello", "target_lang": "am" }

GET /api/v1/translate/languages/
    List all supported languages.

Utility Endpoints:

GET /api/v1/tts/?lang=am&text=ሰላም
    Text-to-speech audio proxy. Returns MP3 audio.

POST /api/v1/stt/
    Server-side speech-to-text. POST audio file with lang parameter.

GET /api/v1/safe-response/?language=am
    Get the standard safe uncertainty message in the requested language.

GET /api/v1/health-tips/?category=nutrition&language=am
    Get health education tips.

GET /api/v1/medications/search/?q=amoxicillin&language=am
    Search medications by name or condition.


9. CORE MODULES

Symptom Engine (core/symptom_engine.py)

The symptom engine matches user-reported symptoms against a knowledge base of conditions. It uses a scoring algorithm that counts symptom overlaps between the reported symptoms and each condition's symptom list. The engine returns the top three matching conditions with confidence scores, urgency classification, and localized messages. Urgency levels are: emergency, visit_health_center, and self_care.

The engine also includes an Amharic symptom dictionary that maps common Amharic symptom words to their English equivalents, allowing users to type symptoms in Amharic.

Chatbot (core/chatbot.py)

The chatbot manages a multi-turn conversation to collect symptom information from users. It asks a series of questions in the user's chosen language: the main symptom, duration, additional symptoms, age, and sex. Once all information is collected, it calls the symptom engine to generate an assessment. The chatbot maintains session state in memory using a dictionary keyed by session ID.

Pregnancy Engine (core/pregnancy_engine.py)

The pregnancy engine calculates gestational age from the last menstrual period (LMP) using Naegele's rule (EDD = LMP + 280 days). It generates an 8-visit ANC schedule based on WHO guidelines and Ethiopia's FMOH protocols, showing which visits are completed, overdue, or upcoming. It also checks blood pressure readings for hypertensive disorders of pregnancy and returns danger sign lists in all four supported languages.

Growth Engine (core/growth_engine.py)

The growth engine assesses child nutritional status using weight-for-age, height-for-age, and MUAC (mid-upper arm circumference) measurements. It classifies children as having Severe Acute Malnutrition (SAM), Moderate Acute Malnutrition (MAM), or normal nutritional status. The engine uses WHO growth standards as reference.

Chronic Disease Engine (core/chronic_disease_engine.py)

The chronic disease engine classifies blood pressure readings into five stages: normal, elevated, stage 1 hypertension, stage 2 hypertension, and hypertensive crisis. It classifies blood glucose readings as hypoglycemia, normal, or hyperglycemia based on whether the reading is fasting or post-meal. Each classification returns a localized message, danger signs list, and urgency flag.

SMS Engine (core/sms_engine.py)

The SMS engine handles all outbound SMS communication through Africa's Talking. It includes message templates for appointment reminders, vaccine reminders, ANC reminders, medication reminders, and danger sign alerts. All templates are available in English, Amharic, Oromo, and Tigrinya. The engine falls back to simulation mode (logging only) when SMS_ENABLED is False.

Reminder Scheduler (core/reminder_scheduler.py)

The reminder scheduler uses APScheduler to run background jobs. It checks daily for active medication reminder subscriptions and sends SMS reminders at the appropriate time of day (morning, afternoon, or evening). It also checks for upcoming appointments and sends reminders 24 hours in advance.

Localization (core/localization.py)

The localization module provides hardcoded multilingual strings for the four supported languages. It includes IVR menu prompts, safe uncertainty messages, and symptom pictograms. All strings are available offline without requiring an API call.

Translation Service (core/translation_service.py)

The translation service provides a hybrid translation strategy. It first checks an in-memory cache, then a SQLite cache database, and finally calls the Google Cloud Translation API if a key is configured. Translations are cached after the first API call to minimize costs. The service supports batch translation for efficiency.


10. DATABASE MODELS

The following models are defined in api/models.py:

Consultation stores symptom assessment sessions with session ID, symptoms list, assessment result, urgency level, age, sex, and language.

HealthFacility stores health facility information including name, type, region, woreda, phone, and GPS coordinates.

Appointment stores patient appointments with patient name, phone, facility details, date, time, reason, urgency level, and status (pending, confirmed, or cancelled).

Child stores registered children for growth monitoring with child ID, name, date of birth, sex, mother name, kebele, region, and phone.

GrowthRecord stores individual growth measurements for a child including date, age in months, weight, height, MUAC, oedema status, and nutritional status classification.

VaccinationRecord stores vaccination events for a child including vaccine ID, name, date given, dose number, facility, and next due date.

PregnancyRecord stores pregnancy follow-up records with mother name, age, phone, LMP date, EDD, gravida, parity, status, and risk factors.

ANCVisit stores individual antenatal care visits with visit number, date, gestational age, weight, blood pressure, fundal height, fetal heart rate, and danger signs.

HEWChecklist stores completed HEW home visit checklists with visit type, HEW name, kebele, household ID, visit date, checklist data, and referral information.

MedicationReminder stores medication reminder subscriptions with patient name, phone, medication name, condition, time of day, language, start date, and end date.

SMSLog stores all sent and received SMS messages with direction, phone, message content, status, and type.

EmergencyContact stores emergency contacts registered by users with user identifier, name, phone, and relationship.

EmergencyAlertLog stores emergency alerts sent with user identifier, condition summary, urgency level, contacts notified, and location.

CalendarEvent stores community health calendar events with kebele, event type, date, and multilingual titles.

Referral stores patient referrals created by CHWs with patient details, CHW identifier, destination facility, reason, referral date, expected visit date, and status.

ChronicDiseaseRecord stores chronic disease patient registrations with patient identifier, name, phone, condition (hypertension or diabetes), kebele, and medication.

ChronicDiseaseReading stores individual BP or glucose readings with reading type, date, values, stage or status classification, and urgency flag.

MentalHealthScreening stores PHQ-2 and GAD-2 screening results with scores, totals, positive or negative results, and referral status.

FeedbackRating stores user feedback with session ID, rating (1 to 5), helpful flag, comment, language, and feature used.

StockShortageReport stores HEW stock shortage reports with kebele, HEW name, report data, urgent flag, and resolved status.


11. MULTILINGUAL SUPPORT

The system supports four languages: English (en), Amharic (am), Oromo (om), and Tigrinya (ti).

Language selection happens at the start of each session. The selected language is stored in the session and used for all subsequent messages, assessments, and SMS notifications.

All API endpoints accept a "language" parameter. The validators.py module validates that only the four supported language codes are accepted and returns an error for any other value.

The localization.py module provides hardcoded translations for all system messages, IVR menus, and safe uncertainty messages. These are always available offline.

The translation_service.py module provides dynamic translation through Google Cloud Translation API for content that is not hardcoded. Translations are cached in a SQLite database to minimize API usage and costs.

The Amharic symptom dictionary in symptom_engine.py maps common Amharic symptom words to English equivalents, allowing users to type symptoms in Amharic and receive accurate assessments.

All SMS message templates in sms_engine.py are available in all four languages. The system automatically selects the correct template based on the patient's registered language preference.


12. SMS AND NOTIFICATIONS

The SMS system uses Africa's Talking as the gateway provider. To set up SMS:

1. Register at https://africastalking.com and create a free sandbox account.
2. Copy your API key and username to the .env file.
3. Set SMS_ENABLED=True to send real messages, or keep it False for simulation.

In simulation mode, all SMS messages are logged to the console and to the SMSLog database table but are not actually sent. This is useful for development and testing.

The system sends the following types of SMS messages:

Appointment reminders are sent 24 hours before a scheduled appointment. They include the patient name, facility name, and appointment date.

Vaccine reminders are sent when a child's next vaccine is due. They include the child name, vaccine name, and due date.

ANC reminders are sent when an antenatal care visit is due. They include the mother name, visit label, and due date along with a reminder about danger signs.

Medication reminders are sent daily at the patient's preferred time (morning, afternoon, or evening). They include the patient name, medication name, and time of day.

Danger sign alerts are sent immediately when a user reports a danger sign. They include the patient name, the reported sign, and instructions to go to hospital immediately.

Emergency alerts are sent to all registered emergency contacts when a user triggers an emergency. They include the condition summary, location, and nearest facility information.

Inbound SMS from patients is handled by the sms_chat.py module, which parses the message and generates an appropriate response using the symptom engine.


13. VALIDATION SYSTEM

The validators.py module provides comprehensive input validation for all API endpoints. All validation functions raise a ValidationError exception on failure. The @validate_request decorator on each view function catches these exceptions and returns a structured HTTP 400 response automatically.

The following validation functions are available:

sanitize_text validates that a required text field is not empty, escapes HTML entities to prevent XSS attacks, and enforces a maximum length.

sanitize_optional_text is the same as sanitize_text but returns a default value instead of raising an error when the input is empty.

validate_language checks that the language code is one of the four supported values: en, am, om, or ti.

validate_age checks that age is an integer between 0 and 120.

validate_sex checks that sex is one of: male, female, or unknown.

validate_phone validates Ethiopian phone numbers in the formats +251XXXXXXXXX, 0XXXXXXXXX, or 9XXXXXXXX and normalizes them to the +251 prefix format.

validate_date_string parses a date string in YYYY-MM-DD format and optionally checks whether the date is in the past or future.

validate_symptoms checks that the symptoms field is a non-empty list of non-empty strings and sanitizes each symptom.

validate_weight checks that weight is between 0.3 and 500 kilograms.

validate_height checks that height is between 20 and 250 centimeters.

validate_muac checks that MUAC is between 5 and 50 centimeters.

validate_blood_pressure checks that systolic is between 50 and 300 mmHg, diastolic is between 30 and 200 mmHg, and that diastolic is lower than systolic.

validate_glucose checks that blood glucose is between 10 and 1000 mg/dL.

validate_coordinates checks that latitude is between -90 and 90 and longitude is between -180 and 180.

validate_urgency checks that urgency level is one of: emergency, urgent, routine, self_care, or unknown.

validate_condition checks that chronic disease condition is one of: hypertension or diabetes.

validate_visit_type checks that HEW checklist visit type is one of: newborn, sick_child, postnatal, antenatal, family_planning, or nutrition.

validate_rating checks that a feedback rating is an integer between 1 and 5.


14. RUNNING THE APPLICATION

To run the complete application, you need to start both the backend and the frontend.

Starting the Backend:

Open a terminal and navigate to the backend directory:
    cd health-assistant/backend

Activate the virtual environment:
    On Windows: venv\Scripts\activate
    On Mac/Linux: source venv/bin/activate

Start the Django development server:
    python manage.py runserver

The backend API will be available at http://127.0.0.1:8000

Starting the Frontend:

Open a second terminal and navigate to the frontend directory:
    cd health-assistant/frontend

If you are on Windows and get a script execution error, first run:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then install dependencies (only needed once):
    npm install

Start the React development server:
    npm start

The frontend will open automatically at http://localhost:3000

The frontend is configured to proxy all /api/ requests to the backend at http://localhost:8000, so both servers must be running at the same time.

Checking the Backend is Running:

Open a browser and go to http://127.0.0.1:8000/api/v1/safe-response/?language=am

You should see a JSON response with an Amharic message confirming the server is working.


15. DEPLOYMENT NOTES

For production deployment, the following changes are required:

Set DEBUG=False in the .env file to disable detailed error pages.

Set a strong, unique SECRET_KEY value. Never use the development key in production.

Set ALLOWED_HOSTS to your actual domain name, for example: ALLOWED_HOSTS=yourdomain.com

Switch from SQLite to PostgreSQL for better performance and reliability. Install psycopg2 and update the DATABASES setting in config/settings.py.

Set SMS_ENABLED=True and provide real Africa's Talking credentials to enable actual SMS delivery.

Configure a production web server such as Nginx or Apache to serve the Django application through Gunicorn or uWSGI.

Build the React frontend for production using "npm run build" and serve the build/ folder through Nginx.

Set up HTTPS using a free SSL certificate from Let's Encrypt.

Configure regular database backups.

Set SCHEDULER_ENABLED=True to enable daily medication and appointment reminders.

For DHIS2 integration, update the DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD, DHIS2_ORG_UNIT, and DHIS2_DATASET_UID values to point to the actual Ethiopia national DHIS2 instance.


END OF DOCUMENTATION
