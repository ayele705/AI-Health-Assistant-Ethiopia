# Design Document — Accessibility and Inclusion

## Overview

This document describes the technical design for extending the AI-Based Health Assistant for Rural Ethiopia to be fully accessible and inclusive. It covers the frontend accessibility layer, multilingual support, voice/IVR/SMS channels, consent management, safety/ethics module, and the accessibility dashboard.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Channels                       │
│  React Web App │ IVR (SIP/VoIP) │ SMS/USSD │ Mobile App │
└────────────────────────┬────────────────────────────────┘
                         │ REST API v1
┌────────────────────────▼────────────────────────────────┐
│              Django REST Framework Backend               │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐  │
│  │ Accessibility│ │   Consent    │ │  Safety/Ethics  │  │
│  │   Views      │ │   Manager    │ │    Module       │  │
│  └──────────────┘ └──────────────┘ └─────────────────┘  │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐  │
│  │  Symptom     │ │ Localization │ │  Knowledge Base │  │
│  │  Engine      │ │   Service    │ │   (JSON)        │  │
│  └──────────────┘ └──────────────┘ └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    SQLite Database                       │
│  Consultation │ Appointment │ ConsentLog │ A11ySession  │
│  Feedback     │ CHVRegistry │ Partners   │ PilotCohort  │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Frontend Accessibility Layer

### 1.1 AccessibilityContext (`AccessibilityContext.js`)

Manages user preferences persisted in `localStorage`:

| Preference     | Type    | Effect |
|----------------|---------|--------|
| `highContrast` | boolean | Adds `html.high-contrast` CSS class |
| `largeText`    | boolean | Adds `html.large-text` class + sets `font-size: 120%` |
| `simpleMode`   | boolean | Adds `html.simple-mode` class (larger touch targets) |
| `screenReader` | boolean | Adds `html.screen-reader-mode` class + enables  replay buttons |
| `textToSpeech` | boolean | Auto-reads bot messages via Web Speech API |
| `voiceInput`   | boolean | Shows  button in chat using SpeechRecognition API |
| `hearingMode`  | boolean | Adds `html.hearing-mode` class + visual emergency banners |

### 1.2 CSS Accessibility Modes (`App.css`)

- `html.high-contrast` — 4.5:1+ contrast ratio, dark green on white
- `html.large-text` — 120% base font size
- `html.simple-mode` — 48×48dp minimum touch targets
- `html.screen-reader-mode` — 4px focus outline, "Assistant:/You:" prefixes
- `html.hearing-mode` — pulsing red emergency badge animation

### 1.3 ARIA Implementation

All interactive elements have:
- `role="tab"`, `aria-selected` on navigation tabs
- `role="log"`, `aria-live="polite"` on chat message container
- `role="alert"`, `aria-live="assertive"` on emergency banners
- `role="dialog"` on consent screen and accessibility panel
- `aria-label` on all buttons and inputs

---

## 2. Multilingual Support

### 2.1 Supported Languages

| Code | Language | Script |
|------|----------|--------|
| `en` | English  | Latin  |
| `am` | Amharic  | Ethiopic (Ge'ez) |
| `ti` | Tigrinya | Ethiopic (Ge'ez) |
| `om` | Oromo    | Latin  |
| `sid`| Sidamo   | Latin  |

### 2.2 Frontend Translation Pattern

Each component uses a `T` object with per-language keys. Fallback chain: `lang → am → en`.

```js
const t = T[lang] || T['en'];
```

Components translated: `Chat.js`, `Tips.js`, `Facilities.js`, `Appointment.js`, `Dashboard.js`, `AccessibilityDashboard.js`, `AccessibilityToolbar.js`, `ConsentScreen.js`, `App.js`.

### 2.3 Backend Translation Pattern

`knowledge_base.py` uses fallback chain for all localized fields:

```python
def get_field(tip, field):
    return (tip.get(f'{field}_{language}')
            or tip.get(f'{field}_am')
            or tip.get(f'{field}_en', ''))
```

`symptom_engine.py` uses `_get_localized()` with same fallback for condition names, descriptions, self-care advice.

### 2.4 Symptom Translation Maps

Three maps in `symptom_engine.py`:
- `AMHARIC_SYMPTOM_MAP` — Ethiopic → English
- `TIGRINYA_SYMPTOM_MAP` — Ethiopic → English
- `OROMO_SYMPTOM_MAP` — Latin → English

All maps are checked in order for each symptom input.

### 2.5 Knowledge Base Localization

`knowledge_base.json` contains per-language fields for all 16 conditions:
- `name_en`, `name_am`, `name_ti`
- `description_en`, `description_am`, `description_ti`
- `self_care_en`, `self_care_am`, `self_care_ti`
- `emergency_signs_en`, `emergency_signs_am`

All 11 health tips have `title_en/am/ti/om` and `content_en/am/ti/om`.

---

## 3. Consent Management

### 3.1 ConsentScreen Component

Displayed before first chat session. Supports 5 languages. Three actions:
- **Agree** — proceeds to chat
- **Caregiver Mode** — sets `caregiverMode=true`, proceeds to chat
- **Cancel** — redirects to Tips tab

### 3.2 Backend Consent API

Endpoints in `accessibility_views.py`:
- `POST /api/v1/accessibility/consent/submit/` — records consent with session ID, timestamp, language, channel, type
- `DELETE /api/v1/accessibility/consent/{session_id}/withdraw/` — deletes session data

`ConsentLog` model stores: `session_id`, `language`, `channel`, `consent_type` (user/caregiver), `timestamp`, `withdrawn`.

---

## 4. Safety and Ethics Module

### 4.1 Safety Threshold (`core/safety.py`)

```python
SAFETY_THRESHOLD = 0.15

def apply_safety_threshold(result, language):
    top_score = result['conditions'][0]['score'] if result['conditions'] else 0
    if top_score < SAFETY_THRESHOLD:
        result['conditions'] = []
        result['message'] = get_safe_message(language)
    return result
```

Applied in `quick_assess` view before returning results.

### 4.2 Data Minimization

- Consultation records store symptoms, age, sex, language — no names or phone numbers
- Appointment records store patient name and phone only when explicitly provided by user
- Minor users (age < 18): no demographic data beyond age range and sex stored

### 4.3 Disclaimer

Every assessment result includes the safe-uncertainty message when confidence is low. Frontend displays urgency badge with text label (not color alone).

---

## 5. IVR and SMS/USSD Channels

### 5.1 IVR Menu (`core/localization.py`)

`IVR_MENUS` dict provides all prompts in 5 languages:
- `welcome`, `lang_select`, `symptom_prompt`, `duration_prompt`, `other_symptoms`, `age_prompt`, `sex_prompt`, `emergency`, `result_intro`, `sms_offer`, `repeat`, `goodbye`

### 5.2 IVR Endpoint

`POST /api/v1/channels/ivr/` — accepts DTMF input, returns TTS prompt text and next menu state.

### 5.3 SMS Endpoint

`POST /api/v1/channels/sms/` — accepts keyword SMS, routes to symptom engine, returns structured SMS reply.

---

## 6. Accessibility Session Tracking

### 6.1 Models (`accessibility_models.py`)

| Model | Purpose |
|-------|---------|
| `AccessibilitySession` | Tracks modes used, channel, language, completion status |
| `AccessibilityFeedback` | 1–5 rating + optional comment per session |
| `EmergencyAuditLog` | Emergency escalation events |
| `CHVSupporterRegistry` | Certified CHV/advocate registry |
| `PartnerRegistry` | NGO/donor partner registry |
| `PilotCohort` | Pilot cohort definitions |
| `FieldTestChecklist` | CHV field-test checklist submissions |

### 6.2 KPI Dashboard API

`GET /api/v1/accessibility/kpis/` returns:
- `total_sessions`, `completed_sessions`, `completion_rate`
- `mode_counts` (per accessibility mode)
- `average_feedback_score`, `emergency_escalations`, `active_partners`

`GET /api/v1/accessibility/kpis/export/` returns CSV.

---

## 7. Pictogram Support

`core/localization.py` provides `SYMPTOM_PICTOGRAMS` and `URGENCY_PICTOGRAMS` maps:

```python
SYMPTOM_PICTOGRAMS = {
    'fever': '️', 'cough': '‍', 'headache': '', ...
}
URGENCY_PICTOGRAMS = {
    'emergency': '', 'visit_health_center': '', 'self_care': ''
}
```

Used in Simple Mode to display icons alongside text labels.

---

## 8. Gap Analysis — Requirements vs Implementation

| Req | Description | Status |
|-----|-------------|--------|
| 1 | Screen reader + high contrast + large text |  Implemented |
| 2 | Motor impairment — large touch targets, keyboard nav |  Implemented (simple-mode CSS) |
| 3 | Deaf/HoH — visual alerts, text alternatives |  Implemented (hearingMode) |
| 4 | Cognitive/low-literacy — Simple Mode, pictograms |  Implemented |
| 5 | Voice IVR channel | ️ API endpoints exist, no real SIP integration |
| 6 | Offline TTS/ASR | ️ Web Speech API used (online only) |
| 7 | SMS/USSD interface | ️ API endpoints exist, no gateway integration |
| 8 | Multilingual TTS/ASR (am/ti/om/sid) |  Translations complete, TTS via Web Speech API |
| 9 | Braille/tactile resources |  Not implemented |
| 10 | Accessible informed consent |  Implemented |
| 11 | Caregiver consent |  Implemented |
| 12 | Accessibility QA checklist | ️ Manual only, no automated axe-core tests |
| 13 | Accessibility KPIs + feedback |  Dashboard + feedback API implemented |
| 14 | CHV/advocate training module | ️ Registry exists, training content not built |
| 15 | Evaluation plan + pilot KPIs |  PilotCohort + FieldTestChecklist models |
| 16 | Unified deployment stack |  Single REST API, Docker compose |
| 17 | Safety, ethics, privacy |  Safety threshold, data minimization, consent |
| 18 | Localization + cultural adaptation |  5 languages, fallback chain |
| 19 | Partner outreach support |  PartnerRegistry model + dashboard export |

### Gaps to Address

- **Req 5/7**: IVR and SMS/USSD need real gateway integration (Ethio Telecom adapter)
- **Req 6**: Offline TTS/ASR needs on-device models (e.g., Coqui TTS)
- **Req 9**: Braille BRF file generation not implemented
- **Req 12**: Automated axe-core accessibility tests not set up in CI
- **Req 14**: CHV training content and competency quiz not built
