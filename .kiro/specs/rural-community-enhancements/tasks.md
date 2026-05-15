# Implementation Plan: Rural Community Enhancements

## Overview

Implement eight feature areas that extend the existing Django + React PWA health assistant to better serve rural Ethiopian communities. Tasks are ordered to build foundational infrastructure first (offline engine, data models, language packs), then feature-specific components, and finally integration and wiring.

## Tasks

- [ ] 1. Extend Django data models and run migrations
  - Add `EmergencyContact`, `EmergencyAlertLog`, `CalendarEvent`, `PersonalReminder`, `Referral`, `TraditionalRemedy`, and `USSDSessionLog` models to `backend/api/models.py` as specified in the design
  - Create and apply a new migration file `0006_rural_enhancements.py`
  - _Requirements: 2.7, 7.1, 11.1, 12.1, 13.1_

- [ ] 2. Implement Offline Engine and Sync Manager
  - [ ] 2.1 Update Service Worker (`frontend/public/sw.js`)
    - Cache core assets, knowledge base, facility data, medication data, and Language Packs on first load
    - Intercept all API requests and serve IndexedDB-cached responses when offline
    - Fall back to pre-cached offline error page only for requests with no cached equivalent
    - _Requirements: 3.1, 3.2, 3.8_

  - [ ] 2.2 Create `frontend/src/services/offlineStore.js`
    - Define IndexedDB schema with all new stores: `pending_sync`, `patient_records`, `language_packs`, `audio_clips`, `calendar_events`, `referrals`, `emergency_contacts`, `trad_remedies`
    - Implement AES-256 encryption/decryption for all patient record writes and reads using a PIN-derived key
    - _Requirements: 3.3, 3.6, 17.1_

  - [ ]* 2.3 Write property test for offline submission persistence
    - **Property 4: Offline Submission Persistence**
    - **Validates: Requirements 3.3**

  - [ ]* 2.4 Write property test for IndexedDB encryption
    - **Property 16: IndexedDB Encryption**
    - **Validates: Requirements 17.1**

  - [ ] 2.5 Create `frontend/src/services/syncManager.js`
    - Queue offline submissions in `pending_sync` IndexedDB store with timestamp and status
    - On reconnection, replay all `pending_sync` records to the backend within 60 seconds
    - Implement exponential backoff with max 5 retries; mark as `sync_failed` after exhaustion
    - Silently refresh stale data (>30 days) in the background when online
    - _Requirements: 3.3, 3.4, 3.5, 3.7_

  - [ ]* 2.6 Write property test for sync completeness
    - **Property 5: Sync Completeness**
    - **Validates: Requirements 3.4**

  - [ ]* 2.7 Write property test for retry exhaustion
    - **Property 6: Retry Exhaustion**
    - **Validates: Requirements 3.5**

  - [ ]* 2.8 Write property test for auto-save persistence
    - **Property 17: Auto-Save Persistence**
    - **Validates: Requirements 20.1**

- [ ] 3. Checkpoint — Ensure offline engine tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement Language Pack Manager
  - [ ] 4.1 Create `backend/api/language_views.py`
    - `GET /api/language-packs/` — list available packs with sizes
    - `GET /api/language-packs/<lang>/bundle/` — download full pack
    - `GET /api/language-packs/<lang>/audio/` — download audio bundle only
    - Register routes in `backend/api/urls.py`
    - _Requirements: 8.1, 8.2, 8.3_

  - [ ] 4.2 Create `frontend/src/services/languageManager.js`
    - Display download size before initiating download
    - Store downloaded Language Pack in `language_packs` IndexedDB store
    - Fall back to Amharic (audio) / English (text) when pack not downloaded
    - Support dialect variants within a language
    - _Requirements: 8.3, 8.4, 8.6_

  - [ ]* 4.3 Write unit tests for language fallback behaviour
    - Test fallback to Amharic audio and English text when pack missing
    - Test dialect variant selection
    - _Requirements: 8.4, 8.6_

- [ ] 5. Implement Voice Interface
  - [ ] 5.1 Create `frontend/src/hooks/useVoice.js`
    - Capture audio via `window.SpeechRecognition` / `webkitSpeechRecognition`
    - Expose `startListening`, `stopListening`, `speak`, `fallbackAudio` as per design interface
    - Fall back to Language Pack pre-recorded audio when Web Speech API does not support the selected language
    - On empty recognition result, set error state to trigger pictogram fallback
    - Suppress non-essential animations while voice mode is active
    - _Requirements: 1.1, 1.2, 1.4, 1.5, 1.6_

  - [ ] 5.2 Create `frontend/src/components/VoiceInterface.js`
    - Display transcribed text and read it back before submitting to the health assistant
    - Read Health Assistant responses aloud in the user's selected language
    - Offer to send assessment result as SMS on completion
    - _Requirements: 1.2, 1.3, 1.7, 1.8_

  - [ ]* 5.3 Write property test for voice response read-aloud
    - **Property 1: Voice Response Read-Aloud**
    - **Validates: Requirements 1.3**

  - [ ]* 5.4 Write unit tests for voice interface error handling
    - Test empty recognition result → pictogram fallback
    - Test microphone permission denied → text input alternative
    - Test Language Pack audio fallback for unsupported languages
    - _Requirements: 1.4, 1.5_

- [ ] 6. Implement USSD/IVR Gateway
  - [ ] 6.1 Create `backend/core/ussd_engine.py`
    - Implement state machine: `LanguageSelect → SymptomMenu → GuidanceResult → SMSOffer`
    - Return plain-text responses ≤160 characters per page, prefixed `CON` or `END`
    - On session timeout, send SMS summary of last completed step
    - Log sessions using SHA-256 hash of AT session ID (no raw PII stored)
    - _Requirements: 2.1, 2.2, 2.3, 2.6, 2.7_

  - [ ] 6.2 Create `backend/api/ussd_views.py`
    - `POST /api/ussd/` — Africa's Talking USSD webhook handler
    - `POST /api/ivr/` — Africa's Talking IVR webhook handler (TwiML-style XML with `<Say>` prompts)
    - `GET /api/ussd/sessions/` — admin: list anonymised session logs
    - Register routes in `backend/api/urls.py`
    - On IVR emergency result, speak emergency message and provide nearest facility phone number
    - On user request, send full guidance result as SMS
    - _Requirements: 2.4, 2.5, 2.8_

  - [ ]* 6.3 Write property test for USSD response length constraint
    - **Property 2: USSD Response Length Constraint**
    - **Validates: Requirements 2.3**

  - [ ]* 6.4 Write property test for session log anonymisation
    - **Property 3: Session Log Anonymisation**
    - **Validates: Requirements 2.7**

  - [ ]* 6.5 Write unit tests for USSD state machine
    - Test initial language selection menu response
    - Test session timeout → SMS summary
    - Test invalid input → re-display menu with error
    - _Requirements: 2.1, 2.6_

- [ ] 7. Checkpoint — Ensure USSD/IVR and voice tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement Audio Content Store
  - [ ] 8.1 Create `frontend/src/services/audioStore.js`
    - Serve pre-recorded audio health tips (32 kbps MP3) from Cache API when offline
    - Play cached clips within 1 second; stream within 3 seconds when online
    - Support per-language bundle download
    - Respect Low Bandwidth Mode (no auto-download)
    - _Requirements: 4.1, 4.3, 4.4, 4.6, 4.7_

  - [ ] 8.2 Create `frontend/src/components/AudioTips.js`
    - Display each tip with a pictogram, short text label, and play button
    - Show which tips require connectivity to download when offline
    - Allow users to download all audio tips for their language as a single bundle
    - _Requirements: 4.2, 4.4, 4.5_

  - [ ]* 8.3 Write unit tests for audio content store
    - Test cached clip plays within 1 second
    - Test offline indicator for uncached tips
    - Test Low Bandwidth Mode blocks auto-download
    - _Requirements: 4.3, 4.4, 4.6_

- [ ] 9. Implement Image-Based Symptom Reporting
  - [ ] 9.1 Create `frontend/src/services/imageAnalyser.js`
    - Load bundled TF.js model from `/models/skin_classifier/model.json`
    - Classify images into: wound, rash, skin infection, eye condition, other
    - Return `{ category, confidence, low_confidence }` as per design interface
    - Set `low_confidence: true` when confidence < 0.60
    - Compress images to ≤200 KB before upload
    - Store images locally in encrypted form; schedule auto-delete after 30 days
    - _Requirements: 6.2, 6.4, 6.6, 6.7, 6.8_

  - [ ] 9.2 Create `frontend/src/components/ImageSymptom.js`
    - Activate device camera or gallery selection
    - Display classification result with confidence indicator
    - Combine image category with verbal/text symptoms before generating guidance
    - Show retake prompt and offer voice/pictogram alternative when confidence < 60%
    - Present informed consent screen before any image upload
    - _Requirements: 6.1, 6.3, 6.4, 6.5_

  - [ ]* 9.3 Write property test for image and symptom combination
    - **Property 7: Image and Symptom Combination**
    - **Validates: Requirements 6.3**

  - [ ]* 9.4 Write property test for low confidence threshold
    - **Property 8: Low Confidence Threshold**
    - **Validates: Requirements 6.4**

  - [ ]* 9.5 Write unit tests for image analyser
    - Test image compression to ≤200 KB
    - Test auto-delete scheduling after 30 days
    - Test model load failure → fallback to text/voice input
    - _Requirements: 6.6, 6.7, 6.8_

- [ ] 10. Implement Traditional Medicine Knowledge Base
  - [ ] 10.1 Create `backend/data/traditional_medicine_kb.json`
    - Add ≥50 Ethiopian traditional remedy entries following the JSON schema in the design
    - Each entry must include: local names (≥2 Ethiopian languages), common use, active compounds, safety notes, known interactions, serious adverse effect flag, evidence level
    - _Requirements: 7.1_

  - [ ] 10.2 Create `backend/core/trad_medicine_engine.py`
    - Load `traditional_medicine_kb.json` at startup
    - Implement fuzzy name lookup by local name across supported languages
    - Implement interaction check against a user's medication list
    - Return culturally respectful safety notes; display prominent warning for serious adverse effects
    - _Requirements: 7.2, 7.3, 7.4, 7.7_

  - [ ] 10.3 Create Traditional Medicine API views in `backend/api/views.py` (or a new `trad_medicine_views.py`)
    - `GET /api/trad-medicine/search/?q=<name>&language=<lang>`
    - `GET /api/trad-medicine/<id>/`
    - `POST /api/trad-medicine/check-interactions/`
    - `PUT /api/trad-medicine/<id>/` — admin only
    - Register routes in `backend/api/urls.py`
    - _Requirements: 7.6_

  - [ ]* 10.4 Write property test for remedy safety note inclusion
    - **Property 9: Remedy Safety Note Inclusion**
    - **Validates: Requirements 7.2**

  - [ ]* 10.5 Write property test for interaction warning presence
    - **Property 10: Interaction Warning Presence**
    - **Validates: Requirements 7.3**

  - [ ]* 10.6 Write unit tests for traditional medicine engine
    - Test remedy not found → respectful acknowledgement, no crash
    - Test serious adverse effect flag → prominent warning displayed
    - Test TBA extended view for registered TBAs
    - _Requirements: 7.4, 7.5, 7.7_

- [ ] 11. Checkpoint — Ensure traditional medicine and image tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement Emergency Alert Engine
  - [ ] 12.1 Create `backend/core/emergency_engine.py`
    - Implement contact registry logic (up to 5 contacts per user)
    - Trigger on `urgency_level == 'emergency'`; send SMS to all contacts via `core/sms_engine.py`
    - Include in each SMS: user name, condition summary, GPS/nearest location, nearest facility phone + distance
    - Queue SMS in `pending_sync` when offline; send within 60 seconds of reconnection
    - Log every alert event in `EmergencyAlertLog`
    - _Requirements: 11.2, 11.3, 11.4, 11.5, 11.6_

  - [ ] 12.2 Add Emergency Contact API endpoints to `backend/api/views.py`
    - `GET /api/emergency-contacts/`
    - `POST /api/emergency-contacts/`
    - `DELETE /api/emergency-contacts/<id>/`
    - `POST /api/emergency-alert/send/`
    - Register routes in `backend/api/urls.py`
    - _Requirements: 11.1_

  - [ ] 12.3 Create `frontend/src/components/EmergencyAlert.js`
    - Allow users to register up to 5 emergency contacts (name, phone, relationship)
    - Display prominent alert on emergency urgency result
    - Show 10-second cancellation countdown before sending SMS
    - Display warning when no contacts are registered
    - _Requirements: 11.1, 11.2, 11.7_

  - [ ]* 12.4 Write property test for emergency SMS completeness
    - **Property 12: Emergency SMS Completeness**
    - **Validates: Requirements 11.3**

  - [ ]* 12.5 Write property test for cancellation prevents send
    - **Property 13: Cancellation Prevents Send**
    - **Validates: Requirements 11.7**

  - [ ]* 12.6 Write unit tests for emergency alert engine
    - Test no contacts registered → warning displayed
    - Test offline queuing → sends on reconnection
    - Test all SMS sends fail → failure notification with manual retry option
    - _Requirements: 11.4, 11.6_

- [ ] 13. Implement Community Calendar
  - [ ] 13.1 Create `backend/api/calendar_views.py`
    - `GET /api/calendar/?kebele=<kebele>&days=90`
    - `POST /api/calendar/` — CHW/admin: create event
    - `PUT /api/calendar/<id>/`
    - `POST /api/calendar/<id>/remind/` — set personal reminder
    - Register routes in `backend/api/urls.py`
    - Push new events to registered devices within 24 hours via Sync Manager
    - _Requirements: 12.1, 12.3_

  - [ ] 13.2 Create `frontend/src/components/CommunityCalendar.js`
    - Display health events for the user's kebele for the next 90 days using cached data when offline
    - Allow users to set personal reminders (SMS or in-app, 24 h before event)
    - Auto-add child vaccination due dates on child registration
    - Display events in user's language with pictograms alongside text labels
    - _Requirements: 12.2, 12.4, 12.5, 12.6_

  - [ ]* 13.3 Write unit tests for community calendar
    - Test offline display of cached events
    - Test personal reminder creation and SMS delivery
    - Test auto-add vaccination due dates on child registration
    - _Requirements: 12.2, 12.4, 12.5_

- [ ] 14. Implement Referral Tracker
  - [ ] 14.1 Create `backend/api/referral_views.py`
    - `GET /api/referrals/?chw=<id>`
    - `POST /api/referrals/`
    - `PUT /api/referrals/<id>/outcome/`
    - `GET /api/referrals/report/?chw=<id>&month=<YYYY-MM>`
    - Register routes in `backend/api/urls.py`
    - Implement APScheduler job to check for missed visits daily and send SMS reminders 3 days after missed expected visit date
    - _Requirements: 13.1, 13.3, 13.4, 13.5, 13.6_

  - [ ] 14.2 Create `frontend/src/components/ReferralTracker.js`
    - Display open referrals sorted by expected visit date, offline-capable
    - Allow CHW to record referral outcome (attended, not attended, admitted, discharged)
    - Display follow-up tasks prominently when expected date passes without outcome
    - Generate monthly summary report viewable offline
    - _Requirements: 13.2, 13.3, 13.4, 13.6_

  - [ ]* 14.3 Write property test for referral data completeness
    - **Property 14: Referral Data Completeness**
    - **Validates: Requirements 13.1**

  - [ ]* 14.4 Write property test for missed visit SMS trigger
    - **Property 15: Missed Visit SMS Trigger**
    - **Validates: Requirements 13.5**

  - [ ]* 14.5 Write unit tests for referral tracker
    - Test duplicate referral ID → new UUID generated
    - Test missing required field → validation error
    - Test monthly report generation
    - _Requirements: 13.1, 13.6_

- [ ] 15. Checkpoint — Ensure emergency, calendar, and referral tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Implement Low Bandwidth Mode
  - [ ] 16.1 Create `frontend/src/context/BandwidthContext.js`
    - Expose `lowBandwidth` toggle and `sessionDataUsage` counter
    - Auto-suggest enabling Low Bandwidth Mode when Network Information API reports speed < 50 kbps
    - Cache all session responses in IndexedDB when Low Bandwidth Mode is active
    - Display total session data usage in status bar
    - _Requirements: 9.1, 9.5, 9.6, 9.7_

  - [ ] 16.2 Add `?compact=1` support to all Django API views
    - When `compact=1` is present, serialise responses with IDs and essential fields only (no nested objects)
    - Enforce ≤2 KB response payload limit for compact responses
    - Show data usage estimate before each network action in the frontend
    - _Requirements: 9.2, 9.3, 9.4_

  - [ ]* 16.3 Write property test for API payload size limit
    - **Property 11: API Payload Size Limit**
    - **Validates: Requirements 9.4**

  - [ ]* 16.4 Write unit tests for low bandwidth mode
    - Test auto-suggestion when speed < 50 kbps
    - Test image/video/audio auto-load disabled
    - Test data usage estimate displayed before network action
    - _Requirements: 9.2, 9.3, 9.5_

- [ ] 17. Implement P2P Sync
  - [ ] 17.1 Create `frontend/src/services/p2pSync.js`
    - Establish WebRTC data channel between two devices on the same LAN
    - Display pairing code on initiator; require entry on receiver to confirm connection
    - Sync: pending patient records, updated KB entries, Language Pack bundles
    - Encrypt all transmitted data using AES-256
    - On conflict, present both versions to user for explicit selection
    - Display transfer summary on completion; send no data to external servers
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [ ]* 17.2 Write unit tests for P2P sync
    - Test pairing code mismatch → error, allow 3 retries
    - Test connection drop mid-sync → rollback partial sync
    - Test encryption failure → abort and log
    - _Requirements: 10.2, 10.4_

- [ ] 18. Implement CHW Dashboard enhancements
  - [ ] 18.1 Update `frontend/src/components/HEWChecklist.js` and related CHW components
    - Add PIN-protected offline login using locally stored credentials
    - Support offline data entry for: patient registration, symptom assessment, growth measurements, vaccination records, pregnancy follow-up, referral creation
    - Display caseload view with last visit date and overdue follow-ups from cached data
    - Generate printable/SMS-shareable patient summary in patient's local language
    - Display conflict log from Sync Manager when conflicts are resolved
    - Display prominent emergency alert with nearest referral facility when urgency is `emergency`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [ ]* 18.2 Write unit tests for CHW dashboard offline behaviour
    - Test PIN login without network
    - Test UUID preservation on sync
    - Test overdue follow-up display
    - _Requirements: 5.1, 5.2, 5.5_

- [ ] 19. Implement TBA Module
  - [ ] 19.1 Create TBA-specific views and components
    - Add role-based registration for TBA role in `backend/api/models.py` / `views.py`
    - Create `frontend/src/components/TBAModule.js` with: safe delivery checklist, danger signs guide, newborn care checklist, postnatal follow-up schedule
    - Prompt for birth event data: delivery date, birth weight, complications, referral status
    - Activate Emergency Alert Engine on danger sign detection (heavy bleeding, prolonged labour, convulsions, absent foetal movement)
    - Display all checklists with pictograms and audio narration
    - Auto-create follow-up task in Referral Tracker on postnatal visit completion
    - Store all birth records in IndexedDB; sync when online
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6_

  - [ ]* 19.2 Write unit tests for TBA module
    - Test danger sign detection → emergency alert activation
    - Test postnatal visit → referral follow-up task created
    - Test offline birth record storage and sync
    - _Requirements: 15.3, 15.4, 15.6_

- [ ] 20. Implement Health Education Videos
  - [ ] 20.1 Add video library support to `frontend/src/components/Dashboard.js` or a new `VideoLibrary.js`
    - Display library of health education videos (handwashing, ORS preparation, malaria net use, safe childbirth, child nutrition)
    - Play locally cached version if available; stream if online
    - Display file size and estimated download time before initiating download
    - Block auto-play and auto-download when Low Bandwidth Mode is active
    - Display subtitles in user's language when device is in silent mode or subtitles are enabled
    - Enforce ≤360p / 400 kbps encoding and ≤200 MB total bundle size per language
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7_

  - [ ]* 20.2 Write unit tests for video library
    - Test cached video plays without network
    - Test Low Bandwidth Mode blocks auto-play
    - Test subtitle display in silent mode
    - _Requirements: 14.2, 14.5, 14.7_

- [ ] 21. Implement accessibility and Simple Mode
  - [ ] 21.1 Update `frontend/src/AccessibilityContext.js` and UI components
    - Add Simple_Mode toggle that replaces text-heavy screens with pictogram-first layouts and voice-guided navigation
    - Ensure pictograms alongside every navigation element, symptom option, urgency indicator, and action button
    - Add audio label on long-press for every interactive element
    - Enforce consistent colour coding: red = emergency, amber = visit health centre, green = self-care
    - Enforce minimum 48×48 dp touch targets on all interactive elements
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5, 18.6_

  - [ ]* 21.2 Write unit tests for accessibility features
    - Test Simple Mode activates pictogram-first layout
    - Test audio label plays on long-press
    - Test touch target size ≥48×48 dp
    - _Requirements: 18.2, 18.3, 18.6_

- [ ] 22. Implement power management and connectivity resilience
  - [ ] 22.1 Add auto-save and power-saving logic to relevant frontend components
    - Auto-save in-progress form state every 30 seconds to IndexedDB
    - Display connectivity status (online, offline, syncing) persistently in status bar
    - On reconnection, display summary of synced records and any sync errors
    - Enable power-saving mode (disable animations, suspend background sync) when battery < 15%
    - Support PWA installation on device home screen
    - Support session token persistence for up to 7 days without re-authentication
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 16.6_

  - [ ]* 22.2 Write unit tests for power and connectivity resilience
    - Test auto-save restores form state after app close
    - Test power-saving mode activates at 15% battery
    - Test session token valid for 7 days
    - _Requirements: 20.1, 16.6, 20.6_

- [ ] 23. Checkpoint — Ensure all feature tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 24. Wire all components into the main application
  - [ ] 24.1 Update `frontend/src/App.js`
    - Register all new routes: VoiceInterface, AudioTips, ImageSymptom, CommunityCalendar, ReferralTracker, EmergencyAlert, TBAModule, VideoLibrary
    - Wrap app with `BandwidthContext` and updated `AccessibilityContext`
    - Integrate `syncManager` startup on app load (register background sync, start connectivity listener)
    - _Requirements: 3.2, 9.1, 18.3_

  - [ ] 24.2 Update `backend/config/urls.py`
    - Include all new URL modules: `ussd_views`, `calendar_views`, `referral_views`, `language_views`, and any new view files for traditional medicine and emergency contacts
    - _Requirements: 2.1, 7.6, 11.1, 12.1, 13.1_

  - [ ] 24.3 Update `frontend/src/components/Dashboard.js`
    - Add navigation tiles for all new features with pictograms and audio labels
    - Display connectivity status bar and session data usage (when Low Bandwidth Mode active)
    - _Requirements: 9.7, 18.1, 20.3_

  - [ ]* 24.4 Write integration tests for end-to-end flows
    - Test complete voice symptom assessment → guidance → SMS send
    - Test offline data submission → reconnect → verify backend sync
    - Test emergency urgency → emergency alert → SMS to contacts
    - _Requirements: 1.8, 3.4, 11.3_

- [ ] 25. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at logical boundaries
- Property tests validate universal correctness properties (Properties 1–17 from the design)
- Unit tests validate specific examples and edge cases
- The TF.js skin classifier model (`/models/skin_classifier/model.json`) must be sourced or trained separately and bundled with the PWA before Task 9 can be completed
- Africa's Talking credentials must be configured in `backend/.env` before USSD/IVR tasks (Task 6) can be integration-tested
