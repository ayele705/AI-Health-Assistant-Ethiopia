# AI-Based Health Assistant for Rural Ethiopia
## Presentation Slides

---

## SLIDE 1 — Title

#  AI-Based Health Assistant
## Improving Healthcare Access in Rural Ethiopia

**Presented by:** Ayele Moges
**Institution:** University of Gondar
**Date:** May 2026

---

## SLIDE 2 — The Problem

# The Healthcare Crisis in Rural Ethiopia

| Indicator | Ethiopia | WHO Target |
|---|---|---|
| Physicians per 10,000 people | < 1 | 23 |
| Rural population | 80% | — |
| Maternal mortality (per 100k) | 401 | < 70 |
| Under-5 mortality (per 1,000) | 55 | < 25 |

### Key Barriers
- ️ Geographic isolation — patients walk 30+ km to reach care
- ‍️ Severe shortage of health professionals
-  Low health literacy
- ️ 80+ languages — most tools support only English/Amharic
-  Unreliable internet connectivity

---

## SLIDE 3 — The Solution

# AI Health Assistant

> A mobile-accessible, multilingual AI system that brings health guidance directly to rural communities

### What it does
-  Assesses symptoms and gives guidance in the user's language
-  Supports Community Health Workers with digital tools
-  Works on smartphones AND feature phones (USSD)
-  Functions offline — syncs when connectivity returns
-  Sends SMS reminders for medications and appointments
-  Detects disease outbreaks and reports to national HMIS

---

## SLIDE 4 — System Overview

# System Architecture

```
┌─────────────────────────────────┐
│        React PWA Frontend        │
│  9 Languages · Offline Mode      │
│  Voice Input · Accessibility     │
└──────────────┬──────────────────┘
               │ REST API
┌──────────────▼──────────────────┐
│      Django REST API Backend     │
│  24 Core Engines · 50+ Endpoints │
│  50+ Conditions · 9 Languages    │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│       External Integrations      │
│  Africa's Talking · DHIS2        │
│  ElevenLabs TTS · Google Maps    │
└─────────────────────────────────┘
```

---

## SLIDE 5 — Languages

# 9 Ethiopian Languages Supported

| Language | Speakers | Script |
|---|---|---|
|  Amharic | 32M | Ethiopic |
|  Oromo | 40M | Latin |
|  Tigrinya | 7M | Ethiopic |
|  Sidama | 4M | Latin |
|  Somali | 6M | Latin |
|  Afar | 2M | Latin |
|  Wolaytta | 2M | Latin |
|  Hadiyya | 1.5M | Latin |
|  English | — | Latin |

**Combined reach: 90%+ of Ethiopia's population**

---

## SLIDE 6 — Core Features

# Phase 1: Core Health Assistance

###  Symptom Assessment Chat
- Conversational 5-question interview
- Returns top 3 matching conditions with confidence scores
- Urgency classification: Emergency / Visit HC / Self-Care
- Emergency sign detection with immediate alerts

###  Medication Lookup
- Search by name, generic name, or condition
- WHO essential medicines flagged
- Dosage and safety information

###  Facility Finder
- GPS-based nearest facility search
- Distance, phone number, facility type
- Referral chain guidance

---

## SLIDE 7 — CHW Tools

# Phase 2: Community Health Worker Tools

###  Child Growth Monitoring
- MUAC, weight-for-age, height-for-age
- SAM/MAM/Normal classification
- Growth trend charts

###  Vaccination Tracker
- Ethiopia EPI schedule
- Due date alerts
- Coverage tracking

###  Pregnancy Follow-up
- ANC scheduling (8 visits)
- Blood pressure danger sign detection
- EDD calculation

###  HEW Checklists
- Newborn care, sick child, postnatal, ANC
- Digital submission and tracking

---

## SLIDE 8 — SMS & Communication

# Phase 3: SMS & Reminders

```
Patient registers for medication reminder
         ↓
System sends daily SMS at chosen time
         ↓
Patient replies with symptoms via SMS
         ↓
System assesses and replies with guidance
         ↓
If emergency → sends alert to contacts
```

### Powered by Africa's Talking
- Medication reminders
- Appointment reminders
- Danger sign alerts
- Inbound SMS symptom assessment
- USSD feature-phone access

---

## SLIDE 9 — Analytics & DHIS2

# Phase 4: Analytics & Reporting

###  Dashboard Metrics
- Total consultations by urgency level
- Growth/nutrition status trends
- Vaccination coverage rates
- Pregnancy and ANC completion rates

###  Outbreak Detection
- Disease spike detection algorithm
- Regional alert generation
- 7-day trend visualization

###  DHIS2 Integration
- Automatic data export in DHIS2 format
- Push to Ethiopia's national HMIS
- Aligned with HSTP-II reporting requirements

---

## SLIDE 10 — Rural Enhancements

# Rural Community Enhancements

| Feature | Problem Solved |
|---|---|
|  USSD/IVR | Feature phones without internet |
|  Offline Mode | No connectivity in remote areas |
|  Referral Tracker | Lost patients after referral |
|  Community Calendar | Missed vaccination days |
|  Traditional Medicine KB | Community trust and safety |
|  Emergency Contacts | Delayed emergency response |
|  TBA Module | Unsafe home deliveries |
|  Voice Interface | Low literacy users |

---

## SLIDE 11 — New Health Programs

# Phase 5: New Health Programs

###  Mental Health Screening
- PHQ-2 depression screen
- GAD-2 anxiety screen
- Culturally adapted messaging
- Crisis response with hotline

###  Chronic Disease Management
- Blood pressure classification (5 stages)
- Blood glucose assessment
- Medication adherence reminders
- Self-monitoring checklists

###  Nutrition Counseling
- IYCF guidance by child age
- SAM/MAM therapeutic feeding protocols
- Micronutrient deficiency guidance

###  Supply Chain Tracking
- 15 essential supply items
- Shortage detection and alerts
- HEW stock reporting

---

## SLIDE 12 — Voice Technology

# Human Voice with ElevenLabs TTS

### Before (Google TTS)
- Robotic, unnatural sound
- Limited language support
- 200 character limit

### After (ElevenLabs)
-  Natural human voice
-  `eleven_multilingual_v2` model
-  Supports Amharic, Tigrinya, Oromo
-  500 character limit
-  Automatic fallback to Google TTS

### Impact
> Low-literacy users can now receive health guidance in a natural, trustworthy voice in their own language

---

## SLIDE 13 — Knowledge Base

# Medical Knowledge Base

### 50+ Conditions Covered

| Category | Examples |
|---|---|
| Infectious | Malaria, TB, Pneumonia, Typhoid, HIV |
| Maternal | Preeclampsia, PPH, Ectopic pregnancy |
| Child | SAM, Dehydration, Measles |
| Chronic | Hypertension, Diabetes, Asthma |
| Injury | Burns, Wounds, Fractures |

### Each Condition Includes
- Multilingual names (9 languages)
- 10–15 symptoms
- Emergency signs
- Self-care guidance
- Prevention strategies
- ICD-10 codes
- WHO essential medicine flags

### Traditional Medicine KB
- 25 Ethiopian remedies
- Safety notes and interactions
- Culturally respectful framing

---

## SLIDE 14 — Accessibility

# Designed for All Users

### Accessibility Modes
| Mode | For |
|---|---|
|  Text-to-Speech | Blind users |
|  Voice Input | Low-literacy users |
| ️ Screen Reader | Visually impaired |
|  High Contrast | Low vision |
|  Large Text | Elderly users |
|  Hearing Mode | Deaf users |
| 🟢 Simple Mode | Low digital literacy |

### Offline Capability
- AES-256 encrypted local storage
- 90-day patient record retention
- Background sync with exponential backoff
- Works without internet after first load

---

## SLIDE 15 — Ethics & Safety

# Ethical Framework

### Data Protection
-  Minimum data collection (symptoms, age, sex, language only)
-  No names or phone numbers without consent
-  AES-256 encryption for patient records
-  Data deletion on request

### Clinical Safety
-  Every result includes clinical disclaimer
-  Low-confidence results redirect to health workers
-  Emergency signs trigger immediate alerts
-  Minor protection built into safety module

### Cultural Sensitivity
-  Traditional medicine respected and integrated
-  Culturally adapted mental health messaging
-  Community trust built through local language support

---

## SLIDE 16 — Impact

# Expected Impact

### For Rural Communities
- Immediate health guidance without traveling 30+ km
- Emergency alerts reach family within 30 seconds
- Health education in their own language

### For Health Extension Workers
- Digital checklists replace paper forms
- Growth monitoring with automatic classification
- Referral tracking with follow-up reminders

### For the Health System
- Real-time disease surveillance
- Automated DHIS2 reporting
- Supply shortage early warning

### Scale Potential
> With 45% mobile penetration and growing, the system can reach **millions of Ethiopians** without additional infrastructure

---

## SLIDE 17 — Technical Achievements

# What Was Built

| Component | Count |
|---|---|
| API Endpoints | 60+ |
| Database Models | 25+ |
| React Components | 30+ |
| Core Engines | 24 |
| Languages | 9 |
| Conditions in KB | 50+ |
| Traditional Remedies | 25 |
| Migrations | 7 |

### Lines of Code
- Backend (Python): ~8,000 lines
- Frontend (JavaScript): ~12,000 lines
- Total: ~20,000 lines

---

## SLIDE 18 — Demo Flow

# Live Demo Walkthrough

```
1. Open http://localhost:3000
         ↓
2. Select language (Amharic)
         ↓
3. Give consent → Start chat
         ↓
4. Report symptoms: "ትኩሳት፣ ራስ ምታት"
         ↓
5. System assesses → Returns guidance
         ↓
6.  Click speaker → Hear in human voice
         ↓
7. Navigate to Growth Monitor
         ↓
8. Register child → Add MUAC measurement
         ↓
9. System classifies: SAM / MAM / Normal
         ↓
10. View Analytics Dashboard
```

---

## SLIDE 19 — Future Work

# Roadmap

### Short Term (1–3 months)
- [ ] Complete USSD/IVR state machine
- [ ] Finish offline sync with conflict resolution
- [ ] Add P2P sync via WebRTC
- [ ] Record audio health tips (6 categories × 9 languages)

### Medium Term (3–6 months)
- [ ] TensorFlow Lite image-based symptom reporting
- [ ] Health education video library
- [ ] Malaria RDT guidance module
- [ ] Community health mapping

### Long Term (6–12 months)
- [ ] Integration with Ethio Telecom USSD
- [ ] Clinical validation study
- [ ] National deployment with MoH partnership
- [ ] Predictive outbreak modeling

---

## SLIDE 20 — Conclusion

# Summary

### Problem
Rural Ethiopia faces a severe healthcare access crisis — 80% of the population lives far from qualified care.

### Solution
An AI-powered health assistant that works in 9 languages, on any device, with or without internet.

### Achievement
A fully functional system with 60+ API endpoints, 30+ components, 50+ conditions, and 9 languages — covering symptom assessment, CHW tools, SMS reminders, analytics, mental health, chronic disease, nutrition, and supply tracking.

### Alignment
Directly supports Ethiopia's **Health Sector Transformation Plan II** and **Digital Ethiopia 2025** strategy.

---

> *"Technology alone cannot solve Ethiopia's healthcare crisis — but in the hands of community health workers and rural families, the right technology can save lives."*

---

## SLIDE 21 — References

# References

1. World Health Organization. (2023). *Global Health Observatory: Ethiopia*. WHO.
2. Ethiopian Ministry of Health. (2020). *Health Sector Transformation Plan II 2020/21–2024/25*. MoH Ethiopia.
3. Medhanyie, A., et al. (2012). The role of health extension workers in improving utilization of maternal and child health services. *BMC Health Services Research*, 12(1), 352.
4. Olu, O., et al. (2019). Digital health: A catalyst for achieving the health-related SDGs in Africa. *BMJ Global Health*, 4(2), e001497.
5. Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*, 542, 115–118.
6. Ada Health GmbH. (2023). *Ada Health: AI-powered health assessment*. https://ada.com
7. Babylon Health. (2022). *Babylon Health Rwanda*. https://babylonhealth.com
8. Ethiopian Public Health Institute. (2022). *Ethiopia National Health Survey*. EPHI.
9. ElevenLabs. (2024). *Multilingual v2 TTS Model*. https://elevenlabs.io
10. Africa's Talking. (2024). *SMS and USSD API Documentation*. https://africastalking.com

---

*AI Health Assistant · Rural Ethiopia · May 2026*
