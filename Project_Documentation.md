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
6. Non-Functional Requirements
7. Technology Stack
8. Module Descriptions
9. Database Design
10. API Reference
11. NLP and AI Engine
12. Testing Results
13. Deployment Guide
14. Ethical Framework
15. Known Limitations
16. Future Work
17. References

---

## 1. Project Overview

The AI-Based Health Assistant is a conversational mobile application designed to improve
healthcare access for rural communities in Ethiopia. It provides symptom-based health
guidance, health education, and referral recommendations through a chat interface
accessible on Android smartphones and via USSD on feature phones.

**Primary users:**
- Rural community members who lack access to nearby health facilities
- Health Extension Workers (HEWs) who need decision-support tools for triage and referral

The assistant supports English, Amharic, Oromo and Tigrinya, operates in low-bandwidth environments,
and includes offline functionality for core features. It is not a diagnostic tool
and does not replace professional medical care. It acts as a first-contact health
information bridge.

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
5. Evaluate prototype usability and functional accuracy through structured testing
6. Assess utility as a decision-support tool for Health Extension Workers

---

## 4. System Architecture

The system follows a three-tier client-server architecture:

```
+---------------------------+
|     Presentation Tier     |
|  Android App  |  USSD UI  |
+---------------------------+
           |
+---------------------------+
|     Application Tier      |
|  Django REST API          |
|  NLP Engine (mBERT)       |
|  Symptom Assessment Engine|
|  Recommendation Engine    |
+---------------------------+
           |
+---------------------------+
|       Data Tier           |
|  PostgreSQL (structured)  |
|  MongoDB (knowledge base) |
|  SQLite (on-device cache) |
+---------------------------+
           |
+---------------------------+
|    Integration Layer      |
|  DHIS2 API                |
|  SMS Gateway              |
|  (Africa's Talking)       |
+---------------------------+
```

### Offline Architecture
A local SQLite database on the device caches:
- Core health knowledge base content
- Recent consultation records
- Static facility list

When connectivity is restored, the app syncs with the server automatically.

---

## 5. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | User registration with name, age, sex, location, language preference | High |
| FR-02 | Symptom input via text and voice in English, Amharic, Oromo and Tigrinya | High |
| FR-03 | Structured symptom interview through conversational interface | High |
| FR-04 | Generate ranked list of possible conditions from symptoms | High |
| FR-05 | Classify urgency: self-care / visit health center / emergency | High |
| FR-06 | Health education content in text and audio format | High |
| FR-07 | Proactive health tips based on user profile and season | Medium |
| FR-08 | Nearest health facility lookup based on user location | High |
| FR-09 | Generate referral summary for the user to present at facility | Medium |
| FR-10 | Appointment scheduling at connected health facilities | Medium |
| FR-11 | Medication information: dosage, side effects, interactions | Medium |
| FR-12 | First aid guidance for common emergencies | High |
| FR-13 | Emergency contact numbers for local facilities | High |
| FR-14 | Aggregate anonymized data and report to DHIS2 | Low |
| FR-15 | HEW community health dashboard | Medium |
| FR-16 | Core features available in offline mode | High |
| FR-17 | Data sync when connectivity is restored | High |

---

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Response time under normal network conditions | < 3 seconds |
| NFR-02 | Concurrent user support | 10,000 users |
| NFR-03 | Server uptime | 99.5% |
| NFR-04 | Data encryption in transit | TLS 1.3 |
| NFR-05 | Data encryption at rest | AES-256 |
| NFR-06 | System Usability Scale (SUS) score | >= 70 |
| NFR-07 | First-use navigation without training | <= 5 minutes |
| NFR-08 | Code test coverage | >= 80% |
| NFR-09 | Health data standard compliance | HL7 FHIR |
| NFR-10 | Health system integration | DHIS2 API |
| NFR-11 | Horizontal scalability | Supported |
| NFR-12 | Knowledge base updates | Without downtime |

---

## 7. Technology Stack


### Backend
| Component | Technology |
|---|---|
| Language | Python 3.10 |
| Framework | Django REST Framework |
| Task Queue | Celery |
| Cache and Broker | Redis |
| Primary Database | PostgreSQL 14 |
| Document Store | MongoDB 6.0 |
| On-device Storage | SQLite |

### AI and NLP
| Component | Technology |
|---|---|
| NLP Model | Multilingual BERT (mBERT) fine-tuned |
| NLP Library | Hugging Face Transformers |
| Symptom Classifier | Random Forest (scikit-learn) |
| Text Processing | NLTK, spaCy |
| Deep Learning | TensorFlow 2.x, Keras |

### Mobile (Android)
| Component | Technology |
|---|---|
| Language | Kotlin |
| Architecture | MVVM |
| HTTP Client | Retrofit |
| Local Database | Room |
| Voice Input | Android SpeechRecognizer API |

### USSD Interface
| Component | Technology |
|---|---|
| Language | JavaScript / Node.js |
| Gateway | Africa's Talking USSD API |

### DevOps
| Component | Technology |
|---|---|
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud Hosting | AWS EC2 |
| Web Server | Nginx |
| API Testing | Postman |

---

## 8. Module Descriptions

### 8.1 NLP Module
Processes raw user input (text or voice) to extract health intent and symptom entities.

- **Model**: Fine-tuned mBERT on 15,000 Amharic/English health queries
- **Tasks**: Intent classification, Named Entity Recognition (NER) for symptoms
- **Intent labels**: symptom_report, health_query, appointment_request, emergency
- **Output**: Extracted symptom list and classified intent

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("health-assistant-amharic-bert")
model = AutoModelForTokenClassification.from_pretrained("health-assistant-amharic-bert")
nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_symptoms(user_input: str) -> list:
    """Extract symptom entities from user input text."""
    entities = nlp_pipeline(user_input)
    symptoms = [e["word"] for e in entities if e["entity_group"] == "SYMPTOM"]
    return symptoms
```

### 8.2 Symptom Assessment Engine
Classifies symptoms into probable conditions and assigns urgency level.

- **Model**: Random Forest classifier
- **Training data**: 50,000 symptom-condition pairs from Ethiopian disease surveillance and ICD-10
- **Accuracy**: 84% on test set (top-3 condition prediction)
- **Output**: Top-3 conditions with probabilities, urgency level, recommendations

```python
import joblib

symptom_classifier = joblib.load("models/symptom_classifier_v2.pkl")
mlb = joblib.load("models/symptom_binarizer.pkl")

def assess_symptoms(symptoms: list, patient_age: int, patient_sex: str) -> dict:
    """Generate health assessment from symptom list and patient demographics."""
    symptom_vector = mlb.transform([symptoms])
    probabilities = symptom_classifier.predict_proba(symptom_vector)
    top_conditions = get_top_conditions(probabilities, n=3)
    urgency = classify_urgency(top_conditions, symptoms)
    return {
        "conditions": top_conditions,
        "urgency_level": urgency,
        "recommendations": generate_recommendations(top_conditions, urgency)
    }
```

### 8.3 Health Knowledge Base
A curated repository of health information covering Ethiopia's primary disease burden.

- **Format**: JSON documents stored in MongoDB
- **Coverage**: 30+ common conditions including malaria, TB, diarrheal diseases, respiratory infections, maternal health, nutrition
- **Languages**: English, Amharic, Oromo and Tigrinya for all content
- **Sources**: WHO Primary Care Guidelines, Ethiopian Standard Treatment Guidelines, FMOH materials

### 8.4 Referral and Recommendation Engine
Maps urgency level to recommended action and provides facility information.

| Urgency Level | Color Code | Recommended Action |
|---|---|---|
| Low | Green | Self-care guidance provided |
| Medium | Yellow | Visit nearest health post or health center |
| High | Red | Seek emergency care immediately |

### 8.5 USSD Interface
Menu-driven interface for feature phones without internet access.

- Powered by Africa's Talking USSD API
- Covers: symptom reporting (simplified), health tips, facility finder
- No smartphone or internet required

### 8.6 Offline Sync Module
Manages local data caching and server synchronization.

- Caches knowledge base, recent consultations, and facility list to SQLite
- Detects connectivity and triggers sync automatically
- Handles conflict resolution for simultaneous updates

---

## 9. Database Design

### users
```
user_id         UUID PRIMARY KEY
full_name       VARCHAR(100)
age             INTEGER
sex             VARCHAR(10)
region          VARCHAR(50)
woreda          VARCHAR(50)
kebele          VARCHAR(50)
phone_number    VARCHAR(20)
language_pref   VARCHAR(10)   -- 'am' or 'en'
created_at      TIMESTAMP
last_login      TIMESTAMP
```

### health_profiles
```
profile_id          UUID PRIMARY KEY
user_id             UUID FOREIGN KEY -> users
medical_history     TEXT
allergies           TEXT
chronic_conditions  TEXT
current_medications TEXT
updated_at          TIMESTAMP
```

### consultations
```
consultation_id   UUID PRIMARY KEY
user_id           UUID FOREIGN KEY -> users
start_time        TIMESTAMP
end_time          TIMESTAMP
primary_symptom   VARCHAR(100)
all_symptoms      JSONB
assessment_result JSONB
urgency_level     ENUM('low','medium','high')
recommendations   TEXT
status            VARCHAR(20)
```

### conditions
```
condition_id    UUID PRIMARY KEY
icd_code        VARCHAR(10)
name_en         VARCHAR(100)
name_am         VARCHAR(100)
description_en  TEXT
description_am  TEXT
symptoms        JSONB
treatments      TEXT
urgency_level   VARCHAR(10)
category        VARCHAR(50)
```

### health_facilities
```
facility_id     UUID PRIMARY KEY
name            VARCHAR(100)
facility_type   VARCHAR(50)
region          VARCHAR(50)
woreda          VARCHAR(50)
kebele          VARCHAR(50)
latitude        DECIMAL(9,6)
longitude       DECIMAL(9,6)
phone           VARCHAR(20)
services        JSONB
operating_hours VARCHAR(100)
```

### appointments
```
appointment_id  UUID PRIMARY KEY
user_id         UUID FOREIGN KEY -> users
facility_id     UUID FOREIGN KEY -> health_facilities
scheduled_time  TIMESTAMP
reason          TEXT
status          ENUM('pending','confirmed','cancelled','completed')
created_at      TIMESTAMP
```

### health_content
```
content_id      UUID PRIMARY KEY
title_en        VARCHAR(200)
title_am        VARCHAR(200)
category        VARCHAR(50)
content_type    VARCHAR(20)
text_en         TEXT
text_am         TEXT
audio_url_en    VARCHAR(255)
audio_url_am    VARCHAR(255)
target_audience VARCHAR(50)
published_at    TIMESTAMP
```

---

## 10. API Reference

**Base URL:** `https://api.healthassistant.et/api/v1`

All endpoints require `Authorization: Bearer <token>` except `/auth/register` and `/auth/login`.

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Authenticate and receive JWT token |
| POST | /auth/refresh | Refresh access token |

**POST /auth/register — Request Body**
```json
{
  "full_name": "Almaz Tadesse",
  "age": 28,
  "sex": "female",
  "region": "Oromia",
  "phone_number": "+251911234567",
  "language_preference": "am"
}
```

**POST /auth/login — Response**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "expires_in": 3600
}
```

### Consultations
| Method | Endpoint | Description |
|---|---|---|
| POST | /consultations/start | Start a new symptom assessment session |
| POST | /consultations/{id}/message | Send a message in an active consultation |
| GET | /consultations/{id}/assessment | Retrieve the final assessment result |
| GET | /consultations/history | Get user consultation history |

**GET /consultations/{id}/assessment — Response**
```json
{
  "consultation_id": "uuid",
  "conditions": [
    { "name": "Malaria", "probability": 0.72, "icd_code": "B54" },
    { "name": "Typhoid Fever", "probability": 0.15, "icd_code": "A01.0" }
  ],
  "urgency_level": "medium",
  "recommendations": "Visit your nearest health center within 24 hours.",
  "self_care_advice": "Rest, drink fluids, take paracetamol for fever.",
  "red_flags": ["Difficulty breathing", "Seizures - seek emergency care immediately"]
}
```

### Facilities
| Method | Endpoint | Description |
|---|---|---|
| GET | /facilities/nearby | Get nearby health facilities |
| GET | /facilities/{id} | Get details for a specific facility |

**GET /facilities/nearby — Query Parameters**
```
latitude=9.0250&longitude=38.7469&radius_km=20&type=health_center
```

### Appointments
| Method | Endpoint | Description |
|---|---|---|
| POST | /appointments | Schedule an appointment |
| GET | /appointments | List user appointments |
| PATCH | /appointments/{id} | Update appointment status |

### Health Content
| Method | Endpoint | Description |
|---|---|---|
| GET | /content/education | List health education articles |
| GET | /content/education/{id} | Get a specific article |
| GET | /content/categories | List content categories |

---

## 11. NLP and AI Engine

### Model Details
| Property | Value |
|---|---|
| Base model | bert-base-multilingual-cased (mBERT) |
| Fine-tuning dataset | 15,000 Amharic/English health queries |
| Tasks | Intent classification + NER symptom extraction |
| Library | Hugging Face Transformers 4.x |

### Intent Classes
| Intent | Description | Example |
|---|---|---|
| symptom_report | User describing symptoms | 'I have fever and cough' |
| health_query | General health information request | 'How do I prevent malaria?' |
| appointment_request | User wants to book a visit | 'I want to see a doctor' |
| emergency | Urgent or life-threatening situation | 'My wife is bleeding heavily' |
| greeting | Conversation opener | 'Hello' |
| out_of_scope | Non-health topic | Redirect to health topics |

### Symptom Classifier
| Property | Value |
|---|---|
| Algorithm | Random Forest |
| Training samples | 50,000 symptom-condition pairs |
| Features | Symptom binary vector + age + sex |
| Top-1 accuracy | 67% |
| Top-3 accuracy | 84% |

### Urgency Classification Logic
```
IF any red-flag symptom present
   (difficulty breathing, loss of consciousness, heavy bleeding, seizure, chest pain):
    urgency = HIGH  ->  emergency

ELSE IF top condition probability > 0.6 AND condition is serious (malaria, TB, sepsis):
    urgency = MEDIUM  ->  visit health center

ELSE IF symptoms present < 3 days AND no red flags:
    urgency = LOW  ->  self-care with monitoring

ELSE:
    urgency = MEDIUM  ->  visit health center to be safe
```

---

## 12. Testing Results

### Unit Testing
| Module | Tests | Passed | Pass Rate |
|---|---|---|---|
| NLP Module | 45 | 43 | 95.6% |
| Symptom Assessment Engine | 60 | 57 | 95.0% |
| User Management | 30 | 30 | 100% |
| Facility Finder | 25 | 24 | 96.0% |
| Appointment Scheduler | 20 | 20 | 100% |
| Offline Sync Module | 35 | 33 | 94.3% |
| **Total** | **215** | **207** | **96.3%** |

### User Acceptance Testing (UAT)
**Participants:** 45 users — 30 community members + 15 HEWs  
**Location:** 3 rural communities, Oromia region  
**Duration:** 2 weeks

| Task | Completion Rate | Avg. Time |
|---|---|---|
| Register and create profile | 93% | 4.2 min |
| Report symptoms and receive assessment | 87% | 6.8 min |
| Access health education article | 96% | 2.1 min |
| Find nearest health facility | 91% | 3.4 min |
| Schedule appointment | 82% | 5.6 min |
| Use voice input for symptom reporting | 78% | 7.3 min |
| Access system in offline mode | 89% | 3.9 min |

### Key Metrics
| Metric | Result |
|---|---|
| SUS Score - Overall | 74.3 / 100 (Good) |
| SUS Score - HEWs | 79.1 / 100 |
| SUS Score - Community members | 71.8 / 100 |
| Symptom accuracy - Top-1 | 67% |
| Symptom accuracy - Top-3 | 81% |
| User satisfaction | 84% |
| Would use the system again | 91% |
| Amharic language support rated highly | 96% |
| Audio health content rated highly | 89% |

### Issues Found in UAT
| Issue | Severity | Status |
|---|---|---|
| Voice recognition drops in noisy outdoor environments | Medium | Backlog |
| Symptom interview too long (>10 questions) | Medium | Fixed in Sprint 10 |
| Appointment feature underused | Low | UX improvement planned |
| Users requested Oromo language support | High | Planned for v2 |
| DHIS2 data format mapping errors | Medium | Fixed - transformation layer added |
| Offline sync conflict resolution failures | Medium | Fixed in Sprint 9 |

---

## 13. Deployment Guide

### Prerequisites
- Docker and Docker Compose installed
- AWS EC2 instance (t3.medium or larger)
- Domain name with SSL certificate
- Africa's Talking account (USSD and SMS)
- PostgreSQL 14 and MongoDB 6.0

### Environment Variables (.env)
```
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

DATABASE_URL=postgresql://user:password@db:5432/healthassistant
MONGO_URI=mongodb://mongo:27017/healthassistant
REDIS_URL=redis://redis:6379/0

AFRICASTALKING_USERNAME=your-username
AFRICASTALKING_API_KEY=your-api-key

DHIS2_BASE_URL=https://dhis2.moh.gov.et
DHIS2_USERNAME=your-dhis2-user
DHIS2_PASSWORD=your-dhis2-password

JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24
```

### Startup Commands
```bash
git clone https://github.com/ayele705/AI-Health-Assistant-Ethiopia.git
cd health-assistant-ethiopia
cp backend/.env.example backend/.env
# Edit .env with your values

docker-compose up --build -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py loaddata knowledge_base_seed.json
docker-compose exec backend python manage.py createsuperuser
```

### Services
| Service | Port | Description |
|---|---|---|
| backend | 8000 | Django REST API |
| nginx | 80, 443 | Reverse proxy + SSL |
| postgres | 5432 | Primary database |
| mongo | 27017 | Knowledge base store |
| redis | 6379 | Cache and Celery broker |
| celery | - | Async task worker |

### Health Check
```bash
curl https://yourdomain.com/api/v1/health
# Expected: {"status": "ok", "version": "1.0.0"}
```

---

## 14. Ethical Framework

| Principle | Implementation |
|---|---|
| Do No Harm | System is decision-support only; never prescribes treatment or dosages |
| Informed Consent | Users informed at first launch that the system provides information, not diagnosis |
| Privacy by Design | No PII required to use core features; all stored data encrypted |
| Data Minimization | Only data necessary for health guidance is collected |
| Transparency | All AI outputs include confidence indicators and clear disclaimers |
| Human Oversight | All urgency outputs direct users toward human health services |
| Equity | Designed for low-literacy users; audio content included for non-readers |
| Data Sovereignty | Health data stored on servers within Ethiopia |

### User Disclaimer
> This assistant provides general health information only. It does not diagnose illness
> or replace professional medical care. Always consult a qualified health worker or
> visit your nearest health facility for any serious health concern.

### Data Handling
- No real patient data used in training or testing
- Interaction logs stored for 90 days then deleted
- Users can request deletion of their data at any time
- Compliant with Ethiopia's Personal Data Protection Proclamation and GDPR principles

---

## 15. Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Amharic, English, Oromo, Tigrinya only | Excludes Somali, Sidama speakers | Planned for v2 |
| NLP requires internet for full processing | Reduced accuracy offline | Rule-based fallback available offline |
| No clinical RCT validation | Cannot claim clinical-grade accuracy | Clear disclaimers; information tool only |
| Voice recognition degrades in noisy environments | Lower usability outdoors | Improved acoustic model planned |
| Knowledge base covers ~30 conditions | Rare conditions not covered | Fallback: visit a health center |
| No live DHIS2 integration in prototype | Reporting is simulated | Full integration in production version |
| Limited field validation | Real-world effectiveness unconfirmed | Pilot deployment recommended |

---

## 16. Future Work

### Version 2 Priorities
1. **Language expansion** - Add Oromo, Tigrinya, Somali, and Sidama NLP models
2. **Voice interface improvement** - Retrain Amharic ASR on rural accent data
3. **Telemedicine integration** - Escalate from AI chat to live video consultation
4. **Clinical validation** - Randomized controlled trial comparing health outcomes
5. **Predictive analytics** - Disease outbreak detection from consultation data
6. **Wearable integration** - Connect with low-cost pulse oximeters and BP monitors
7. **HEW dedicated app** - Patient management, community health mapping, supply chain
8. **Full DHIS2 integration** - Live reporting to national health surveillance system
9. **Federated learning** - Train models on distributed data without centralizing records
10. **Health equity study** - Measure impact on women, elderly, and people with disabilities

### Recommended Pilot Plan
| Phase | Duration | Activity |
|---|---|---|
| Phase 1 | 3 months | Deploy in 5 kebeles in Oromia; 200 users |
| Phase 2 | 6 months | Expand to 50 kebeles; add HEW dashboard |
| Phase 3 | 12 months | Regional scale; add Oromo language; clinical validation |
| Phase 4 | 24 months | National scale; DHIS2 live integration; telemedicine |

---

## 17. References

### Standards and Guidelines
- WHO Primary Care Guidelines (2023)
- Ethiopian Standard Treatment Guidelines - Federal Ministry of Health
- HL7 FHIR R4 Specification - hl7.org/fhir
- DHIS2 API Documentation - docs.dhis2.org
- ICD-10 Classification - WHO

### Key Research Papers
- Esteva et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*, 542, 115-118.
- Wahl et al. (2018). AI and global health: How can AI contribute in resource-poor settings? *BMJ Global Health*, 3(4).
- Mekonnen et al. (2019). Mobile health interventions in LMICs: A systematic review. *JMIR*, 21(7).
- Rajpurkar et al. (2018). Deep learning for chest radiograph diagnosis. *PLOS Medicine*, 15(11).

### Tools and Libraries
- Hugging Face Transformers - huggingface.co/docs/transformers
- scikit-learn - scikit-learn.org
- Django REST Framework - django-rest-framework.org
- Africa's Talking USSD API - africastalking.com/ussd

---

*Documentation for: AI-Based Health Assistant for Improving Healthcare Access in Rural Ethiopia*
*Academic Year 2026 | AI Course Project*
