# AI Prompt Guide: AI-Based Health Assistant for Rural Ethiopia

A ready-to-use collection of prompts organized by category. Copy, paste, and adapt as needed.

---

## 1. Research & Context

```
Summarize the healthcare access challenges in rural Ethiopia — infrastructure, workforce shortage, disease burden, and cultural barriers — with recent statistics and citations.
```

```
List existing digital health and mHealth initiatives in Ethiopia and similar low-resource settings. Include what worked, what failed, and why.
```

```
Provide a short literature review (5–10 papers) on AI chatbots used for rural health triage and health education in sub-Saharan Africa.
```

---

## 2. User & Needs Research

```
Design a rapid needs-assessment survey for rural Ethiopian communities to identify top health information needs, preferred languages and communication channels, and mobile phone access levels.
```

```
Create interview question guides for healthcare workers and community health volunteers about their experience and expectations for using an AI health assistant.
```

---

## 3. Product & System Design

```
Draft a system architecture for an AI-based health assistant that works offline-first (mobile/USSD/IVR) and syncs when connected. Include components, data flow, and minimal hardware requirements.
```

```
Propose a feature-priority roadmap (MVP to v2) for the first 12 months, focused on maximum health impact and low-cost deployment in rural Ethiopia.
```

```
List essential non-functional requirements — security, privacy, latency, offline capability — for deploying an AI health assistant in rural Ethiopia.
```

---

## 4. Conversational Design (Building the Assistant)

**System prompt for the assistant backend:**
```
You are a friendly, concise health assistant for rural Ethiopian users. Provide evidence-based, culturally sensitive health guidance in simple language. When unsure, advise the user to seek their nearest clinic or health worker. Never give prescriptions. Ask clarifying questions when necessary.
```

**Triage follow-up prompt:**
```
A user says: "I have fever and stomach pain for 3 days." Generate follow-up questions, list likely causes, provide immediate home-care advice, identify red flags requiring clinic or ambulance, and recommend the next step in the local Ethiopian health context.
```

**Health education prompt:**
```
Explain diarrhea prevention and home rehydration in simple Amharic and English. Include a step-by-step ORS (oral rehydration solution) recipe and clear guidance on when to seek care.
```

---

## 5. Data & Datasets

```
Recommend open datasets for Ethiopian health — disease prevalence, health facility locations, demographic surveys — and explain how to legally obtain them.
```

```
Create a data collection plan to gather labeled triage dialogues from community health workers. Include a consent script, privacy safeguards, and minimum required metadata fields.
```

```
Provide annotation guidelines for labeling user intents, symptoms, severity levels, and recommended actions in health conversation data.
```

---

## 6. Modeling & Algorithms

```
Suggest lightweight NLP model options suitable for on-device or edge deployment (quantized models, knowledge distillation) and explain the trade-offs between accuracy and model size.
```

```
Design a simple symptom-triage decision flow that combines rule-based checks with ML intent classification. Include a fallback policy for handling uncertainty safely.
```

```
Provide techniques for building NLP models in low-resource languages like Amharic — transfer learning, multilingual models, active learning — and best practices when labeled data is limited.
```

---

## 7. Evaluation & Monitoring

```
Give an evaluation plan and KPIs for piloting the assistant. Include: triage accuracy, recall of danger signs, user satisfaction score, referral uptake rate, and reduction in unnecessary clinic visits.
```

```
Create a field-testing protocol for a 3-month pilot. Include sample size calculation, key metrics, and a process for capturing and reporting safety incidents.
```

---

## 8. Deployment & Operations

```
Outline an affordable deployment stack for rural contexts: mobile app + SMS/USSD + IVR + central dashboard. Include a recommended approach for cloud hosting and offline data sync.
```

```
List local partnerships to consider — Ministry of Health regional offices, NGOs, telecom providers — and provide a short template outreach email for initiating contact.
```

---

## 9. Safety, Ethics & Privacy

```
Write a brief ethical framework for using AI in rural healthcare. Cover: informed consent, explainability, harm minimization, escalation to human care, and data minimization principles.
```

```
Provide a privacy checklist to ensure best-practice compliance when collecting personal health data in Ethiopia, referencing relevant local and international standards.
```

---

## 10. Localization & Community Engagement

```
Suggest steps and key phrases for translating and culturally adapting health guidance into Amharic, Oromo, Tigrinya, and Sidamo. Include community validation steps.
```

```
Design a community engagement plan to recruit and train community health volunteers to use and promote the AI health assistant in their villages.
```

---

## 11. Funding & Proposal Support

```
Draft a 1-page project concept note aimed at NGOs and impact funders. Include: objective, problem statement, approach, expected impact, and a rough budget estimate.
```

```
List common budget line items and rough cost estimates for a 12-month pilot covering: software development, devices, mobile data, field staff salaries, and training.
```

---

## 12. Technical Implementation

**Flask API starter:**
```
Generate Python starter code for a small Flask API that serves a symptom-triage model. Include endpoints for receiving user messages and logging interactions — no PII stored.
```

**Model quantization:**
```
Provide the shell commands and config to quantize a Hugging Face transformer model for edge deployment, with a short explanation of the accuracy vs. size trade-offs.
```

**Unit tests:**
```
Write a template for unit tests to verify triage logic and red-flag detection in a Python-based symptom assessment module.
```

---

## 13. Conversation Examples for Testing

```
Create 8 sample user queries with varying severity levels, dialect words, and low-literacy writing styles. For each, provide the expected assistant reply including safe escalation steps.
```

**Safe uncertainty response template:**
```
Write a short safe-response template the assistant should use when it is uncertain about a user's condition. Example format: "I'm not sure — please contact your nearest health worker or call [local emergency number]."
```

---

## 14. Training & Capacity Building

```
List a 2-day training agenda to teach community health workers how to use and troubleshoot the AI health assistant. Include role-play exercises and common Q&A scenarios.
```

---

## 15. Deliverables & Next Steps

```
Generate a prioritized 2-week plan to move from concept to a pilot-ready MVP. Include daily or weekly milestones, key decisions, and dependencies.
```

---

## How to Use These Prompts

1. Pick the category matching your current task.
2. Copy the prompt exactly or adapt it with your specific details (region, language, disease focus).
3. Paste it into your AI tool (ChatGPT, Claude, Gemini, Kiro, etc.).
4. Iterate — follow up with "go deeper on X" or "give me a more detailed version of Y."
5. Combine prompts — for example, use the system design prompt first, then the deployment prompt to build on the architecture.

---

*Prompts compiled for: AI-Based Health Assistant for Improving Healthcare Access in Rural Ethiopia*
