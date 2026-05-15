#  AI Health Assistant — Rural Ethiopia

> An AI-powered health guidance system for rural Ethiopian communities.
> Supports symptom assessment, CHW tools, SMS reminders, analytics, and more — in 9 languages.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Quick Start](#quick-start)
5. [API Reference](#api-reference)
6. [Languages Supported](#languages-supported)
7. [Architecture](#architecture)
8. [Configuration](#configuration)
9. [Deployment (Docker)](#deployment-docker)
10. [Project Structure](#project-structure)

---

## Overview

The AI Health Assistant is a Django REST API + React PWA designed to bridge the healthcare access gap in rural Ethiopia. It provides:

- **Symptom assessment** via conversational chat in local languages
- **Community Health Worker (CHW) tools** — growth monitoring, vaccination tracking, pregnancy follow-up
- **SMS reminders** via Africa's Talking
- **Analytics dashboard** with outbreak detection and DHIS2 reporting
- **Rural enhancements** — USSD/IVR, offline mode, emergency alerts, traditional medicine KB
- **New health programs** — mental health screening, chronic disease management, nutrition counseling, supply tracking

---

## Features

### Core (Phase 1)
| Feature | Description |
|---|---|
|  Symptom Chat | 5-question conversational assessment in user's language |
|  Medication Lookup | Search by name, generic, or condition |
|  Facility Finder | GPS-based nearest facility with distance |
|  Health Tips | Categorized education content in 9 languages |
|  Differential Diagnosis | Confidence-scored condition matching |

### Community Health Worker Tools (Phase 2)
| Feature | Description |
|---|---|
|  Growth Monitoring | MUAC, weight-for-age, height-for-age with SAM/MAM classification |
|  Vaccination Tracker | EPI schedule tracking with due-date alerts |
|  Pregnancy Follow-up | ANC scheduling, BP danger sign detection, EDD calculation |
|  HEW Checklists | Home visit checklists for newborn, sick child, postnatal, ANC |

### SMS & Reminders (Phase 3)
| Feature | Description |
|---|---|
|  Medication Reminders | Daily SMS reminders via Africa's Talking |
|  Appointment Reminders | Automated SMS before appointments |
|  Danger Alerts | Emergency SMS to patient and contacts |
|  SMS Chat | Inbound SMS symptom assessment |

### Analytics & Reporting (Phase 4)
| Feature | Description |
|---|---|
|  Analytics Dashboard | Consultations, growth, vaccination, pregnancy stats |
|  Outbreak Detection | Disease spike detection with regional alerts |
|  DHIS2 Integration | Export and push health data to national HMIS |

### Rural Community Enhancements
| Feature | Description |
|---|---|
|  USSD/IVR | Feature-phone access via Africa's Talking |
|  Referral Tracker | CHW referral management with follow-up |
|  Community Calendar | Vaccination days, CHW visits, health events |
|  Traditional Medicine KB | 25+ Ethiopian remedies with interaction checking |
|  Emergency Contacts | Multi-contact SMS alert with 10-second countdown |

### New Health Programs (Phase 5)
| Feature | Description |
|---|---|
|  Mental Health Screen | PHQ-2 + GAD-2 with culturally adapted messaging |
|  Chronic Disease | BP and glucose tracking, adherence reminders |
|  Nutrition Counseling | IYCF guidance, SAM/MAM protocols, micronutrients |
|  Supply Tracker | HEW stock reporting and shortage alerts |
| ⭐ Feedback & Ratings | Quality improvement through user ratings |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, PWA, Web Speech API, TensorFlow.js |
| Backend | Python 3, Django 4.2, Django REST Framework |
| Database | SQLite (dev) / PostgreSQL (prod) |
| SMS/USSD | Africa's Talking |
| TTS | ElevenLabs (human voice) → Google TTS (fallback) |
| Translation | Google Cloud Translation API + SQLite cache |
| Scheduler | APScheduler |
| Containerization | Docker, Docker Compose |

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip

### Backend

```bash
cd health-assistant/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at **http://localhost:8000**

### Frontend

```bash
cd health-assistant/frontend
npm install
npm start
```

Frontend runs at **http://localhost:3000**

> The frontend proxies all `/api/v1/` requests to the backend automatically.

---

## API Reference

### Core Chat & Assessment

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/chat/start/` | Start a symptom assessment session |
| POST | `/api/v1/chat/{session_id}/message/` | Send a message in a session |
| POST | `/api/v1/assess/` | Direct symptom assessment |
| POST | `/api/v1/differential/` | Enhanced differential diagnosis |
| GET | `/api/v1/safe-response/` | Safe uncertainty message |

### Knowledge Base

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/tips/` | Health education tips |
| GET | `/api/v1/facilities/` | All health facilities |
| GET | `/api/v1/conditions/` | All conditions in KB |
| GET | `/api/v1/medications/` | Medication search |
| GET | `/api/v1/facilities/nearest/` | Nearest facilities by GPS |

### CHW Tools

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/children/register/` | Register a child |
| POST | `/api/v1/children/{id}/growth/add/` | Add growth measurement |
| GET | `/api/v1/children/{id}/vaccines/` | Vaccine schedule |
| POST | `/api/v1/pregnancy/register/` | Register pregnancy |
| POST | `/api/v1/pregnancy/{id}/anc/add/` | Record ANC visit |
| GET | `/api/v1/hew/checklists/` | HEW checklist types |

### SMS & Reminders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/sms/inbound/` | Africa's Talking webhook |
| POST | `/api/v1/reminders/subscribe/` | Subscribe to medication reminders |
| POST | `/api/v1/sms/danger-alert/` | Send danger sign alert |

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/analytics/` | Full dashboard |
| GET | `/api/v1/outbreak/alerts/` | Outbreak alerts |
| GET | `/api/v1/dhis2/export/` | DHIS2 JSON export |
| POST | `/api/v1/dhis2/push/` | Push to DHIS2 |

### New Programs (Phase 5)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/mental-health/questions/` | PHQ-2 + GAD-2 questions |
| POST | `/api/v1/mental-health/screen/` | Run mental health screen |
| POST | `/api/v1/chronic/bp/` | Assess blood pressure |
| POST | `/api/v1/chronic/glucose/` | Assess blood glucose |
| GET | `/api/v1/nutrition/iycf/` | IYCF guidance by age |
| POST | `/api/v1/supply/report/` | Submit stock shortage report |
| POST | `/api/v1/feedback/` | Submit feedback rating |

### Example Requests

**Start a chat in Amharic:**
```json
POST /api/v1/chat/start/
{ "language": "am" }
```

**Direct symptom assessment:**
```json
POST /api/v1/assess/
{
  "symptoms": ["fever", "headache", "chills"],
  "age": 30,
  "sex": "female",
  "language": "en"
}
```

**Blood pressure assessment:**
```json
POST /api/v1/chronic/bp/
{ "systolic": 145, "diastolic": 92, "language": "am" }
```

**Mental health screening:**
```json
POST /api/v1/mental-health/screen/
{ "phq2_scores": [2, 1], "gad2_scores": [1, 2], "language": "am" }
```

---

## Languages Supported

| Code | Language | Script |
|---|---|---|
| `en` | English | Latin |
| `am` | Amharic | Ethiopic (Ge'ez) |
| `om` | Oromo | Latin |
| `ti` | Tigrinya | Ethiopic (Ge'ez) |
| `sid` | Sidama | Latin |
| `so` | Somali | Latin |
| `aa` | Afar | Latin |
| `wal` | Wolaytta | Latin |
| `had` | Hadiyya | Latin |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              React PWA Frontend              │
│  Components · Hooks · i18n · Service Worker  │
│  IndexedDB · AES-256 Offline Storage         │
└──────────────────┬──────────────────────────┘
                   │ REST API (proxy :8000)
┌──────────────────▼──────────────────────────┐
│           Django REST API Backend            │
│                                              │
│  Core Engines:                               │
│  · Symptom Engine  · Growth Engine           │
│  · Vaccine Schedule · Pregnancy Engine       │
│  · SMS Engine      · Analytics Engine        │
│  · Outbreak Detector · DHIS2 Reporter        │
│  · Mental Health   · Chronic Disease         │
│  · Nutrition       · Supply Chain            │
│  · Traditional Medicine · Emergency          │
│  · USSD Engine     · Translation Service     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              External Services               │
│  Africa's Talking · DHIS2 · ElevenLabs TTS  │
│  Google Translate · OpenStreetMap            │
└─────────────────────────────────────────────┘
```

---

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp health-assistant/backend/.env.example health-assistant/backend/.env
```

Key settings:

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key |  |
| `DEBUG` | True for development |  |
| `AT_API_KEY` | Africa's Talking API key | For SMS |
| `AT_USERNAME` | Africa's Talking username | For SMS |
| `GOOGLE_PLACES_API_KEY` | Google Places API | For live facility search |
| `GOOGLE_TRANSLATE_API_KEY` | Google Cloud Translation | For translation |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS | For human voice |
| `ELEVENLABS_VOICE_ID` | ElevenLabs voice ID | For human voice |
| `DHIS2_URL` | DHIS2 server URL | For reporting |

---

## Deployment (Docker)

```bash
cd health-assistant
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## Project Structure

```
health-assistant/
├── backend/
│   ├── api/                    # Django app — views, models, migrations
│   │   ├── views.py            # Core API views
│   │   ├── models.py           # Database models
│   │   ├── urls.py             # URL routing (40+ endpoints)
│   │   ├── mental_health_views.py
│   │   ├── chronic_disease_views.py
│   │   ├── nutrition_views.py
│   │   ├── supply_chain_views.py
│   │   ├── emergency_views.py
│   │   ├── referral_views.py
│   │   ├── calendar_views.py
│   │   └── trad_medicine_views.py
│   ├── core/                   # Business logic engines
│   │   ├── chatbot.py
│   │   ├── symptom_engine.py
│   │   ├── knowledge_base.py
│   │   ├── growth_engine.py
│   │   ├── vaccine_schedule.py
│   │   ├── pregnancy_engine.py
│   │   ├── sms_engine.py
│   │   ├── analytics_engine.py
│   │   ├── mental_health_engine.py
│   │   ├── chronic_disease_engine.py
│   │   ├── nutrition_engine.py
│   │   └── supply_chain_engine.py
│   ├── data/
│   │   ├── knowledge_base.json         # 50+ conditions
│   │   └── traditional_medicine_kb.json # 25 remedies
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # 30+ React components
│   │   ├── services/           # offlineStore, syncManager, p2pSync
│   │   ├── i18n/               # 9 language JSON files
│   │   ├── context/            # BandwidthContext
│   │   ├── hooks/              # useVoice
│   │   ├── App.js              # Main app with navigation
│   │   └── api.js              # API client
│   └── package.json
└── docker-compose.yml
```

---

## Knowledge Base

The system covers **50+ medical conditions** including:

- **Infectious:** Malaria, Pneumonia, Tuberculosis, Typhoid, Meningitis, HIV/AIDS
- **Maternal:** Pregnancy complications, Preeclampsia, Postpartum hemorrhage
- **Child:** Malnutrition, Dehydration, Measles, Whooping cough
- **Chronic:** Hypertension, Diabetes, Asthma
- **Injury:** Burns, Wounds, Fractures

Each condition includes multilingual names, symptoms, emergency signs, self-care guidance, prevention, treatment, risk factors, and ICD-10 codes.

---

## Ethical Principles

- **Data minimization** — Only symptoms, age range, sex, and language collected
- **Informed consent** — Required before every consultation
- **Clinical safety** — Low-confidence results redirect to health workers
- **Disclaimer** — Every result states it is not a clinical diagnosis
- **Privacy** — No names or phone numbers collected without explicit consent

---

*Built for rural Ethiopian communities · Django + React · 9 languages · 50+ conditions*
