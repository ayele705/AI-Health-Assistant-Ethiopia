# AI-Based Health Assistant for Rural Ethiopia
## Project Documentation

**Version:** 1.0  
**Date:** May 2026  
**Course:** AI Course - Academic Year 2026

### Group Members

| # | Name | Student ID |
|---|------|-----------|
| 1 | Ayele Moges | GUR/01091/16 |
| 2 | Birihanekulu Tafere | GUR/01115/16 |
| 3 | Amare Minayehu | GUR/22885/16 |
| 4 | Bezawit Desalegn | GUR/01199/16 |
| 5 | Tigist Markos | GUR/00475/16 |
| 6 | Yabsira Debebe | GUR/02880/16 |

---

## Table of Contents

1. Project Overview
2. Problem Statement
3. Objectives
4. System Architecture
5. Functional Requirements
6. Technology Stack
7. Module Descriptions
8. Database Design
9. API Reference
10. Knowledge Base
11. Urgency Classification
12. Known Limitations
13. Future Work
14. References

---

## 1. Project Overview

The AI-Based Health Assistant is a conversational web application designed to improve
healthcare access for rural communities in Ethiopia. It provides symptom-based health
guidance, health education, and referral recommendations through a chat interface
accessible via web browser (PWA) and via USSD on feature phones.

**Primary users:**
- Rural community members who lack access to nearby health facilities
- Health Extension Workers (HEWs) who need decision-support tools for triage and referral

The assistant supports English, Amharic, Oromo and Tigrinya, operates in low-bandwidth environments,
and includes offline functionality via service worker caching. It is not a diagnostic tool
and does not replace professional medical care.

---

## 2. Problem Statement

Ethiopia has fewer than 1 physician per 10,000 people (WHO). Approximately 80% of
the population lives in rural areas with limited access to health facilities.

| Barrier | Impact |
|---|---|
| Geographic distance | Patients travel hours on foot to reach the nearest clinic |
| Shortage of health workers | HEWs are overwhelmed and lack decision-support tools |
| Low health literacy | Delayed care-seeking for preventable conditions |
| Language diversity | 80+ languages; most digital tools only support English or Amharic |
| Poor connectivity | Unreliable internet limits cloud-based health tools |
| Weak referral system | Under-referral and over-referral both common |

No existing AI health assistant is purpose-built for the linguistic, cultural, and
infrastructural context of rural Ethiopia. This project fills that gap.

---

## 3. Objectives

### General Objective
Design and develop a functional AI health assistant prototype that improves access to
basic health information, symptom guidance, and referral support for rural Ethiopian communities.

### Specific Objectives
1. Identify primary healthcare access barriers through literature review and secondary data analysis
2. Design a system architecture optimized for low-bandwidth and offline environments
3. Develop a prototype with symptom guidance, health education, and referral modules
4. Curate a health knowledge base aligned with Ethiopia's disease burden
5. Implement multilingual support (English, Amharic, Oromo, Tigrinya)
6. Provide decision-support tools for Health Extension Workers

---

## 4. System Architecture

The system follows a three-tier client-server architecture:

```
+--------------------------------------------------+
|               Presentation Tier                    |
|              React SPA (PWA)                       |
|        USSD / IVR (Africa's Talking)              |
|        SMS Chat / Voice (Web Speech API)          |
+--------------------------+------------------------+
                           |
+--------------------------v------------------------+
|               Application Tier                     |
|   Django REST Framework (API)                      |
|   Symptom Assessment Engine (keyword-based)        |
|   Rule-based Chatbot (multi-turn interview)        |
|   Medical domain engines (growth, vaccine, etc.)   |
|   Translation Service (cache + Google API)         |
|   SMS/USSD Engine (Africa's Talking)               |
|   APScheduler (reminders)                          |
+--------------------------+------------------------+
                           |
+--------------------------v------------------------+
|                  Data Tier                          |
|   SQLite (primary database)                        |
|   JSON Knowledge Base (30+ conditions)             |
|   Translation Cache (SQLite)                       |
+--------------------------+------------------------+
                           |
+--------------------------v------------------------+
|              Integration Layer                      |
|   DHIS2 API (REST export/push)                    |
|   Africa's Talking SMS/USSD Gateway               |
|   Google Cloud Translation API                    |
|   Google Places API (facility lookup)             |
+---------------------------------------------------+
```

### Offline Architecture
The React PWA uses a service worker (`sw.js`) to cache:
- Application shell (HTML, JS, CSS)
- Knowledge base queries (Cache API)
- Recent consultation records

When connectivity is restored, the app operates normally from the server.

---

## 5. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Symptom input via text in English, Amharic, Oromo and Tigrinya | High |
| FR-02 | Structured symptom interview through conversational interface (5-step) | High |
| FR-03 | Generate ranked list of possible conditions from symptoms (keyword match) | High |
| FR-04 | Classify urgency: self-care / visit health center / emergency | High |
| FR-05 | Health education content in text format | High |
| FR-06 | Proactive health tips based on user profile and season | Medium |
| FR-07 | Nearest health facility lookup based on user location | High |
| FR-08 | Appointment scheduling at connected health facilities | Medium |
| FR-09 | First aid guidance for common emergencies | High |
| FR-10 | Emergency contact numbers for local facilities | High |
| FR-11 | HEW community health dashboard | Medium |
| FR-12 | Core features available in offline mode (PWA) | Medium |
| FR-13 | Growth monitoring for children (WHO standards) | High |
| FR-14 | Vaccination tracking (Ethiopia EPI schedule) | High |
| FR-15 | Pregnancy follow-up and ANC visit tracking | High |
| FR-16 | HEW field checklists and reporting | Medium |
| FR-17 | SMS reminders and alerts for appointments | Medium |
| FR-18 | Outbreak detection from consultation data | Low |
| FR-19 | Aggregate anonymized data and report to DHIS2 | Low |
| FR-20 | Medication information lookup | Medium |
| FR-21 | Mental health screening (PHQ-9, GAD-7) | Medium |
| FR-22 | Nutrition counseling (IYCF, micronutrients, therapeutic feeding) | Medium |
| FR-23 | Chronic disease management (BP, glucose tracking) | Medium |
| FR-24 | Supply chain / stock shortage reporting | Low |
| FR-25 | Traditional medicine lookup and herb-drug interaction checking | Low |
| FR-26 | USSD interface for feature phones | High |
| FR-27 | Feedback and rating submission | Low |

---

## 6. Technology Stack

### Backend
| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Django 4.2 + Django REST Framework |
| Database | SQLite |
| Task Scheduler | APScheduler |
| SMS/USSD | Africa's Talking SDK |

### Engine/AI Approach
| Component | Approach |
|---|---|
| Symptom Assessment | Keyword-based multilingual symptom matching with scoring |
| Chatbot | Rule-based multi-turn interview (5 steps per language) |
| Growth Monitoring | WHO standard comparison tables (hardcoded) |
| Vaccine Scheduling | Ethiopia EPI static schedule (date calculation) |
| Pregnancy Tracking | ANC visit schedule calculator |
| Outbreak Detection | Threshold-based alerting |
| Translation | Pre-built JSON cache + Google Translate API fallback |

### Frontend
| Component | Technology |
|---|---|
| Framework | React 18 |
| Maps | Leaflet / react-leaflet |
| PWA | Service worker + manifest.json |
| Voice Input | Web Speech API |
| Offline Storage | Cache API |
| State Mgmt | React context |

### USSD/IVR Interface
| Component | Technology |
|---|---|
| Language | Python (Django views) |
| Gateway | Africa's Talking USSD/IVR API |

### DevOps
| Component | Technology |
|---|---|
| Containerization | Docker, Docker Compose |

---

## 7. Module Descriptions

### 7.1 Symptom Assessment Engine
Processes user symptom input using keyword matching across multiple languages.
No machine learning models are used — the engine maps symptom keywords (English,
Amharic, Tigrinya, Oromo, Sidamo) to conditions from the knowledge base and
scores them by overlap count.

- **Method**: Multilingual symptom keyword mapping + condition scoring
- **Languages**: English, Amharic, Tigrinya, Oromo, Sidamo (input mapped to English)
- **Output**: Ranked conditions with scores, urgency level, recommendations

```python
from core.symptom_engine import assess

result = assess(
    symptoms=["fever", "headache", "fatigue"],
    age=30,
    sex="female",
    language="en"
)
# Returns: {conditions: [...], urgency_level: str, recommendations: str}
```

### 7.2 Chatbot Module
Manages a 5-step conversational symptom interview. Questions are asked
sequentially: primary symptom → duration → additional symptoms → age → sex.
At the end, the symptom engine runs and returns the assessment.

- **Languages**: English, Amharic, Tigrinya, Oromo (with scaffolding for Sidamo, Somali, Afar, Wolaytta, Hadiyya)
- **Storage**: In-memory session dictionary (prototype)
- **Output**: Assessment result with conditions, urgency, recommendations

```python
from core.chatbot import start_session, process_message

state = start_session("session-123", language="am")
response = process_message("session-123", "ራስ ምታት አለኝ")
```

### 7.3 Health Knowledge Base
A curated repository of health information stored as a JSON file covering
Ethiopia's primary disease burden.

- **Format**: JSON document (4060 lines)
- **Coverage**: 30+ common conditions including malaria, TB, diarrheal diseases,
  respiratory infections, maternal health, nutrition
- **Languages**: English, Amharic, Tigrinya, Oromo for all content
- **Sources**: WHO Primary Care Guidelines, Ethiopian Standard Treatment Guidelines,
  FMOH materials
- **Also includes**: Health facilities list, medications list, health tips

### 7.4 Growth Monitoring Engine
Assesses child growth against WHO growth standards using hardcoded z-score tables.

- **Metrics**: Weight-for-age, height-for-age, weight-for-height
- **Output**: Normal / moderate malnutrition / severe malnutrition
- **Languages**: English, Amharic, Tigrinya, Oromo

### 7.5 Vaccine Schedule Engine
Calculates due vaccines based on a child's date of birth and the Ethiopia
Expanded Program on Immunization (EPI) schedule.

- **Vaccines**: BCG, OPV, Penta, PCV, Rotavirus, IPV, Measles, MR, Td, HPV
- **Output**: List of due and upcoming vaccines with dates

### 7.6 Pregnancy & ANC Tracking
Tracks pregnancy and antenatal care visits.

- **Registration**: LMP date, expected delivery date
- **ANC Visits**: Scheduled visit timeline with due dates
- **Output**: Visit schedule, risk flags

### 7.7 HEW Checklists
Digital checklists for Health Extension Workers during household visits.

- **Types**: Child health, maternal health, sanitation, nutrition, chronic disease
- **Output**: Completed checklist with submission timestamp

### 7.8 USSD Interface
Menu-driven interface for feature phones without internet access.

- Powered by Africa's Talking USSD API
- Covers: symptom reporting (simplified), health tips, facility finder
- No smartphone or internet required

### 7.9 SMS Engine
Sends SMS reminders and alerts via Africa's Talking gateway.

- **Features**: Appointment reminders, medication reminders, danger alerts
- **Storage**: SMS log in database

### 7.10 Translation Service
Hybrid translation using a pre-built JSON cache with Google Translate API fallback.

- **Pre-built translations**: Loaded on startup into in-memory cache
- **API fallback**: Google Cloud Translation API
- **Languages**: English, Amharic, Tigrinya, Oromo, Somali, Sidamo, Afar

### 7.11 Outbreak Detector
Threshold-based disease outbreak detection from consultation data.

- **Method**: Compares recent consultation counts for a condition against a baseline
- **Alerts**: Generated when threshold exceeded
- **Output**: List of active outbreak alerts

### 7.12 DHIS2 Reporter
Exports aggregate health data to DHIS2 for national health surveillance.

- **Export**: Aggregate consultation counts by condition, region, age group
- **Push**: Sends data to DHIS2 data value sets
- **Status**: Simulated in prototype (REST scaffold in place)

### 7.13 Mental Health Screening
PHQ-9 (depression) and GAD-7 (anxiety) screening questionnaires.

- **Scoring**: Automatic score calculation with severity classification
- **Crisis detection**: Flags suicidal ideation responses

### 7.14 Nutrition Counseling
Provides guidance on IYCF (Infant and Young Child Feeding), micronutrients,
and therapeutic feeding for malnutrition.

- **IYCF**: Breastfeeding and complementary feeding guidance
- **Micronutrients**: Deficiency prevention guidance
- **Therapeutic feeding**: Management of acute malnutrition

### 7.15 Chronic Disease Management
Tracks blood pressure and blood glucose readings for chronic disease patients.

- **BP Assessment**: Classification (normal / elevated / stage 1 / stage 2 / crisis)
- **Glucose Assessment**: Classification (normal / pre-diabetic / diabetic)
- **Adherence**: Medication reminder support

### 7.16 Supply Chain / Stock Tracking
Reports and tracks stock shortages at health facilities.

- **Report**: Medicine/supply shortage with quantity and facility
- **View**: List of reported shortages

---

## 8. Database Design

The project uses SQLite as its database engine with the following models
(defined via Django ORM).

### consultations
```
session_id         VARCHAR(100) PRIMARY KEY
user_name          VARCHAR(100)
age                INTEGER
sex                VARCHAR(10)
region             VARCHAR(100)
language           VARCHAR(5)
symptoms           JSON
assessment_result  JSON
urgency_level      VARCHAR(30)
created_at         DATETIME
```

### health_facilities
```
name               VARCHAR(200)
facility_type      VARCHAR(50)
region             VARCHAR(100)
woreda             VARCHAR(100)
phone              VARCHAR(20)
latitude           FLOAT
longitude          FLOAT
```

### appointments
```
patient_name       VARCHAR(100)
patient_phone      VARCHAR(20)
facility_id        VARCHAR(50)
facility_name      VARCHAR(200)
appointment_date   DATE
appointment_time   TIME
reason             TEXT
urgency_level      VARCHAR(30)
status             VARCHAR(20)  -- pending / confirmed / cancelled
language           VARCHAR(5)
created_at         DATETIME
```

### children
```
child_id           VARCHAR(50) PRIMARY KEY
name               VARCHAR(100)
date_of_birth      DATE
sex                VARCHAR(10)
mother_name        VARCHAR(100)
kebele             VARCHAR(100)
region             VARCHAR(100)
phone              VARCHAR(20)
created_at         DATETIME
```

### growth_records
```
child              FK -> children
date               DATE
weight_kg          FLOAT
height_cm          FLOAT
muac_cm            FLOAT (optional)
```

### vaccination_records
```
child              FK -> children
vaccine_name       VARCHAR(50)
dose_number        INTEGER
date_administered  DATE
facility_name      VARCHAR(200)
```

### pregnancy_records
```
record_id          VARCHAR(50) PRIMARY KEY
mother_name        VARCHAR(100)
age                INTEGER
lmp_date           DATE
edd_date           DATE
gravida            INTEGER
para               INTEGER
region             VARCHAR(100)
phone              VARCHAR(20)
language           VARCHAR(5)
created_at         DATETIME
```

### anc_visits
```
pregnancy          FK -> pregnancy_records
visit_number       INTEGER
visit_date         DATE
gestational_week   INTEGER
bp_systolic        INTEGER
bp_diastolic       INTEGER
weight_kg          FLOAT
hemoglobin         FLOAT
fundal_height      FLOAT
complications      TEXT
```

### hew_checklists
```
visit_type         VARCHAR(50)
child_id           VARCHAR(50)
answers            JSON
submitted_at       DATETIME
```

### medication_reminders
```
patient_name       VARCHAR(100)
patient_phone      VARCHAR(20)
medication_name    VARCHAR(100)
dosage             VARCHAR(100)
time_of_day        VARCHAR(20)
language           VARCHAR(5)
active             BOOLEAN
```

### sms_logs
```
recipient          VARCHAR(20)
message            TEXT
status             VARCHAR(20)
message_type       VARCHAR(30)
sent_at            DATETIME
```

### emergency_contacts
```
name               VARCHAR(100)
phone              VARCHAR(20)
facility_name      VARCHAR(200)
region             VARCHAR(100)
```

### mental_health_screenings
```
patient_name       VARCHAR(100)
screening_type     VARCHAR(10)  -- phq9 / gad7
answers            JSON
total_score        INTEGER
severity           VARCHAR(30)
flagged            BOOLEAN
created_at         DATETIME
```

### chronic_disease_records
```
patient_id         VARCHAR(50)
patient_name       VARCHAR(100)
condition_type     VARCHAR(30)  -- hypertension / diabetes
region             VARCHAR(100)
phone              VARCHAR(20)
created_at         DATETIME
```

### chronic_disease_readings
```
patient            FK -> chronic_disease_records
reading_type       VARCHAR(20)  -- bp / glucose
reading_value      FLOAT
reading_date       DATE
notes              TEXT
```

### supply_shortage_reports
```
facility_name      VARCHAR(200)
item_name          VARCHAR(100)
quantity_needed    INTEGER
urgency            VARCHAR(20)
reported_at        DATETIME
```

### feedback_ratings
```
session_id         VARCHAR(100)
rating             INTEGER
category           VARCHAR(30)
comment            TEXT
created_at         DATETIME
```

Additional models exist for consent logging, accessibility sessions,
CHV registry, partner registry, pilot cohorts, calendar events,
referrals, traditional remedies, USSD session logs, etc.

---

## 9. API Reference

**Base URL:** `http://localhost:8000`

### Chat & Assessment
| Method | Endpoint | Description |
|---|---|---|
| POST | /chat/start/ | Start a new chat session |
| POST | /chat/{session_id}/message/ | Send message in session |
| POST | /assess/ | Quick symptom assessment (single step) |
| POST | /safe-response/ | Get disclaimered health info |

**POST /chat/start/ — Request Body**
```json
{
  "language": "am"
}
```

**POST /chat/start/ — Response**
```json
{
  "session_id": "uuid",
  "message": "ሰላም! እኔ የጤና ረዳትዎ ነኝ። ዛሬ ዋናው ምልክትዎ ምንድን ነው?",
  "step": 0,
  "done": false
}
```

**POST /chat/{session_id}/message/ — Response**
```json
{
  "conditions": [
    {"name": "Malaria", "score": 0.8, "id": "malaria"},
    {"name": "Typhoid", "score": 0.3, "id": "typhoid"}
  ],
  "urgency_level": "medium",
  "recommendations": "Visit your nearest health center within 24 hours.",
  "self_care": "Rest, drink fluids, take paracetamol for fever.",
  "red_flags": ["Difficulty breathing — seek emergency care immediately"],
  "done": true
}
```

**POST /assess/ — Request Body**
```json
{
  "symptoms": ["fever", "headache", "fatigue"],
  "age": 28,
  "sex": "female",
  "language": "en"
}
```

### Knowledge Base
| Method | Endpoint | Description |
|---|---|---|
| GET | /tips/ | List health tips (optional ?category=) |
| GET | /facilities/ | List health facilities (optional ?region=) |
| GET | /conditions/ | List all conditions |

### Consultations & Appointments
| Method | Endpoint | Description |
|---|---|---|
| GET | /consultations/ | List consultations |
| GET | /appointments/ | List appointments |
| POST | /appointments/book/ | Book an appointment |

**POST /appointments/book/ — Request Body**
```json
{
  "patient_name": "Almaz Tadesse",
  "patient_phone": "+251911234567",
  "facility_name": "Gondar Health Center",
  "appointment_date": "2026-06-15",
  "appointment_time": "10:00",
  "reason": "Headache and fever",
  "language": "am"
}
```

### Medications
| Method | Endpoint | Description |
|---|---|---|
| GET | /medications/ | Search medications (?q=paracetamol) |
| GET | /medications/{id}/ | Medication detail |

### Facilities
| Method | Endpoint | Description |
|---|---|---|
| GET | /facilities/nearest/ | Nearest facilities (?lat=&lon=&radius=) |
| GET | /facilities/live/ | Live nearby facilities (Google Places) |

### Children / Growth / Vaccines
| Method | Endpoint | Description |
|---|---|---|
| POST | /children/register/ | Register a child |
| GET | /children/{id}/growth/ | Growth history |
| POST | /children/{id}/growth/add/ | Add growth record |
| POST | /growth/assess/ | Assess growth (WHO) |
| GET | /children/{id}/vaccines/ | Vaccine schedule |
| POST | /children/{id}/vaccines/add/ | Log vaccine dose |

### Pregnancy
| Method | Endpoint | Description |
|---|---|---|
| POST | /pregnancy/register/ | Register pregnancy |
| GET | /pregnancy/{id}/schedule/ | ANC schedule |
| POST | /pregnancy/{id}/anc/add/ | Log ANC visit |

### HEW Tools
| Method | Endpoint | Description |
|---|---|---|
| GET | /hew/checklists/ | List checklist types |
| GET | /hew/checklists/{type}/ | Get checklist |
| POST | /hew/checklists/submit/ | Submit checklist |

### SMS
| Method | Endpoint | Description |
|---|---|---|
| POST | /sms/inbound/ | Inbound SMS webhook |
| POST | /sms/send/ | Send SMS |
| GET | /sms/logs/ | SMS logs |

### Reminders
| Method | Endpoint | Description |
|---|---|---|
| GET | /reminders/ | List reminders |
| POST | /reminders/subscribe/ | Subscribe |
| POST | /reminders/{id}/unsubscribe/ | Unsubscribe |

### Analytics & Outbreak
| Method | Endpoint | Description |
|---|---|---|
| GET | /analytics/ | Dashboard KPIs |
| GET | /analytics/consultations/ | Consultation analytics |
| GET | /outbreak/alerts/ | Outbreak alerts |
| GET | /outbreak/trend/{condition_id}/ | Disease trend |

### DHIS2 Integration
| Method | Endpoint | Description |
|---|---|---|
| POST | /dhis2/export/ | Export aggregate data |
| POST | /dhis2/push/ | Push data to DHIS2 |

### Translation
| Method | Endpoint | Description |
|---|---|---|
| POST | /translate/ | Translate text |
| GET | /translate/languages/ | Supported languages |
| GET | /translate/cache/ | Cache stats |
| POST | /translate/cache/clear/ | Clear cache |

### Mental Health
| Method | Endpoint | Description |
|---|---|---|
| GET | /mental-health/questions/ | PHQ-9 / GAD-7 questions |
| POST | /mental-health/screen/ | Submit screening |

### Nutrition
| Method | Endpoint | Description |
|---|---|---|
| GET | /nutrition/iycf/ | IYCF guidance |
| GET | /nutrition/micronutrients/ | Micronutrient guidance |
| GET | /nutrition/therapeutic/ | Therapeutic feeding |
| POST | /nutrition/assess/ | Nutrition risk assessment |

### Chronic Disease
| Method | Endpoint | Description |
|---|---|---|
| POST | /chronic/bp/ | BP assessment |
| POST | /chronic/glucose/ | Glucose assessment |
| POST | /chronic/patients/register/ | Register patient |
| GET | /chronic/patients/{id}/readings/ | Patient readings |
| POST | /chronic/patients/{id}/readings/add/ | Add reading |

### Supply Chain
| Method | Endpoint | Description |
|---|---|---|
| GET | /supply/list/ | Supply list |
| POST | /supply/report/ | Report shortage |

### Traditional Medicine
| Method | Endpoint | Description |
|---|---|---|
| GET | /trad-medicine/ | Search remedies |
| GET | /trad-medicine/{id}/ | Remedy detail |
| POST | /trad-medicine/check-interactions/ | Check interactions |

### Emergency
| Method | Endpoint | Description |
|---|---|---|
| GET | /emergency-contacts/ | List contacts |
| POST | /emergency-contacts/create/ | Add contact |
| POST | /emergency-alert/send/ | Send alert |

### USSD / IVR
| Method | Endpoint | Description |
|---|---|---|
| POST | /ussd/ | USSD webhook |
| POST | /ivr/ | IVR webhook |

### Feedback
| Method | Endpoint | Description |
|---|---|---|
| POST | /feedback/ | Submit rating |
| GET | /feedback/stats/ | Feedback statistics |

### Accessibility
| Method | Endpoint | Description |
|---|---|---|
| POST | /accessibility/consent/submit/ | Submit consent |
| POST | /accessibility/consent/{id}/withdraw/ | Withdraw consent |
| GET | /accessibility/languages/ | Supported languages |

---

## 10. Knowledge Base

The medical knowledge base is stored as a single JSON file (`data/knowledge_base.json`, ~4060 lines) with the following structure:

```json
{
  "conditions": [
    {
      "id": "malaria",
      "name_en": "Malaria",
      "name_am": "ወባ",
      "name_ti": "ወርቂ",
      "name_om": "Busaa",
      "symptoms": ["fever", "chills", "sweating", "headache", "fatigue"],
      "description_en": "A life-threatening disease transmitted by mosquitoes...",
      "description_am": "...",
      "self_care_en": "Rest, drink fluids, take paracetamol for fever...",
      "self_care_am": "...",
      "urgency": "medium",
      "red_flags": ["difficulty breathing", "convulsions", "severe weakness"]
    }
  ],
  "medications": [...],
  "facilities": [...],
  "health_tips": [...]
}
```

Languages supported per condition: English, Amharic, Tigrinya, Oromo.

---

## 11. Urgency Classification Logic

```
IF any red-flag symptom present
   (difficulty breathing, loss of consciousness, heavy bleeding, seizure, chest pain):
    urgency = HIGH  ->  emergency

ELSE IF condition score > 0.5 AND condition is serious (malaria, TB, sepsis):
    urgency = MEDIUM  ->  visit health center

ELSE IF symptoms present < 3 days AND no red flags:
    urgency = LOW  ->  self-care with monitoring

ELSE:
    urgency = MEDIUM  ->  visit health center to be safe
```

### Urgency Levels

| Level | Color | Action |
|-------|-------|--------|
| Low | Green | Self-care at home |
| Medium | Yellow | Visit health center within 24–48 hrs |
| High | Red | Go to hospital immediately |

---

## 12. Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Symptom assessment is keyword-based (not ML) | Lower accuracy than ML approach | Rule-based fallback; sufficient for prototype |
| English, Amharic, Oromo, Tigrinya only | Excludes Somali, Sidama speakers | Input maps exist for 5+ languages; UI planned for v2 |
| Requires internet for full API access | Reduced functionality offline | PWA service worker caches app shell |
| No authentication system | Open access; no user privacy controls | Acceptable for prototype; JWT/auth planned |
| Voice recognition depends on browser API | Inconsistent across browsers | Server-side STT proxy available as fallback |
| Knowledge base covers ~30 conditions | Rare conditions not covered | Fallback: visit a health center |
| No clinical RCT validation | Cannot claim clinical-grade accuracy | Clear disclaimers; information tool only |
| No formal test suite | Regression risk | Manual testing only in prototype |
| DHIS2 integration is simulated | No live national reporting | REST endpoints scaffolded for production |
| SMS/USSD requires Africa's Talking account | Not functional without credentials | Sandbox mode available for testing |

---

## 13. Future Work

### Version 2 Priorities
1. **Real ML/NLP integration** — Replace keyword symptom engine with intent classification + NER
2. **Language expansion** — Add Somali, Sidama, Afar, Wolaytta, Hadiyya UI support
3. **Authentication** — Add JWT-based user registration and login
4. **PostgreSQL / MongoDB** — Production database scaling
5. **Voice interface improvement** — Server-side ASR for low-resource languages
6. **Telemedicine integration** — Escalate from AI chat to live video consultation
7. **Clinical validation** — Randomized controlled trial comparing health outcomes
8. **Predictive analytics** — ML-based disease outbreak prediction
9. **Full DHIS2 live integration** — Real-time reporting to national health surveillance
10. **HEW dedicated mobile app** — Patient management, community health mapping

### Recommended Pilot Plan
| Phase | Duration | Activity |
|---|---|---|
| Phase 1 | 3 months | Deploy in 5 kebeles in amhara; 200 users |
| Phase 2 | 6 months | Expand to 50 kebeles; add HEW dashboard |
| Phase 3 | 12 months | Regional scale; add amharic language models; clinical validation |
| Phase 4 | 24 months | National scale; DHIS2 live integration; telemedicine |

---

## 14. References

### Standards and Guidelines
- WHO Primary Care Guidelines (2023)
- Ethiopian Standard Treatment Guidelines - Federal Ministry of Health
- ICD-10 Classification - WHO
- DHIS2 API Documentation - docs.dhis2.org

### Key Research Papers
- Esteva et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*, 542, 115-118.
- Wahl et al. (2018). AI and global health: How can AI contribute in resource-poor settings? *BMJ Global Health*, 3(4).
- Mekonnen et al. (2019). Mobile health interventions in LMICs: A systematic review. *JMIR*, 21(7).

### Tools and Libraries
- Django REST Framework - django-rest-framework.org
- React - react.dev
- Leaflet - leafletjs.com
- Africa's Talking USSD API - africastalking.com/ussd

---

## Project Stats

| Metric | Count |
|--------|-------|
| Backend Python files | 62 |
| Backend lines of code | ~7,976 |
| Frontend source files | 47 |
| Frontend lines of code | ~9,022 |
| Knowledge base (JSON) | 1 file, ~4,060 lines |
| Django models | 30+ |
| API endpoints | ~90 |
| Supported languages | 8+ (partial) |
| Git commits | 12 |
| ML models | 0 (rule-based) |
| Test files | 0 (prototype) |

---

*Documentation for: AI-Based Health Assistant for Improving Healthcare Access in Rural Ethiopia*
*Academic Year 2026 | AI Course Project*
