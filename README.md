# 🌿 AI-Based Health Assistant for Rural Ethiopia

> An AI-powered conversational health assistant designed to improve healthcare access for rural communities in Ethiopia — supporting Amharic & English, working offline, and accessible on both smartphones and feature phones.

---

## 👥 Group Members

| # | Name | Student ID |
|---|------|-----------|
| 1 | Ayele Moges | GUR/01091/16 |
| 2 | Birihanekulu Tafere | GUR/01115/16 |
| 3 | Amare Minayehu | GUR/22885/16 |
| 4 | Bezawit Desalegn | GUR/01199/16 |
| 5 | Tigist Markos | GUR/00475/16 |

**Department:** Information Science  
**Institution:** University of Gondar  
**Course:** AI Course — Academic Year 2026  
**Date:** May 2026

---

## 📌 About the Project

Ethiopia has fewer than **1 physician per 10,000 people** (WHO), and approximately **80% of the population** lives in rural areas with limited access to health facilities. This project addresses that gap by providing:

- 🩺 Symptom-based health guidance
- 📚 Health education content in Amharic & English
- 📍 Nearest health facility finder
- 📅 Appointment scheduling
- 🚨 Emergency first aid guidance
- 📵 Offline functionality for core features
- 📱 USSD support for feature phones (no smartphone needed)

---

## 🏗️ System Architecture

```
┌─────────────────────────────┐
│      Presentation Tier      │
│   Android App  │  USSD UI   │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│      Application Tier       │
│  Django REST API            │
│  NLP Engine (mBERT)         │
│  Symptom Assessment Engine  │
│  Recommendation Engine      │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│         Data Tier           │
│  PostgreSQL  │  MongoDB     │
│  SQLite (offline cache)     │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│      Integration Layer      │
│  DHIS2 API  │  SMS Gateway  │
│  (Africa's Talking)         │
└─────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Language | Python 3.10 |
| Framework | Django REST Framework |
| Task Queue | Celery |
| Cache & Broker | Redis |
| Primary Database | PostgreSQL 14 |
| Document Store | MongoDB 6.0 |
| On-device Storage | SQLite |

### AI & NLP
| Component | Technology |
|-----------|-----------|
| NLP Model | Multilingual BERT (mBERT) |
| Library | Hugging Face Transformers |
| Symptom Classifier | Random Forest (scikit-learn) |
| Deep Learning | TensorFlow 2.x / Keras |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | React.js |
| Mobile | Android (Kotlin) |
| Architecture | MVVM |

### DevOps
| Component | Technology |
|-----------|-----------|
| Containerization | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Hosting | AWS EC2 |
| Web Server | Nginx |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14
- MongoDB 6.0
- Redis

### 1. Clone the Repository

```bash
git clone https://github.com/ayele705/AI-Health-Assistant-Ethiopia.git
cd AI-Health-Assistant-Ethiopia/health-assistant
```

### 2. Backend Setup

```bash
cd c:\Users\Student\Desktop\AI\health-assistant\backend
pip install -r requirements.txt
copy .env.example .env
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd c:\Users\Student\Desktop\AI\health-assistant\frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

### 4. Using Docker (Recommended)

```bash
cd health-assistant
docker-compose up --build
```

---

## 🔌 API Endpoints

Base URL: `http://localhost:8000/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/consultations/start` | Start symptom assessment |
| POST | `/consultations/{id}/message` | Send message in consultation |
| GET | `/consultations/{id}/assessment` | Get assessment result |
| GET | `/facilities/nearby` | Find nearby health facilities |
| POST | `/appointments` | Schedule an appointment |
| GET | `/content/education` | List health education articles |
| GET | `/translate/languages/` | List supported languages |
| POST | `/translate/` | Translate text |

---

## 🤖 AI Model Performance

| Metric | Result |
|--------|--------|
| Top-1 Accuracy | 67% |
| Top-3 Accuracy | 84% |
| Unit Test Pass Rate | 96.3% |
| SUS Usability Score | 74.3 / 100 (Good) |
| User Satisfaction | 84% |
| Would use again | 91% |

---

## 🚦 Urgency Levels

| Level | Color | Action |
|-------|-------|--------|
| Low | 🟢 Green | Self-care at home |
| Medium | 🟡 Yellow | Visit health center within 24–48 hrs |
| High | 🔴 Red | Go to hospital immediately |

---

## 🔒 Ethical Framework

- **Do No Harm** — decision-support only, never prescribes treatment
- **Informed Consent** — users informed of system limitations at first launch
- **Privacy by Design** — all data encrypted (AES-256, TLS 1.3)
- **Data Sovereignty** — health data stored on servers within Ethiopia
- **Equity** — audio content for non-readers; designed for low-literacy users

> ⚠️ **Disclaimer:** This assistant provides general health information only. It does not diagnose illness or replace professional medical care.

---

## ⚠️ Known Limitations

- Supports Amharic & English only (Oromo, Tigrinya planned for v2)
- Voice recognition degrades in noisy outdoor environments
- Knowledge base covers ~30 common conditions
- No clinical RCT validation (information tool only)

---

## 🔮 Future Work

- Language expansion: Oromo, Tigrinya, Somali, Sidama
- Telemedicine integration (video consultation)
- Clinical validation (randomized controlled trial)
- Disease outbreak prediction from consultation data
- Full DHIS2 live integration

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 📬 Contact

- **Email:** health-assistant@example.com  
- **GitHub:** [github.com/ayele705/AI-Health-Assistant-Ethiopia](https://github.com/ayele705/AI-Health-Assistant-Ethiopia)

---

*Made with ❤️ for rural Ethiopia — University of Gondar, Department of Information Science*
