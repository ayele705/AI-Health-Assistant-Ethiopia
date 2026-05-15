# AI Health Assistant for Rural Ethiopia
## Simple Documentation Guide

**Version 1.0 | May 2026**

---

##  What is This Project?

This is a **mobile health app** that helps people in rural Ethiopia get health advice when they can't reach a doctor.

**Think of it like:**
- A health chatbot on your phone
- Works in Amharic and English
- Tells you if you need to see a doctor or can treat yourself at home
- Works even without internet

---

##  Why We Built This

### The Problem

**Ethiopia's Healthcare Crisis:**
- Only 1 doctor for every 10,000 people
- 80% of people live in rural areas far from clinics
- People walk for hours to see a doctor
- Many don't know when they need urgent care

**Example:**
> A mother in a rural village has a sick child with fever. She doesn't know if it's serious. The nearest clinic is 3 hours away on foot. Should she make the journey? This app helps her decide.

---

##  How It Works

### Simple 3-Step Process

**Step 1: User Reports Symptoms**
```
User: "My child has fever and cough for 2 days"
```

**Step 2: AI Analyzes**
- Extracts symptoms: fever, cough
- Checks against 30+ common diseases
- Calculates urgency level

**Step 3: App Gives Advice**
```
App: "This could be malaria or flu.
     🟡 MEDIUM URGENCY
     → Visit health center within 24 hours
     → Meanwhile: Rest, drink fluids, give paracetamol"
```

---

## ️ System Parts

### 1. Mobile App (What Users See)
- **Android app** - For smartphones
- **USSD menu** - For basic phones (dial *384*96#)
- **Chat interface** - Like WhatsApp
- **Voice input** - Speak your symptoms

### 2. AI Brain (Behind the Scenes)
- **Language processor** - Understands Amharic and English
- **Symptom checker** - Matches symptoms to diseases
- **Urgency calculator** - Decides if it's emergency, urgent, or can wait

### 3. Database (Stores Information)
- **User profiles** - Age, location, language
- **Health knowledge** - 30+ diseases, symptoms, treatments
- **Health facilities** - Nearest clinics and hospitals

### 4. Connections
- **DHIS2** - Reports to Ethiopia's health system
- **SMS gateway** - Sends appointment reminders
- **Maps** - Finds nearest health facility

---

##  What Can Users Do?

### Main Features

**1. Check Symptoms**
- Type or speak your symptoms
- Get list of possible conditions
- See urgency level (Low/Medium/High)
- Get advice on what to do next

**2. Learn About Health**
- Read articles about diseases
- Listen to audio (for people who can't read)
- Topics: malaria, diarrhea, pregnancy, nutrition, etc.

**3. Find Nearest Clinic**
- Shows health posts, health centers, hospitals nearby
- Shows distance and phone number
- Get directions

**4. Book Appointments**
- Schedule visit to health center
- Get SMS reminder before appointment

**5. Emergency Help**
- First aid instructions
- Emergency phone numbers
- Red flag symptoms that need immediate care

---

##  Urgency Levels Explained

### 🟢 LOW (Green) - Self-Care at Home
**Example:** Mild headache for 1 day
- **What to do:** Rest, drink water, take paracetamol
- **When to worry:** If it gets worse after 2 days

### 🟡 MEDIUM (Yellow) - Visit Health Center Soon
**Example:** Fever and body pain for 3 days
- **What to do:** Visit health center within 24-48 hours
- **Possible cause:** Malaria, typhoid, flu

###  HIGH (Red) - Emergency!
**Example:** Difficulty breathing, heavy bleeding, seizure
- **What to do:** Go to hospital IMMEDIATELY
- **Call:** Emergency number or ambulance

---

##  How Accurate Is It?

### Test Results

**AI Accuracy:**
-  **81% correct** when giving top 3 possible diseases
-  **67% correct** when giving top 1 disease
-  Best at common diseases (malaria, diarrhea, flu)

**User Testing (45 people tested it):**
-  **87%** could report symptoms and get advice
-  **91%** said they would use it again
-  **84%** were satisfied with the app
-  **96%** liked the Amharic language support

**What Users Said:**
> "This is very helpful. I don't have to walk 2 hours to ask simple questions." - Community member, Oromia

> "It helps me decide which patients need urgent referral." - Health Extension Worker

---

## ️ Technology Used

### Simple Explanation

**Frontend (What you see):**
- Android app built with Kotlin
- Simple chat interface
- Works offline

**Backend (The brain):**
- Python programming language
- Django framework (like WordPress but for apps)
- AI models from Hugging Face

**Database (Storage):**
- PostgreSQL - Stores user data
- MongoDB - Stores health knowledge
- SQLite - Stores data on phone for offline use

**AI Models:**
- **mBERT** - Understands Amharic and English
- **Random Forest** - Predicts diseases from symptoms
- Trained on 50,000 symptom examples

---

##  How to Use the App

### For Community Members

**First Time Setup:**
1. Download app from Play Store
2. Open app
3. Enter your name, age, location
4. Choose language (Amharic or English)
5. Done! Start chatting

**Checking Symptoms:**
1. Tap "Check Symptoms"
2. Type or speak your symptoms
3. Answer follow-up questions
4. Get results with advice
5. Find nearest clinic if needed

**Reading Health Tips:**
1. Tap "Health Education"
2. Choose topic (Malaria, Pregnancy, Nutrition, etc.)
3. Read or listen to audio
4. Save favorites

### For Health Extension Workers

**Using the Dashboard:**
1. Login with HEW account
2. See community health summary
3. View recent consultations
4. Check referral queue
5. Generate reports

---

##  Privacy & Safety

### Your Data is Protected

**What We Collect:**
- Your name, age, location (to find nearest clinic)
- Symptoms you report
- Consultation history

**What We DON'T Collect:**
- No photos or videos
- No financial information
- No social media data

**How We Protect It:**
- All data encrypted (scrambled so hackers can't read it)
- Stored on servers in Ethiopia (not sent abroad)
- Deleted after 90 days
- You can delete your account anytime

### Important Disclaimer

️ **THIS APP DOES NOT REPLACE A DOCTOR**

- It gives information and advice only
- It does NOT diagnose diseases
- It does NOT prescribe medicine
- Always see a real doctor for serious problems

---

## ️ What This App CANNOT Do

### Limitations

**1. Language**
- Only Amharic and English now
- Oromo, Tigrinya, Somali coming in version 2

**2. Internet**
- Some features need internet
- Offline mode has limited features

**3. Rare Diseases**
- Only covers 30 common diseases
- Rare conditions not included

**4. Voice Recognition**
- Works poorly in noisy places
- Better indoors than outdoors

**5. Not Clinically Certified**
- Not tested in official medical trials yet
- Use as information tool, not medical device

---

##  Future Plans

### Version 2.0 (Coming 2027)

**New Languages:**
- Oromo
- Tigrinya
- Somali
- Sidama

**New Features:**
- Video call with doctor (telemedicine)
- Connect to blood pressure monitor
- Better voice recognition
- More diseases covered

**Bigger Reach:**
- Start with 5 villages (200 users)
- Expand to 50 villages (2,000 users)
- Then whole region (20,000 users)
- Finally nationwide (200,000+ users)

---

##  Need Help?

### For Users

**Technical Problems:**
- Call: +251-XXX-XXXX
- Email: support@healthassistant.et
- Visit: Nearest health post

**Medical Emergencies:**
- Call: 907 (Ambulance)
- Go to nearest hospital immediately
- Don't wait for app advice

### For Developers

**Code Repository:**
- GitHub: github.com/your-org/health-assistant

**Documentation:**
- API Docs: api.healthassistant.et/docs
- Developer Guide: docs.healthassistant.et

---

##  Quick Reference

### Common Questions

**Q: Is it free?**
A: Yes, completely free for users.

**Q: Do I need internet?**
A: Basic features work offline. Full features need internet.

**Q: Can I use it for my child?**
A: Yes, enter child's age when reporting symptoms.

**Q: What if I don't have a smartphone?**
A: Dial *384*96# on any phone (USSD menu).

**Q: Is my data private?**
A: Yes, encrypted and stored securely in Ethiopia.

**Q: Can it diagnose diseases?**
A: No, it gives information only. See a doctor for diagnosis.

**Q: What languages are supported?**
A: Amharic and English now. More coming soon.

**Q: How accurate is it?**
A: 81% accurate for top-3 predictions. Best for common diseases.

---

##  Glossary (Simple Terms)

**AI (Artificial Intelligence)** - Computer that can think and learn like humans

**API** - Way for apps to talk to each other

**Backend** - The part of the system users don't see (the brain)

**Database** - Digital filing cabinet that stores information

**Frontend** - The part users see and touch (the app screen)

**HEW** - Health Extension Worker (community health agent)

**mBERT** - AI model that understands many languages

**NLP** - Natural Language Processing (teaching computers to understand human language)

**Offline Mode** - App works without internet

**USSD** - Menu you see when you dial codes like *384*96#

**Symptom** - Sign that you're sick (fever, cough, pain, etc.)

**Triage** - Deciding who needs urgent care first

**Urgency Level** - How quickly you need to see a doctor

---

##  Quick Start Checklist

### For New Users

- [ ] Download app from Play Store
- [ ] Register with name, age, location
- [ ] Choose language (Amharic or English)
- [ ] Try checking symptoms
- [ ] Read one health education article
- [ ] Find nearest health facility
- [ ] Save emergency numbers

### For Developers

- [ ] Install Docker
- [ ] Clone GitHub repository
- [ ] Copy .env.example to .env
- [ ] Edit .env with your settings
- [ ] Run `docker-compose up`
- [ ] Run migrations
- [ ] Load sample data
- [ ] Create admin user
- [ ] Test API endpoints
- [ ] Read API documentation

---

##  Project Status

**Current Version:** 1.0 (Prototype)

**What's Working:**
-  Symptom checker
-  Health education
-  Facility finder
-  Offline mode
-  Amharic & English support

**What's Coming:**
- ⏳ More languages
- ⏳ Telemedicine
- ⏳ Better voice recognition
- ⏳ More diseases covered

**Testing Status:**
-  Tested with 45 users
-  96.3% of code tests passing
-  Ready for pilot deployment

---

##  Academic Information

**Course:** AI Course  
**Academic Year:** 2026  
**Institution:** [Your University]  
**Project Type:** Final Year Project

**Team:**
- Project Lead: [Name]
- AI Engineer: [Name]
- Backend Developer: [Name]
- Mobile Developer: [Name]
- Health Advisor: [Name]

**Supervisor:** [Professor Name]

---

##  License

This project is open source under MIT License.

**What this means:**
- Anyone can use it for free
- Anyone can modify it
- Anyone can contribute improvements
- Must give credit to original creators

---

##  Thank You

**Special Thanks To:**
- Ethiopian Ministry of Health
- Health Extension Workers who tested the app
- Community members in Oromia who gave feedback
- WHO Ethiopia Office
- [Your University] AI Department

---

**Last Updated:** May 2026  
**Document Version:** 1.0  
**For Questions:** health-assistant@example.com

---

*Made with ️ for rural Ethiopia*
