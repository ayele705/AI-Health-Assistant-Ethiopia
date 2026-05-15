# Requirements Document

## Introduction

This document defines requirements for extending the AI-Based Health Assistant for Rural Ethiopia to be
fully accessible and inclusive. The existing system provides symptom assessment, health tips, facility
lookup, appointment booking, and a HEW dashboard via a Django REST Framework backend and React frontend,
with bilingual support (English + Amharic).

This feature extends the system to serve users with disabilities (blind, low-vision, deaf, motor-impaired,
cognitive-impaired, low-literacy), adds voice IVR and offline TTS/ASR channels, SMS/USSD interfaces,
multilingual support for Amharic, Oromo, Tigrinya, and Sidamo, accessible informed-consent flows,
caregiver-consent safeguards, Braille/tactile resource integration, accessibility QA, KPI tracking,
community engagement tooling, and a safety/ethics/privacy framework.

---

## Glossary

- **Health_Assistant**: The AI-Based Health Assistant system for rural Ethiopia (backend + frontend + channels).
- **IVR_Channel**: The Interactive Voice Response telephone channel that allows users to interact via voice or keypad.
- **SMS_USSD_Channel**: The SMS and USSD interface for feature-phone users without smartphones.
- **TTS_Engine**: The Text-to-Speech engine that converts text responses into spoken audio.
- **ASR_Engine**: The Automatic Speech Recognition engine that converts spoken input into text.
- **Accessibility_Layer**: The cross-cutting module that enforces WCAG 2.1 AA compliance, screen-reader support, and motor/cognitive adaptations across all UI surfaces.
- **Consent_Manager**: The module that collects, records, and validates informed consent from users or their caregivers before a consultation begins.
- **Caregiver**: A person (family member, CHV, or HEW) who assists a cognitively impaired or minor user in interacting with the Health_Assistant.
- **CHV**: Community Health Volunteer — a trained community member who supports health outreach.
- **HEW**: Health Extension Worker — a government-employed frontline health worker.
- **Localization_Service**: The module responsible for translating and culturally adapting all system content into Amharic, Oromo, Tigrinya, and Sidamo.
- **Braille_Resource_Module**: The module that generates and distributes Braille/tactile health materials in partnership with disability NGOs.
- **Accessibility_Dashboard**: The administrative view that displays accessibility KPIs, user feedback, and QA checklist results.
- **Safety_Ethics_Module**: The module that enforces data-privacy rules, ethical AI guardrails, and clinical safety thresholds.
- **Pilot_Manager**: The module that tracks field-testing protocols, pilot KPIs, and evaluation plan progress.
- **Language**: One of the four supported languages — Amharic (am), Oromo (om), Tigrinya (ti), Sidamo (sid) — plus English (en).

---

## Requirements

### Requirement 1: Screen-Reader and Visual Accessibility

**User Story:** As a blind or low-vision user, I want the mobile app and web interface to be fully
navigable by screen reader and to offer high-contrast and large-text modes, so that I can use the
Health_Assistant independently without sighted assistance.

#### Acceptance Criteria

1. THE Accessibility_Layer SHALL render all interactive elements with ARIA roles, labels, and
   descriptions conforming to WCAG 2.1 Level AA.
2. THE Accessibility_Layer SHALL provide a high-contrast color theme that meets a minimum contrast
   ratio of 4.5:1 for normal text and 3:1 for large text.
3. THE Accessibility_Layer SHALL provide a large-text mode that scales all body text to a minimum of
   20sp (Android) or 20px (web) without loss of content or functionality.
4. WHEN a screen reader (TalkBack on Android, VoiceOver on iOS, NVDA/JAWS on web) is active,
   THE Accessibility_Layer SHALL announce all state changes, error messages, and new chat messages
   within 500 ms of the change occurring.
5. THE Accessibility_Layer SHALL ensure that no information is conveyed by color alone; icons or
   text labels SHALL accompany all color-coded urgency indicators.
6. WHEN a user activates the high-contrast or large-text mode, THE Health_Assistant SHALL persist
   that preference across sessions for the same device.

---

### Requirement 2: Motor-Impaired User Support

**User Story:** As a motor-impaired user with limited fine-motor control, I want to navigate the
Health_Assistant using switch access, keyboard-only navigation, and large touch targets, so that I
can complete a full consultation without requiring precise touch or mouse input.

#### Acceptance Criteria

1. THE Accessibility_Layer SHALL ensure all interactive touch targets have a minimum size of 48×48 dp
   on Android and 44×44 pt on iOS.
2. THE Accessibility_Layer SHALL support full keyboard navigation (Tab, Shift+Tab, Enter, Space,
   Arrow keys) on the web interface with a visible focus indicator at all times.
3. THE Accessibility_Layer SHALL support Android Switch Access and iOS Switch Control for all
   interactive elements in the mobile app.
4. WHEN a user navigates using keyboard or switch access, THE Accessibility_Layer SHALL maintain
   logical focus order that follows the visual reading order of the page.
5. THE Accessibility_Layer SHALL not require time-limited interactions; WHEN a timed prompt is
   displayed, THE Health_Assistant SHALL provide an option to extend or disable the timeout.

---

### Requirement 3: Deaf and Hard-of-Hearing User Support

**User Story:** As a deaf or hard-of-hearing user, I want all audio content to have text equivalents
and visual alerts, so that I can receive the same health information as hearing users.

#### Acceptance Criteria

1. THE Accessibility_Layer SHALL provide text captions or transcripts for all audio and video content
   within the Health_Assistant.
2. WHEN the IVR_Channel delivers a voice message, THE SMS_USSD_Channel SHALL simultaneously deliver
   an equivalent text message to users who have registered a deaf/hard-of-hearing preference.
3. THE Accessibility_Layer SHALL replace all audio-only alerts (e.g., emergency notifications) with
   visual banners and, where supported by the device, haptic vibration patterns.
4. THE Health_Assistant SHALL not require voice input as the sole modality for any interaction;
   a text-based alternative SHALL be available for every voice-driven flow.

---

### Requirement 4: Cognitive Accessibility and Low-Literacy Support

**User Story:** As a user with cognitive impairment or low literacy, I want the Health_Assistant to
use simple language, pictograms, and short prompts, so that I can understand and respond to health
questions without confusion.

#### Acceptance Criteria

1. THE Accessibility_Layer SHALL offer a "Simple Mode" that limits all prompts to a maximum of
   15 words per sentence and uses a reading level equivalent to Grade 3 or below (Flesch-Kincaid
   Grade Level ≤ 3.0 for English; equivalent simplicity for other languages).
2. THE Accessibility_Layer SHALL display pictogram icons alongside all symptom options, urgency
   levels, and navigation actions in Simple Mode.
3. WHEN a user selects Simple Mode, THE Health_Assistant SHALL reduce the number of options
   presented per screen to a maximum of 3.
4. THE Accessibility_Layer SHALL provide a "Repeat" function on every prompt that re-reads or
   re-displays the current question when activated.
5. WHEN a user provides an unrecognized or ambiguous response 2 consecutive times, THE
   Health_Assistant SHALL offer to connect the user to a CHV or HEW for assisted navigation.

---

### Requirement 5: Voice IVR Channel

**User Story:** As a rural user with a basic feature phone, I want to call a toll-free IVR number
and receive health guidance by voice in my local language, so that I can access the Health_Assistant
without a smartphone or internet connection.

#### Acceptance Criteria

1. THE IVR_Channel SHALL accept inbound calls and present a language-selection menu in Amharic,
   Oromo, Tigrinya, Sidamo, and English within 5 seconds of call connection.
2. WHEN a caller selects a language, THE IVR_Channel SHALL conduct the full symptom-assessment
   conversation using TTS_Engine output and DTMF keypad or voice input.
3. THE IVR_Channel SHALL support voice input via ASR_Engine with a word-error rate of ≤ 30% for
   each of the four supported Ethiopian languages under typical rural call conditions (GSM codec,
   background noise ≤ 60 dB SPL).
4. WHEN the ASR_Engine fails to recognize a caller's input after 2 attempts, THE IVR_Channel SHALL
   fall back to DTMF keypad prompts for the same question.
5. THE IVR_Channel SHALL deliver the assessment result and referral recommendation by voice at the
   end of the call and SHALL offer to send an SMS summary to the caller's number.
6. THE IVR_Channel SHALL complete a standard 5-question symptom assessment call in ≤ 4 minutes
   of total call duration.
7. IF a caller's symptoms trigger an emergency alert, THEN THE IVR_Channel SHALL immediately play
   an emergency message and provide the nearest facility phone number before ending the call.

---

### Requirement 6: Offline TTS/ASR for Mobile App

**User Story:** As a mobile app user in an area with no internet connectivity, I want the app to
speak prompts aloud and understand my spoken responses using on-device models, so that I can
complete a consultation without a data connection.

#### Acceptance Criteria

1. THE TTS_Engine SHALL operate fully on-device without requiring a network connection, supporting
   Amharic, Oromo, Tigrinya, Sidamo, and English.
2. THE ASR_Engine SHALL operate fully on-device without requiring a network connection, supporting
   the same five languages.
3. WHEN the device has no network connectivity, THE Health_Assistant SHALL automatically activate
   offline TTS/ASR mode and notify the user that offline mode is active.
4. THE TTS_Engine SHALL produce intelligible speech with a Mean Opinion Score (MOS) of ≥ 3.5 out
   of 5.0 as evaluated by native speakers of each supported language.
5. THE ASR_Engine SHALL achieve a word-error rate of ≤ 35% for health-domain vocabulary in each
   supported language when tested on a held-out set of 200 utterances per language.
6. WHEN network connectivity is restored, THE Health_Assistant SHALL offer to sync any offline
   consultation records to the server without data loss.

---

### Requirement 7: SMS/USSD Interface

**User Story:** As a feature-phone user without voice capability or internet, I want to interact
with the Health_Assistant via SMS or USSD menus, so that I can receive symptom guidance and
referral information using only basic text messaging.

#### Acceptance Criteria

1. THE SMS_USSD_Channel SHALL provide a USSD menu accessible by dialing a short code (e.g., *123#)
   that guides users through symptom selection using numbered options.
2. THE SMS_USSD_Channel SHALL limit each USSD screen to a maximum of 182 characters to comply with
   GSM USSD session limits.
3. THE SMS_USSD_Channel SHALL support keyword-based SMS interaction, where a user sends a symptom
   keyword and receives a structured SMS reply with assessment and referral guidance.
4. WHEN a USSD session times out before completion, THE SMS_USSD_Channel SHALL send an SMS to the
   user's number with a session-resume link or callback option.
5. THE SMS_USSD_Channel SHALL support all four Ethiopian languages plus English for both USSD menus
   and SMS replies, selectable at the start of each session.
6. IF a user's USSD symptom selection triggers an emergency alert, THEN THE SMS_USSD_Channel SHALL
   send an emergency SMS with the nearest facility name and phone number within 30 seconds.
7. THE SMS_USSD_Channel SHALL parse incoming SMS messages and route them to the symptom assessment
   engine; FOR ALL valid keyword inputs, parsing then routing then replying SHALL produce a
   semantically equivalent response to the same input via the mobile app (round-trip equivalence).

---

### Requirement 8: Multilingual TTS/ASR — Amharic, Oromo, Tigrinya, Sidamo

**User Story:** As a speaker of Oromo, Tigrinya, or Sidamo, I want the Health_Assistant to speak
and understand my language, so that I can receive health guidance in my mother tongue.

#### Acceptance Criteria

1. THE Localization_Service SHALL provide complete translations of all system prompts, symptom
   names, condition descriptions, self-care advice, and emergency messages in Amharic, Oromo,
   Tigrinya, and Sidamo.
2. THE TTS_Engine SHALL produce natural-sounding speech for each of the four Ethiopian languages,
   validated by at least 5 native-speaker evaluators per language with a MOS of ≥ 3.5.
3. THE ASR_Engine SHALL recognize health-domain vocabulary in each of the four Ethiopian languages
   with a word-error rate of ≤ 35% on a held-out evaluation set.
4. THE Localization_Service SHALL maintain a terminology glossary for each language that maps
   medical terms to culturally appropriate lay equivalents, reviewed by a qualified health
   professional fluent in that language.
5. WHEN a new language is added to the Localization_Service, THE Health_Assistant SHALL pass a
   round-trip test: for all entries in the terminology glossary, translating from English to the
   target language and back to English SHALL preserve clinical meaning as verified by a bilingual
   health professional.
6. THE Localization_Service SHALL version-control all translations so that updates to source
   content propagate to all language variants within 5 business days.

---

### Requirement 9: Braille and Tactile Resource Integration

**User Story:** As a blind user or a disability NGO partner, I want the Health_Assistant to generate
and distribute Braille and tactile health materials, so that blind users who cannot use digital
devices can still access key health information.

#### Acceptance Criteria

1. THE Braille_Resource_Module SHALL generate Braille-ready print files (BRF format) for all
   health tip categories, emergency sign summaries, and facility contact sheets.
2. THE Braille_Resource_Module SHALL expose an API endpoint that disability NGO partners can call
   to request Braille files for a specified language and content category.
3. WHEN a Braille file is requested, THE Braille_Resource_Module SHALL return the BRF file within
   10 seconds for content already in the knowledge base.
4. THE Braille_Resource_Module SHALL support Amharic Braille (using the standard Ethiopic Braille
   code) and English Braille (Grade 2 UEB).
5. THE Health_Assistant SHALL maintain a partner registry of disability NGOs with API access
   credentials, contact information, and distribution territory.

---

### Requirement 10: Accessible Informed Consent

**User Story:** As a user beginning a consultation, I want to receive an informed-consent
explanation in my language and preferred modality (voice, text, or SMS), so that I understand
what data is collected and how it is used before I proceed.

#### Acceptance Criteria

1. THE Consent_Manager SHALL present an informed-consent script at the start of every new
   consultation session, before any health data is collected.
2. THE Consent_Manager SHALL deliver the consent script in the user's selected language via the
   active channel: voice on IVR_Channel, text on SMS_USSD_Channel, and text-with-TTS on the
   mobile app.
3. THE Consent_Manager SHALL require an explicit affirmative response (voice "yes", keypad "1",
   or tap "I Agree") before proceeding; WHEN no affirmative response is received, THE
   Consent_Manager SHALL end the session and not collect any health data.
4. THE Consent_Manager SHALL record the consent event with a timestamp, session ID, channel,
   language, and consent type (user or caregiver) in a tamper-evident audit log.
5. THE Consent_Manager SHALL provide a "withdraw consent" option at any point during a session;
   WHEN a user withdraws consent, THE Health_Assistant SHALL immediately stop data collection
   and delete all health data collected in that session.
6. THE Consent_Manager SHALL make the full consent text available for download or SMS delivery
   upon user request.

---

### Requirement 11: Caregiver Consent for Cognitively Impaired Users

**User Story:** As a caregiver of a cognitively impaired or minor user, I want to provide consent
on behalf of the user and be guided through the consultation, so that the user receives appropriate
health guidance with proper ethical safeguards.

#### Acceptance Criteria

1. THE Consent_Manager SHALL offer a "Caregiver Mode" option at the consent screen, allowing a
   caregiver to identify themselves and provide consent on behalf of the user.
2. WHEN Caregiver Mode is activated, THE Consent_Manager SHALL collect the caregiver's name,
   relationship to the user, and contact number before proceeding.
3. WHILE Caregiver Mode is active, THE Health_Assistant SHALL address prompts to the caregiver
   and use simplified language appropriate for proxy reporting of a third party's symptoms.
4. THE Consent_Manager SHALL record caregiver consent events separately from user consent events
   in the audit log, including the caregiver's relationship and contact details.
5. IF a user identified as a minor (age < 18) attempts to start a session without a caregiver,
   THEN THE Health_Assistant SHALL display a message advising the user to involve a trusted adult
   and SHALL offer to connect to a CHV.
6. THE Consent_Manager SHALL not allow a single caregiver account to provide consent for more
   than 10 distinct users per 24-hour period without HEW supervisor review.

---

### Requirement 12: Accessibility QA Checklist and Inclusive Test Cases

**User Story:** As a QA engineer or accessibility auditor, I want a structured checklist and
automated test suite that validates all accessibility requirements, so that regressions are caught
before each release.

#### Acceptance Criteria

1. THE Health_Assistant SHALL maintain an accessibility QA checklist covering all WCAG 2.1 AA
   success criteria applicable to the system, with a pass/fail status for each criterion.
2. THE Health_Assistant SHALL include automated accessibility tests (using axe-core or equivalent)
   that run on every CI build and fail the build if any WCAG 2.1 AA violation is introduced.
3. THE Health_Assistant SHALL include end-to-end test cases for each disability user persona:
   blind user (screen reader), low-vision user (high contrast + large text), deaf user (no audio),
   motor-impaired user (keyboard/switch only), cognitive user (Simple Mode), and low-literacy user
   (pictogram mode).
4. WHEN an accessibility test fails, THE Health_Assistant CI pipeline SHALL block the merge and
   generate a report identifying the failing criterion, affected component, and remediation guidance.
5. THE Health_Assistant SHALL conduct manual accessibility testing with at least 3 users per
   disability category before each major release (defined as a version increment in the major or
   minor version number).

---

### Requirement 13: Accessibility KPIs and User Feedback Collection

**User Story:** As a program manager, I want to track accessibility KPIs and collect structured
user feedback from users with disabilities, so that I can measure inclusion progress and prioritize
improvements.

#### Acceptance Criteria

1. THE Accessibility_Dashboard SHALL display the following KPIs updated daily: percentage of
   sessions using each accessibility mode (screen reader, high contrast, large text, Simple Mode,
   IVR, SMS/USSD), task-completion rate per accessibility mode, and average session duration per
   accessibility mode.
2. THE Health_Assistant SHALL present a 3-question accessibility feedback survey (rating scale 1–5)
   at the end of every 10th session for a given user, delivered in the user's active channel and
   language.
3. THE Accessibility_Dashboard SHALL aggregate feedback scores by disability category, language,
   and channel, and SHALL flag any category with an average score below 3.0 for immediate review.
4. WHEN a user submits a feedback score of 1 or 2, THE Health_Assistant SHALL offer a free-text
   or voice comment field and SHALL route the feedback to the accessibility team within 24 hours.
5. THE Accessibility_Dashboard SHALL export KPI data in CSV format on demand for use in donor
   reports and evaluation plans.

---

### Requirement 14: Community Engagement — CHV and Disability Advocate Training

**User Story:** As a CHV or disability advocate, I want access to training materials and a
structured onboarding flow within the Health_Assistant, so that I can effectively support users
with disabilities in my community.

#### Acceptance Criteria

1. THE Health_Assistant SHALL provide a CHV/Advocate training module accessible from the HEW
   Dashboard, containing step-by-step guides for assisting users with each disability category.
2. THE Health_Assistant SHALL deliver training content in all five supported languages (Amharic,
   Oromo, Tigrinya, Sidamo, English) in both text and audio formats.
3. THE Health_Assistant SHALL include a competency quiz at the end of each training module;
   WHEN a CHV scores below 70% on the quiz, THE Health_Assistant SHALL require the CHV to
   retake the module before being granted "Certified Accessibility Supporter" status.
4. THE Health_Assistant SHALL maintain a registry of Certified Accessibility Supporters with
   their name, region, contact number, and certification date.
5. WHEN a user in Simple Mode or Caregiver Mode requests CHV assistance, THE Health_Assistant
   SHALL look up the nearest Certified Accessibility Supporter in the registry and display their
   contact information.

---

### Requirement 15: Evaluation Plan, Field-Testing Protocol, and Pilot KPIs

**User Story:** As a researcher or program evaluator, I want a structured evaluation plan and
field-testing protocol embedded in the system, so that pilot results can be systematically
collected and reported.

#### Acceptance Criteria

1. THE Pilot_Manager SHALL record the following data points for every pilot session: session ID,
   channel, language, accessibility modes used, consultation completion status, urgency outcome,
   consent type, and timestamp.
2. THE Pilot_Manager SHALL compute and display the following pilot KPIs on the Accessibility_Dashboard:
   total sessions by channel and language, consultation completion rate, emergency escalation rate,
   consent withdrawal rate, and average feedback score.
3. THE Pilot_Manager SHALL support configurable pilot cohorts, allowing an administrator to define
   a cohort by region, facility, or CHV group and track KPIs separately per cohort.
4. WHEN a pilot cohort reaches its target sample size (configurable per cohort), THE Pilot_Manager
   SHALL send an automated notification to the designated evaluator.
5. THE Pilot_Manager SHALL export a structured pilot report in PDF and CSV formats, including all
   KPIs, cohort definitions, and aggregated feedback scores, on demand.
6. THE Health_Assistant SHALL include a field-testing checklist that CHVs complete after each
   assisted session, covering device compatibility, network conditions, user comprehension, and
   any adverse events.

---

### Requirement 16: Deployment Stack — Mobile App, SMS/USSD, IVR, Central Dashboard

**User Story:** As a system administrator, I want a unified deployment stack that integrates the
mobile app, SMS/USSD gateway, IVR telephony, and central dashboard, so that all channels share
a single backend and data store.

#### Acceptance Criteria

1. THE Health_Assistant SHALL expose a single versioned REST API (v1) that serves all channels:
   mobile app, SMS_USSD_Channel, and IVR_Channel.
2. THE Health_Assistant SHALL integrate with at least one Ethiopian SMS/USSD gateway provider
   (e.g., Ethio Telecom or a licensed MVNO) via a configurable gateway adapter.
3. THE Health_Assistant SHALL integrate with a SIP-compatible VoIP platform for IVR_Channel
   delivery, configurable via environment variables.
4. THE Accessibility_Dashboard SHALL be accessible via a web browser and SHALL display real-time
   data from all channels on a single screen.
5. WHEN a new channel adapter is added, THE Health_Assistant SHALL not require changes to the
   core symptom assessment engine or knowledge base.
6. THE Health_Assistant SHALL support horizontal scaling of the API tier to handle a minimum of
   500 concurrent sessions across all channels.

---

### Requirement 17: Safety, Ethics, and Privacy Framework

**User Story:** As a data protection officer or ethics board member, I want the Health_Assistant
to enforce data minimization, user anonymization, and clinical safety thresholds, so that user
privacy is protected and no harm results from AI-generated health guidance.

#### Acceptance Criteria

1. THE Safety_Ethics_Module SHALL collect only the minimum data necessary for symptom assessment:
   symptoms, age range (not exact age), sex, language, and channel; THE Health_Assistant SHALL
   not collect names, phone numbers, or location data unless the user explicitly provides them
   for appointment booking.
2. THE Safety_Ethics_Module SHALL anonymize all consultation records by replacing any user-provided
   identifiers with a pseudonymous session ID before storing in the database.
3. THE Safety_Ethics_Module SHALL enforce a clinical safety threshold: WHEN the symptom assessment
   engine produces a result with a top-condition score below 0.15, THE Health_Assistant SHALL
   present the safe-uncertainty message and recommend visiting a health worker, rather than
   displaying a low-confidence condition match.
4. THE Safety_Ethics_Module SHALL log all emergency escalation events with session ID, urgency
   level, and timestamp in a separate audit log accessible only to authorized HEW supervisors.
5. THE Health_Assistant SHALL display a disclaimer on every assessment result stating that the
   output is not a clinical diagnosis and does not replace professional medical advice, in the
   user's active language.
6. THE Safety_Ethics_Module SHALL comply with Ethiopia's Personal Data Protection Proclamation
   and SHALL provide a data-deletion endpoint that removes all records associated with a session
   ID within 72 hours of a verified deletion request.
7. WHEN a user under age 18 is identified, THE Safety_Ethics_Module SHALL apply additional data
   minimization: no demographic data beyond age range and sex SHALL be stored for minor users.

---

### Requirement 18: Localization and Cultural Adaptation

**User Story:** As a content manager, I want all health content to be culturally adapted for each
supported language community, so that messages are appropriate, trusted, and actionable for users
in each region.

#### Acceptance Criteria

1. THE Localization_Service SHALL adapt all health tip content, symptom descriptions, and self-care
   advice for cultural appropriateness in each language community, reviewed by a community health
   expert fluent in that language.
2. THE Localization_Service SHALL avoid direct translations of idioms or culturally sensitive terms;
   WHEN a term has no culturally appropriate equivalent, THE Localization_Service SHALL use a
   descriptive phrase approved by the community health reviewer.
3. THE Localization_Service SHALL support right-to-left text rendering for any future language
   additions that require it, without requiring changes to the core UI components.
4. THE Localization_Service SHALL store all localized strings in a structured resource file
   (JSON or PO format) per language, enabling non-developer translators to update content
   without modifying source code.
5. WHEN a localized string is missing for a given language, THE Health_Assistant SHALL fall back
   to the Amharic string, then to English, and SHALL log the missing key for translator review.
6. THE Localization_Service SHALL include culturally adapted pictograms for each symptom and
   urgency level, reviewed for cultural appropriateness by community members in each region.

---

### Requirement 19: Funding and Partner Outreach Support

**User Story:** As a project coordinator, I want the Health_Assistant to generate structured
partner outreach materials and funding proposal data exports, so that I can efficiently engage
NGOs, donors, and government partners.

#### Acceptance Criteria

1. THE Accessibility_Dashboard SHALL provide a "Partner Report" export that summarizes system
   reach (sessions by region, language, channel, and disability category) in a format suitable
   for donor reporting.
2. THE Health_Assistant SHALL maintain a partner registry with fields for organization name,
   type (NGO, government, donor), contact person, territory, and partnership status.
3. WHEN a new partner is added to the registry, THE Health_Assistant SHALL send an automated
   welcome email with API credentials (for NGO partners) or a summary report (for donor partners).
4. THE Accessibility_Dashboard SHALL display a funding KPI panel showing: number of active
   partners, total sessions attributed to partner-supported regions, and Braille materials
   distributed per partner.
