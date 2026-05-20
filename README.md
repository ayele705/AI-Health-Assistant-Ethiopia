# AI-Based Health Assistant for Rural Ethiopia

> An AI-powered conversational health assistant designed to improve healthcare access for rural communities in Ethiopia — supporting English, Amharic, Oromo & Tigrinya, with offline PWA support and USSD access for feature phones.

---

**Department:** Information Science  
**Institution:** University of Gondar  
**Course:** AI Course — Academic Year 2026  
**Date:** May 2026

---

## About the Project

Ethiopia has fewer than **1 physician per 10,000 people** (WHO), and approximately **80% of the population** lives in rural areas with limited access to health facilities. This project addresses that gap by providing:

- Symptom-based health guidance via keyword matching
- Multi-turn conversational symptom interview (5-step)
- Health education content in English, Amharic, Oromo & Tigrinya
- Nearest health facility finder
- Appointment scheduling
- Emergency first aid guidance
- Offline functionality (PWA service worker)
- USSD support for feature phones (Africa's Talking)
- Growth monitoring for children (WHO standards)
- Vaccination tracking (Ethiopia EPI schedule)
- Pregnancy follow-up & ANC visit tracking
- HEW (Health Extension Worker) checklists
- SMS reminders and alerts
- Outbreak detection (threshold-based)
- DHIS2 integration (simulated)
- Mental health screening
- Nutrition counseling (IYCF, micronutrients, therapeutic feeding)
- Chronic disease management (BP, glucose tracking)
- Supply chain / stock shortage reporting
- Traditional medicine lookup & interaction checking
- Translation (pre-built cache + Google Translate API)

---

## System Architecture

```
┌──────────────────────────────────────────────────┐
│               Presentation Tier                   │
│              React SPA (PWA)                      │
│        USSD / IVR (Africa's Talking)              │
│        SMS Chat / Voice (Web Speech API)          │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│               Application Tier                    │
│   Django REST Framework (API)                     │
│   Symptom Assessment Engine (keyword-based)       │
│   Rule-based Chatbot (multi-turn interview)       │
│   Medical domain engines (growth, vaccine, etc.)  │
│   Translation Service (cache + Google API)        │
│   SMS/USSD Engine (Africa's Talking)              │
│   APScheduler (reminders)                         │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│                  Data Tier                         │
│   SQLite (primary database)                       │
│   JSON Knowledge Base (30+ conditions)            │
│   Translation Cache (SQLite)                      │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              Integration Layer                     │
│   DHIS2 API (REST export/push)                    │
│   Africa's Talking SMS/USSD Gateway               │
│   Google Cloud Translation API                    │
│   Google Places API (facility lookup)             │
└───────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| Framework | Django 4.2 + Django REST Framework |
| Database | SQLite |
| Task Scheduler | APScheduler |
| SMS/USSD | Africa's Talking SDK |

### Medical Domain Engines
| Component | Approach |
|-----------|----------|
| Symptom Assessment | Keyword-based multilingual symptom matching |
| Chatbot | Rule-based multi-turn interview (5 steps) |
| Growth Monitoring | WHO standard comparison tables |
| Vaccine Scheduling | Ethiopia EPI static schedule |
| Pregnancy Tracking | ANC visit schedule calculator |
| Outbreak Detection | Threshold-based alerts |
| Translation | Pre-built JSON cache + Google Translate API fallback |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | React 18 |
| Maps | Leaflet / react-leaflet |
| PWA | Service worker + manifest.json |
| Voice Input | Web Speech API |
| Offline Storage | Cache API |
| Styling | Custom CSS |

### USSD Interface
| Component | Technology |
|-----------|-----------|
| Language | Python (Django views) |
| Gateway | Africa's Talking USSD API |

### DevOps
| Component | Technology |
|-----------|-----------|
| Containerization | Docker & Docker Compose |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Navigate to the Project

```bash
cd health-assistant
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

If `npm` is blocked in PowerShell, use `npm.cmd` instead or enable script execution with:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Frontend runs at: `http://localhost:3000`

### 4. Using Docker

```bash
cd health-assistant
docker-compose up --build
```

> Note: Docker Compose launches backend and frontend services. Frontend build may need a Dockerfile added.

---

## API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/start/` | Start a new chat session |
| POST | `/chat/{session_id}/message/` | Send a message in session |
| POST | `/assess/` | Quick symptom assessment (single step) |
| POST | `/safe-response/` | Get safe, disclaimered health info |
| GET | `/tips/` | List health tips |
| GET | `/facilities/` | List health facilities |
| GET | `/conditions/` | List all conditions in knowledge base |
| GET | `/consultations/` | List consultations |
| GET | `/appointments/` | List all appointments |
| POST | `/appointments/book/` | Book an appointment |
| GET | `/medications/` | Search medications |
| GET | `/medications/{id}/` | Medication detail |
| GET | `/facilities/nearest/` | Find nearest facilities |
| POST | `/differential/` | Differential diagnosis |
| POST | `/children/register/` | Register a child |
| GET | `/children/{id}/growth/` | Growth history |
| POST | `/children/{id}/growth/add/` | Add growth record |
| POST | `/growth/assess/` | Assess growth (WHO) |
| GET | `/children/{id}/vaccines/` | Vaccine schedule |
| POST | `/children/{id}/vaccines/add/` | Log vaccine |
| POST | `/pregnancy/register/` | Register pregnancy |
| GET | `/pregnancy/{id}/schedule/` | ANC visit schedule |
| POST | `/pregnancy/{id}/anc/add/` | Log ANC visit |
| GET | `/hew/checklists/` | HEW checklist types |
| POST | `/hew/checklists/submit/` | Submit HEW checklist |
| POST | `/sms/inbound/` | SMS inbound webhook |
| POST | `/sms/send/` | Send SMS |
| GET | `/reminders/` | List reminders |
| POST | `/reminders/subscribe/` | Subscribe to reminder |
| GET | `/analytics/` | Dashboard analytics |
| GET | `/outbreak/alerts/` | Outbreak alerts |
| POST | `/dhis2/export/` | Export data to DHIS2 |
| GET | `/translate/languages/` | Supported translation languages |
| POST | `/translate/` | Translate text |
| POST | `/mental-health/screen/` | Mental health screening |
| POST | `/nutrition/assess/` | Nutrition risk assessment |
| POST | `/chronic/bp/` | Blood pressure assessment |
| POST | `/chronic/glucose/` | Glucose assessment |
| GET | `/supply/list/` | Supply list |
| POST | `/supply/report/` | Report stock shortage |
| POST | `/feedback/` | Submit feedback rating |
| POST | `/ussd/` | USSD webhook |
| POST | `/ivr/` | IVR webhook |
| GET | `/emergency-contacts/` | Emergency contacts |
| POST | `/emergency-alert/send/` | Send emergency alert |
| GET | `/trad-medicine/` | Search traditional medicine |
| POST | `/trad-medicine/check-interactions/` | Check herb-drug interactions |

---

## Urgency Levels

| Level | Color | Action |
|-------|-------|--------|
| Low | Green | Self-care at home |
| Medium | Yellow | Visit health center within 24–48 hrs |
| High | Red | Go to hospital immediately |

---

## Ethical Framework

- **Do No Harm** — decision-support only, never prescribes treatment
- **Informed Consent** — users informed of system limitations at first launch
- **Data Minimization** — only data necessary for health guidance is collected
- **Transparency** — all outputs include clear disclaimers
- **Human Oversight** — all urgency outputs direct users toward human health services
- **Equity** — multilingual content for low-literacy users; audio planned

> **Disclaimer:** This assistant provides general health information only. It does not diagnose illness or replace professional medical care.

---

## Known Limitations

- Supports English, Amharic, Oromo & Tigrinya (Somali, Sidama planned for v2)
- Symptom assessment is keyword-based, not ML-driven
- Voice recognition depends on browser Web Speech API
- Knowledge base covers ~30 common conditions in JSON
- DHIS2 integration is simulated (REST export scaffolded)
- No clinical RCT validation (information tool only)
- No authentication system (open access for prototype)
- SMS/USSD requires Africa's Talking sandbox/production account
- No formal test suite (prototype phase)

---

## Future Work

- Language expansion: Somali, Sidama, Afar, Wolaytta, Hadiyya
- Real ML/NLP integration (intent classification, NER)
- Telemedicine integration (video consultation)
- Clinical validation (randomized controlled trial)
- Disease outbreak prediction from consultation data
- Full DHIS2 live integration
- Dedicated HEW mobile app
- PostgreSQL / MongoDB for production scaling

---

## Project Structure

```
health-assistant/
├── backend/
│   ├── api/               # Django app: views, models, urls, serializers
│   │   ├── views.py       # 30+ API endpoints (~1063 lines)
│   │   ├── models.py      # 15+ Django ORM models (~438 lines)
│   │   ├── urls.py        # ~90 URL routes
│   │   ├── validators.py  # Input validation (~576 lines)
│   │   └── accessibility_models.py / views.py
│   ├── core/              # Business logic engines
│   │   ├── symptom_engine.py     # Keyword-based symptom matching
│   │   ├── chatbot.py            # Multi-turn interview flow
│   │   ├── knowledge_base.py     # JSON KB loader
│   │   ├── growth_engine.py      # WHO growth assessment
│   │   ├── vaccine_schedule.py   # EPI vaccine schedule
│   │   ├── pregnancy_engine.py   # ANC tracking
│   │   ├── outbreak_detector.py  # Threshold-based alerts
│   │   ├── dhis2_reporter.py     # DHIS2 integration
│   │   ├── translation_service.py # Translation cache + API
│   │   ├── sms_engine.py         # Africa's Talking SMS
│   │   ├── ussd_engine.py        # USSD/IVR logic
│   │   ├── medication_engine.py  # Medication lookup
│   │   ├── nutrition_engine.py   # Nutrition guidance
│   │   ├── mental_health_engine.py # PHQ-9/GAD-7 screening
│   │   ├── chronic_disease_engine.py # BP/glucose mgmt
│   │   └── ... more engines
│   ├── config/            # Django settings, URLs, WSGI
│   ├── data/              # Translation files
│   └── manage.py
├── frontend/
│   ├── src/               # React app source
│   │   ├── App.js         # Main SPA (~307 lines)
│   │   ├── api.js         # API client (~269 lines)
│   │   └── components/    # 30+ components
│   └── public/
│       ├── sw.js          # Service worker (offline)
│       └── manifest.json  # PWA manifest
├── data/
│   └── knowledge_base.json  # Medical KB (~4060 lines)
├── docker-compose.yml
└── scripts/
```

---

## License

This project is open source under the [MIT License](LICENSE).

---

## Contact

- **Email:** health-assistant@example.com  
- **GitHub:** [github.com/ayele705/AI-Health-Assistant-Ethiopia](https://github.com/ayele705/AI-Health-Assistant-Ethiopia)

---

*Made for rural Ethiopia — University of Gondar, Department of Information Science*
