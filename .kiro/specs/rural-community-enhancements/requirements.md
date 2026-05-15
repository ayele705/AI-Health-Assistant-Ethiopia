# Requirements Document

## Introduction

This document defines requirements for enhancing the AI Health Assistant to better serve rural Ethiopian communities. The existing system provides symptom assessment, facility finding, medication lookup, growth monitoring, vaccination tracking, pregnancy follow-up, SMS reminders, and an analytics dashboard with multilingual support (English, Amharic, Oromo, Tigrinya, Sidama).

The enhancements target eight critical rural challenges: intermittent connectivity, low literacy, shared/feature-phone device access, limited local language coverage, low community trust, expensive mobile data, unreliable electricity, and the need to integrate traditional medicine knowledge. Improvements are grouped into three priority tiers — Critical, High, and Medium — and span voice interaction, USSD/IVR access, aggressive offline operation, community health worker tooling, image-based symptom reporting, traditional medicine integration, emergency alerting, and health education.

The system is not a clinical diagnostic tool. It serves as a first-contact health information bridge and decision-support resource for community members, Health Extension Workers (HEWs), and traditional practitioners.

---

## Glossary

- **Health_Assistant**: The AI-based health guidance system (Django backend + React PWA frontend).
- **Voice_Interface**: The speech-to-text and text-to-speech subsystem enabling voice-based interaction.
- **USSD_IVR_Gateway**: The Unstructured Supplementary Service Data / Interactive Voice Response integration layer (Africa's Talking or Twilio) enabling feature-phone access.
- **Offline_Engine**: The service-worker and IndexedDB subsystem that stores data locally and synchronises when connectivity is restored.
- **Sync_Manager**: The background-sync component responsible for queuing and replaying offline actions when connectivity is available.
- **P2P_Sync**: The WebRTC-based peer-to-peer data exchange mechanism between nearby devices.
- **Audio_Content_Store**: The local cache of pre-recorded audio health tips in supported languages.
- **CHW_Dashboard**: The Community Health Worker offline-capable data-collection and patient-management interface.
- **Image_Analyser**: The on-device TensorFlow Lite model that classifies wound, rash, and skin-condition images.
- **Traditional_Medicine_KB**: The curated knowledge base of Ethiopian traditional remedies, interactions, and safety notes.
- **Language_Pack**: A downloadable bundle containing UI strings, audio clips, and IVR prompts for one language/dialect.
- **Emergency_Alert_Engine**: The component that detects danger-level urgency and triggers multi-contact notification.
- **Referral_Tracker**: The module that records, monitors, and follows up on patient referrals to higher-level facilities.
- **Community_Calendar**: The shared schedule of vaccination days, health worker visits, and community health events.
- **HEW**: Health Extension Worker — a community-level frontline health agent.
- **TBA**: Traditional Birth Attendant.
- **PWA**: Progressive Web App — a web application installable on a device home screen with offline capability.
- **IndexedDB**: Browser-native structured storage used for offline data persistence.
- **Service_Worker**: A browser script that intercepts network requests and manages caching for offline use.
- **Low_Bandwidth_Mode**: A UI mode that disables images, reduces payload sizes, and compresses responses.
- **Urgency_Level**: A classification of health condition severity: `self_care`, `visit_health_center`, or `emergency`.
- **Kebele**: The smallest administrative unit in Ethiopia, roughly equivalent to a village or ward.
- **DHIS2**: District Health Information Software 2 — the national health data reporting platform used in Ethiopia.

---

## Requirements

---

### Requirement 1: Voice-Based Interaction

**User Story:** As a rural community member who cannot read or write, I want to speak my symptoms and hear the health guidance spoken back to me, so that I can use the Health_Assistant without literacy skills.

#### Acceptance Criteria

1. WHEN a user activates the voice input button, THE Voice_Interface SHALL capture audio using the device microphone and convert it to text using the Web Speech API within 5 seconds of the user finishing speech.
2. WHEN speech-to-text transcription produces a result, THE Voice_Interface SHALL display the transcribed text and read it back to the user using text-to-speech before submitting it to the Health_Assistant.
3. WHEN the Health_Assistant produces a response, THE Voice_Interface SHALL read the response aloud in the user's selected language using text-to-speech at a speaking rate appropriate for comprehension.
4. WHEN the selected language is Amharic, Oromo, Tigrinya, or Sidama, THE Voice_Interface SHALL use a Language_Pack audio fallback if the Web Speech API does not support that language natively.
5. IF speech recognition fails or returns an empty result, THEN THE Voice_Interface SHALL prompt the user to speak again and offer a pictogram-based fallback input method.
6. WHILE voice mode is active, THE Voice_Interface SHALL suppress all non-essential UI animations and reduce screen brightness prompts to conserve battery.
7. THE Voice_Interface SHALL support a minimum of five languages: English, Amharic, Oromo, Tigrinya, and Sidama.
8. WHEN a user completes a voice-based symptom assessment, THE Health_Assistant SHALL offer to send the result as an SMS to a registered phone number.

---

### Requirement 2: USSD and IVR Feature-Phone Access

**User Story:** As a rural community member who owns only a basic feature phone, I want to access health guidance by dialling a short code or calling a number, so that I can receive health support without a smartphone or internet connection.

#### Acceptance Criteria

1. THE USSD_IVR_Gateway SHALL accept inbound USSD sessions initiated by dialling a registered short code and present a language-selection menu within 3 seconds.
2. WHEN a user selects a language, THE USSD_IVR_Gateway SHALL present a symptom-selection menu using numbered options corresponding to the five most common presenting complaints: fever, cough, stomach pain, difficulty breathing, and other.
3. WHEN a user completes the USSD symptom flow, THE USSD_IVR_Gateway SHALL return a plain-text health guidance message of no more than 160 characters per USSD screen page.
4. THE USSD_IVR_Gateway SHALL support IVR call-in access where spoken prompts guide the user through the same symptom flow using keypad input.
5. WHEN the IVR flow determines an Urgency_Level of `emergency`, THE USSD_IVR_Gateway SHALL speak the emergency message and provide the phone number of the nearest health facility before ending the session.
6. IF a USSD session times out before completion, THEN THE USSD_IVR_Gateway SHALL send an SMS summary of the last completed step to the caller's number.
7. THE USSD_IVR_Gateway SHALL log all sessions with anonymised identifiers for analytics without storing personally identifiable information.
8. WHEN a user requests it during an IVR session, THE USSD_IVR_Gateway SHALL send the full guidance result as an SMS to the caller's number at zero additional cost to the user where operator agreements permit.

---

### Requirement 3: Aggressive Offline Mode with Background Sync

**User Story:** As a rural community member in an area with no internet, I want the Health_Assistant to work fully offline and automatically sync my data when connectivity returns, so that I never lose health records or guidance due to poor network conditions.

#### Acceptance Criteria

1. THE Offline_Engine SHALL cache all core application assets, the symptom knowledge base, facility data, medication data, and Language_Packs during the first successful online session so that the Health_Assistant is fully functional without any network connection thereafter.
2. WHEN the device has no network connectivity, THE Health_Assistant SHALL display a clear offline status indicator and continue to allow symptom assessment, facility lookup, medication lookup, growth monitoring, vaccination tracking, and pregnancy follow-up using cached data.
3. WHEN a user submits data (consultation, growth measurement, vaccination record, referral) while offline, THE Sync_Manager SHALL store the submission in IndexedDB with a timestamp and a `pending_sync` status.
4. WHEN network connectivity is restored, THE Sync_Manager SHALL automatically upload all `pending_sync` records to the backend within 60 seconds without requiring user action.
5. IF a sync upload fails due to a server error, THEN THE Sync_Manager SHALL retry with exponential backoff up to five attempts before marking the record as `sync_failed` and notifying the user.
6. THE Offline_Engine SHALL store a minimum of 90 days of patient records per device in IndexedDB without exceeding 50 MB of storage.
7. WHEN cached data is more than 30 days old and connectivity is available, THE Offline_Engine SHALL silently refresh the knowledge base, facility list, and medication data in the background.
8. THE Service_Worker SHALL intercept all API requests and serve cached responses when the network is unavailable, falling back to a pre-cached offline error page only for requests with no cached equivalent.

---

### Requirement 4: Audio Health Tips in Local Languages

**User Story:** As a rural community member who cannot read, I want to hear health education tips spoken in my language, so that I can learn about disease prevention and healthy practices without needing literacy.

#### Acceptance Criteria

1. THE Audio_Content_Store SHALL contain pre-recorded audio health tips covering at minimum the following categories: malaria prevention, diarrhoea prevention, maternal health, child nutrition, vaccination importance, and hand hygiene — in all five supported languages.
2. WHEN a user opens the health tips section, THE Health_Assistant SHALL display each tip with a pictogram, a short text label, and a play button that streams or plays the locally cached audio clip.
3. WHEN a user taps the play button for a tip, THE Audio_Content_Store SHALL play the audio clip within 1 second if cached locally, or begin streaming within 3 seconds if connectivity is available.
4. WHEN the device is offline, THE Audio_Content_Store SHALL play only tips that are already cached and SHALL indicate which tips require connectivity to download.
5. THE Health_Assistant SHALL allow users to download all audio tips for their selected language as a single Language_Pack bundle while connected, for later offline playback.
6. WHERE a user has enabled Low_Bandwidth_Mode, THE Health_Assistant SHALL not auto-download audio content and SHALL require explicit user action to initiate any audio download.
7. THE Audio_Content_Store SHALL support audio files encoded at a maximum of 32 kbps to minimise data usage and storage requirements.

---

### Requirement 5: Community Health Worker Offline Dashboard

**User Story:** As a Health Extension Worker operating in a remote kebele without internet, I want to collect patient data, run assessments, and manage my caseload offline, so that I can serve my community and sync records when I reach connectivity.

#### Acceptance Criteria

1. THE CHW_Dashboard SHALL be accessible via a PIN-protected login that works without network connectivity using locally stored credentials.
2. WHEN a CHW creates a new patient record offline, THE CHW_Dashboard SHALL store the record in IndexedDB and assign a locally generated UUID that is preserved when the record syncs to the server.
3. THE CHW_Dashboard SHALL support offline data entry for: patient registration, symptom assessment, growth measurements, vaccination records, pregnancy follow-up visits, and referral creation.
4. WHEN a CHW completes a patient assessment offline, THE CHW_Dashboard SHALL generate a printable or SMS-shareable summary using the patient's local language.
5. THE CHW_Dashboard SHALL display a caseload view showing all patients assigned to the CHW, their last visit date, and any overdue follow-ups, using only locally cached data when offline.
6. WHEN connectivity is restored, THE Sync_Manager SHALL sync all CHW_Dashboard records to the backend and resolve conflicts using a last-write-wins strategy with a conflict log visible to the CHW.
7. THE CHW_Dashboard SHALL include a checklist module aligned with the Ethiopian HEW standard visit protocol, allowing CHWs to record visit outcomes against each checklist item.
8. IF a patient assessment produces an Urgency_Level of `emergency`, THEN THE CHW_Dashboard SHALL display a prominent alert and provide the CHW with the nearest referral facility contact details from cached data.

---

### Requirement 6: Image-Based Symptom Reporting

**User Story:** As a rural community member or CHW, I want to photograph a wound, rash, or skin condition and have the Health_Assistant analyse it, so that I can get guidance without needing to describe the condition in words.

#### Acceptance Criteria

1. WHEN a user selects the image symptom input option, THE Health_Assistant SHALL activate the device camera or allow selection from the device gallery.
2. WHEN an image is captured or selected, THE Image_Analyser SHALL run an on-device TensorFlow Lite classification model to identify the condition category (wound, rash, skin infection, eye condition, or other) within 10 seconds without requiring network connectivity.
3. WHEN the Image_Analyser produces a classification result, THE Health_Assistant SHALL display the identified condition category with a confidence indicator and combine it with any verbally or textually reported symptoms before generating guidance.
4. IF the Image_Analyser confidence score is below 60%, THEN THE Health_Assistant SHALL inform the user that the image is unclear, suggest retaking the photo in better lighting, and offer the option to describe the condition using voice or pictograms instead.
5. THE Health_Assistant SHALL not transmit patient images to the backend server without explicit informed consent from the user, presented in the user's selected language.
6. WHERE a user has granted consent for image upload, THE Health_Assistant SHALL compress images to a maximum of 200 KB before transmission to minimise data usage.
7. THE Image_Analyser model SHALL be bundled with the PWA installation and SHALL not require a network connection to perform classification.
8. WHEN an image analysis is completed, THE Health_Assistant SHALL store the image locally in encrypted form and SHALL delete it automatically after 30 days unless the user explicitly saves it to their health record.

---

### Requirement 7: Traditional Medicine Knowledge Base Integration

**User Story:** As a rural community member who uses traditional remedies, I want the Health_Assistant to acknowledge traditional treatments and advise me on their safety alongside modern guidance, so that I can make informed decisions that respect my cultural practices.

#### Acceptance Criteria

1. THE Traditional_Medicine_KB SHALL contain entries for at minimum 50 commonly used Ethiopian traditional remedies, each including: local name in at least two Ethiopian languages, common use, known active compounds where documented, known safety concerns, and known interactions with common medications.
2. WHEN a user reports using a traditional remedy during a symptom assessment, THE Health_Assistant SHALL look up the remedy in the Traditional_Medicine_KB and include any relevant safety notes or interaction warnings in the guidance response.
3. WHEN the Traditional_Medicine_KB contains a documented interaction between a reported traditional remedy and a medication in the user's medication list, THE Health_Assistant SHALL display a clearly labelled interaction warning before presenting other guidance.
4. THE Health_Assistant SHALL present traditional medicine information in a culturally respectful tone that acknowledges the value of traditional practices while clearly distinguishing between documented evidence and unverified claims.
5. WHERE a user is a registered TBA, THE Health_Assistant SHALL provide an extended Traditional_Medicine_KB view that includes birth-related traditional practices and their evidence-based safety assessments.
6. THE Traditional_Medicine_KB SHALL be updatable by authorised health administrators without requiring a full application deployment.
7. IF a traditional remedy in the Traditional_Medicine_KB is associated with a known serious adverse effect, THEN THE Health_Assistant SHALL display a prominent safety warning and recommend consulting a health worker before use.

---

### Requirement 8: Local Language Expansion

**User Story:** As a rural community member whose primary language is not currently supported, I want to interact with the Health_Assistant in my own language or dialect, so that I can understand health guidance without relying on translation.

#### Acceptance Criteria

1. THE Health_Assistant SHALL support a minimum of eight Ethiopian languages at launch of this feature, adding Somali, Afar, Wolaytta, and Hadiyya to the existing five (English, Amharic, Oromo, Tigrinya, Sidama).
2. WHEN a new Language_Pack is added, THE Health_Assistant SHALL include: all UI strings, IVR_MENUS prompts, SAFE_MESSAGES, symptom names, urgency messages, and at least 20 audio health tips in that language.
3. THE Health_Assistant SHALL allow users to download a Language_Pack for offline use while connected, and SHALL display the download size before initiating the download.
4. WHEN a user selects a language for which a Language_Pack is not yet downloaded, THE Health_Assistant SHALL fall back to Amharic for audio content and English for text content, and SHALL prompt the user to download the Language_Pack.
5. THE Health_Assistant SHALL display a language selector on the home screen that is accessible without reading, using flag icons and audio pronunciation of each language name.
6. WHERE a Language_Pack includes dialect variants, THE Health_Assistant SHALL allow the user to select the specific dialect after selecting the base language.

---

### Requirement 9: Low-Bandwidth Mode

**User Story:** As a rural community member with expensive or slow mobile data, I want a mode that minimises data usage, so that I can use the Health_Assistant without incurring unaffordable data costs.

#### Acceptance Criteria

1. THE Health_Assistant SHALL provide a Low_Bandwidth_Mode toggle accessible from the main settings screen.
2. WHILE Low_Bandwidth_Mode is active, THE Health_Assistant SHALL disable all image loading, video loading, and auto-play audio, and SHALL compress all API request and response payloads to plain text or minimal JSON.
3. WHILE Low_Bandwidth_Mode is active, THE Health_Assistant SHALL display a data usage estimate for each action that requires network access before the action is performed.
4. WHILE Low_Bandwidth_Mode is active, THE Health_Assistant SHALL limit each API response payload to a maximum of 2 KB.
5. THE Health_Assistant SHALL automatically suggest enabling Low_Bandwidth_Mode when it detects a network connection speed below 50 kbps.
6. WHEN Low_Bandwidth_Mode is enabled, THE Health_Assistant SHALL cache all responses from the current session in IndexedDB so that the user can review them without additional data cost.
7. THE Health_Assistant SHALL display the total data consumed in the current session in the status bar when Low_Bandwidth_Mode is active.

---

### Requirement 10: Peer-to-Peer Data Sync

**User Story:** As a CHW who meets other CHWs in the field without internet access, I want to sync patient records and knowledge base updates between our devices directly, so that we can share the latest data without needing connectivity.

#### Acceptance Criteria

1. THE P2P_Sync component SHALL allow two devices running the Health_Assistant to establish a direct WebRTC data channel when both are on the same local Wi-Fi network or within Bluetooth range.
2. WHEN a P2P_Sync session is initiated, THE P2P_Sync component SHALL display a pairing code on the initiating device that the receiving device must enter to confirm the connection.
3. WHEN a P2P_Sync session is established, THE P2P_Sync component SHALL synchronise: pending patient records, updated knowledge base entries, and new Language_Pack bundles between the two devices.
4. THE P2P_Sync component SHALL encrypt all data transmitted during a P2P_Sync session using AES-256 encryption.
5. IF a conflict is detected between records on the two devices during P2P_Sync, THEN THE P2P_Sync component SHALL present both versions to the user and require explicit selection of the correct version before completing the sync.
6. WHEN a P2P_Sync session completes, THE P2P_Sync component SHALL display a summary of records transferred, updated, and skipped.
7. THE P2P_Sync component SHALL not transmit any data to external servers during a P2P_Sync session; all data exchange SHALL be device-to-device only.

---

### Requirement 11: Emergency Contact Tree

**User Story:** As a rural community member whose health assessment indicates a danger-level condition, I want the Health_Assistant to automatically notify my family members and the nearest CHW, so that I can receive help even if I am unable to seek it myself.

#### Acceptance Criteria

1. THE Health_Assistant SHALL allow users to register up to five emergency contacts, each with a name, phone number, and relationship, stored locally and synced to the backend when online.
2. WHEN a symptom assessment produces an Urgency_Level of `emergency`, THE Emergency_Alert_Engine SHALL display a prominent alert and offer to notify all registered emergency contacts via SMS.
3. WHEN the user confirms emergency notification, THE Emergency_Alert_Engine SHALL send an SMS to each registered contact within 30 seconds containing: the user's name, the assessed condition summary, and the GPS coordinates or nearest named location of the user.
4. IF the device has no network connectivity when an emergency is detected, THEN THE Emergency_Alert_Engine SHALL queue the SMS notifications and send them automatically within 60 seconds of connectivity being restored.
5. THE Emergency_Alert_Engine SHALL include the phone number and distance of the nearest health facility in every emergency SMS notification.
6. WHEN an emergency alert is sent, THE Emergency_Alert_Engine SHALL log the event with a timestamp in the user's local health record.
7. THE Health_Assistant SHALL allow users to cancel a pending emergency notification within a 10-second countdown window before the SMS is sent.

---

### Requirement 12: Community Health Calendar

**User Story:** As a community member or CHW, I want to see a shared calendar of upcoming vaccination days, health worker visits, and community health events in my kebele, so that I can plan attendance and remind community members.

#### Acceptance Criteria

1. THE Community_Calendar SHALL display upcoming health events for the user's registered kebele, including: vaccination days, CHW visit schedules, antenatal care clinic days, and community health education sessions.
2. WHEN a user views the Community_Calendar, THE Health_Assistant SHALL show events for the next 90 days using only locally cached data when offline.
3. WHEN a new event is added to the Community_Calendar by an authorised CHW or health administrator, THE Sync_Manager SHALL push the update to all registered devices in the affected kebele within 24 hours when connectivity is available.
4. THE Community_Calendar SHALL allow users to set personal reminders for any event, delivered as an SMS or an in-app notification 24 hours before the event.
5. WHEN a user registers a child for vaccination tracking, THE Health_Assistant SHALL automatically add the child's upcoming vaccination due dates to the Community_Calendar.
6. THE Community_Calendar SHALL display events in the user's selected language and SHALL use pictograms alongside text labels for all event types.

---

### Requirement 13: Referral Tracking

**User Story:** As a CHW who refers patients to higher-level facilities, I want to track whether referred patients attended their appointments and what the outcome was, so that I can follow up on patients who did not attend and improve continuity of care.

#### Acceptance Criteria

1. WHEN a CHW creates a referral for a patient, THE Referral_Tracker SHALL record: patient identifier, referring CHW, destination facility, referral reason, referral date, and expected visit date.
2. THE Referral_Tracker SHALL display a list of all open referrals for the CHW's caseload, sorted by expected visit date, accessible offline using cached data.
3. WHEN the expected visit date of a referral passes without a recorded outcome, THE Referral_Tracker SHALL generate a follow-up task for the CHW and display it prominently in the CHW_Dashboard.
4. WHEN a CHW records a referral outcome (attended, not attended, admitted, discharged), THE Referral_Tracker SHALL update the referral status and sync the outcome to the backend when connectivity is available.
5. IF a patient does not attend a referral within 3 days of the expected visit date, THEN THE Referral_Tracker SHALL send an SMS reminder to the patient's registered phone number if one is available.
6. THE Referral_Tracker SHALL generate a monthly summary report for each CHW showing: total referrals made, attendance rate, and most common referral reasons, viewable offline.

---

### Requirement 14: Health Education Videos

**User Story:** As a rural community member, I want to watch short health education videos in my language, so that I can learn about health topics in an engaging and accessible format even without reading skills.

#### Acceptance Criteria

1. THE Health_Assistant SHALL provide a library of health education videos covering at minimum: handwashing technique, oral rehydration solution preparation, malaria net use, safe childbirth practices, and child nutrition.
2. WHEN a user selects a video, THE Health_Assistant SHALL play a locally cached version if available, or stream the video if connectivity is available.
3. THE Health_Assistant SHALL encode all videos at a maximum resolution of 360p and a maximum bitrate of 400 kbps to minimise storage and data requirements.
4. WHEN a user downloads a video for offline viewing, THE Health_Assistant SHALL display the file size and estimated download time before initiating the download.
5. WHERE Low_Bandwidth_Mode is active, THE Health_Assistant SHALL not auto-play or auto-download any video content.
6. THE Health_Assistant SHALL allow users to download all videos for their selected language as a single bundle, with a total bundle size not exceeding 200 MB.
7. WHEN a video is played, THE Health_Assistant SHALL display subtitles in the user's selected language if the device is in silent mode or if the user has enabled subtitles in accessibility settings.

---

### Requirement 15: Traditional Birth Attendant Integration

**User Story:** As a Traditional Birth Attendant, I want access to safe delivery checklists, danger sign recognition guidance, and referral tools in my language, so that I can improve birth outcomes and know when to refer mothers to a health facility.

#### Acceptance Criteria

1. THE Health_Assistant SHALL provide a TBA-specific module accessible after role-based registration, containing: a safe delivery checklist, a danger signs recognition guide, a newborn care checklist, and a postnatal follow-up schedule.
2. WHEN a TBA records a birth event, THE Health_Assistant SHALL prompt for: delivery date, birth weight if available, delivery complications, and whether the mother and newborn were referred.
3. THE TBA module SHALL be fully functional offline, storing all birth records in IndexedDB and syncing to the backend when connectivity is available.
4. WHEN a TBA identifies a danger sign during delivery (heavy bleeding, prolonged labour, convulsions, or absent foetal movement), THE Emergency_Alert_Engine SHALL activate and offer to notify the nearest health facility and the mother's emergency contacts.
5. THE TBA module SHALL display all checklists and guidance using pictograms alongside text, with audio narration available in the TBA's selected language.
6. WHEN a TBA completes a postnatal visit record, THE Referral_Tracker SHALL automatically create a follow-up task for the next recommended postnatal visit date.

---

## Non-Functional Requirements

### Requirement 16: Performance in Low-Resource Environments

**User Story:** As a rural community member using an entry-level Android device, I want the Health_Assistant to load and respond quickly, so that I am not frustrated by slow performance on my device.

#### Acceptance Criteria

1. THE Health_Assistant SHALL achieve an initial load time of under 5 seconds on a device with 1 GB RAM and a 3G connection (minimum 1 Mbps).
2. THE Health_Assistant SHALL achieve an initial load time of under 3 seconds when loaded from the PWA cache with no network connection.
3. WHEN a user submits a symptom assessment, THE Health_Assistant SHALL display a guidance result within 2 seconds when operating offline using cached data.
4. THE Health_Assistant SHALL not consume more than 100 MB of device RAM during normal operation.
5. THE Health_Assistant SHALL not consume more than 150 MB of device storage for the base installation including the core knowledge base and one Language_Pack.
6. WHILE the device battery level is below 15%, THE Health_Assistant SHALL automatically enable a power-saving mode that disables animations, reduces screen brightness prompts, and suspends background sync.

---

### Requirement 17: Data Privacy and Security

**User Story:** As a rural community member, I want my health data to be kept private and secure, so that sensitive information about my health is not accessible to unauthorised parties.

#### Acceptance Criteria

1. THE Health_Assistant SHALL encrypt all patient data stored in IndexedDB using AES-256 encryption with a key derived from the user's PIN.
2. THE Health_Assistant SHALL transmit all data to the backend over HTTPS with TLS 1.2 or higher.
3. WHEN a user registers, THE Health_Assistant SHALL present an informed consent screen in the user's selected language explaining what data is collected, how it is used, and how to withdraw consent.
4. THE Health_Assistant SHALL allow users to delete all locally stored personal data from the device at any time from the settings screen.
5. THE Health_Assistant SHALL not share any personally identifiable information with third parties without explicit user consent.
6. IF a device is shared between multiple users, THEN THE Health_Assistant SHALL require PIN authentication before displaying any patient records and SHALL support separate PIN-protected profiles for up to five users per device.

---

### Requirement 18: Accessibility for Low-Literacy Users

**User Story:** As a rural community member with limited literacy, I want the Health_Assistant interface to be understandable without reading, so that I can navigate and use all features independently.

#### Acceptance Criteria

1. THE Health_Assistant SHALL display a pictogram alongside every navigation element, symptom option, urgency indicator, and action button.
2. THE Health_Assistant SHALL provide an audio label for every interactive element that plays when the element is long-pressed.
3. THE Health_Assistant SHALL support a Simple_Mode that replaces all text-heavy screens with pictogram-first layouts and voice-guided navigation.
4. WHEN Simple_Mode is active, THE Health_Assistant SHALL guide the user through each step of a symptom assessment using spoken prompts and pictogram selection, requiring no text input.
5. THE Health_Assistant SHALL use colour coding consistently: red for emergency, amber for visit health centre, green for self-care — across all urgency indicators.
6. THE Health_Assistant SHALL support a minimum touch target size of 48×48 dp for all interactive elements to accommodate users with limited fine motor control.

---

### Requirement 19: Cultural Sensitivity

**User Story:** As a rural Ethiopian community member, I want the Health_Assistant to communicate in a way that respects my cultural values and community structures, so that I trust the guidance it provides.

#### Acceptance Criteria

1. THE Health_Assistant SHALL present all health guidance in a tone that acknowledges community and family decision-making structures, using inclusive language that addresses both the individual and their family or community.
2. THE Health_Assistant SHALL not present guidance that contradicts or dismisses traditional practices without first acknowledging the practice respectfully and explaining the evidence-based concern.
3. WHEN a user reports a traditional remedy, THE Health_Assistant SHALL respond with a culturally respectful acknowledgement before presenting any safety information.
4. THE Health_Assistant SHALL allow CHWs and health administrators to flag guidance content for cultural review and to submit suggested culturally appropriate alternatives through the CHW_Dashboard.
5. THE Health_Assistant SHALL use locally relevant examples, seasonal references, and community-level health events in health education content where applicable.

---

### Requirement 20: Connectivity Resilience and Power Management

**User Story:** As a rural community member in an area with unreliable electricity and intermittent connectivity, I want the Health_Assistant to handle power interruptions and connectivity drops gracefully, so that I do not lose data or progress.

#### Acceptance Criteria

1. THE Health_Assistant SHALL auto-save the state of any in-progress symptom assessment, form, or data entry every 30 seconds to IndexedDB so that progress is not lost if the app is closed or the device loses power.
2. WHEN the Health_Assistant detects that connectivity has been lost during a data submission, THE Sync_Manager SHALL save the submission locally and display a notification confirming that the data has been saved and will sync automatically.
3. THE Health_Assistant SHALL display the current connectivity status (online, offline, syncing) persistently in the status bar.
4. WHEN the device reconnects after an offline period, THE Health_Assistant SHALL display a summary of records that were synced and any sync errors that require user attention.
5. THE Health_Assistant SHALL support installation as a PWA on the device home screen so that it can be launched without a browser and without an internet connection.
6. THE Health_Assistant SHALL function correctly after a device restart without requiring re-authentication for up to 7 days, using a locally stored session token.
