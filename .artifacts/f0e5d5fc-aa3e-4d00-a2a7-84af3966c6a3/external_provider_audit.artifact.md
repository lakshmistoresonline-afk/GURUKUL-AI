# External Provider Audit & User Actions Required

Gurukul AI is designed as an aggregator of national and open educational resources. This audit identifies the current integration status and the steps required by the project owner to fully enable these features.

## 1. Provider Audit Matrix

| Provider | Type | Status | API/Access | License |
| :--- | :--- | :--- | :--- | :--- |
| **Local Repo** | Internal | ✅ ACTIVE | N/A | Proprietary/Original |
| **NCERT ePathshala**| External | ⚠️ STUBBED | Web Scraping/OER | CC BY-NC-SA |
| **DIKSHA** | National | ⚠️ AUTH REQ | Sunbird API | Platform Terms |
| **GeoGebra** | Tool | ✅ VERIFIED | IFrame/HTML5 | OER |
| **PhET** | Simulation | ✅ VERIFIED | HTML5 | CC BY 4.0 |
| **Khan Academy** | OER | ✅ VERIFIED | YouTube/Embed | CC BY-NC-SA |

## 2. USER ACTIONS REQUIRED (Project Owner)

To move from "Prototype" to "Production", the following credentials and registrations must be completed:

### A. DIKSHA / Sunbird Integration
- **Website**: [diksha.gov.in](https://diksha.gov.in)
- **Action**: Register as a "Content Consumer" to obtain a `Partner ID` and `API Key`.
- **Why**: Required for high-speed metadata fetching and QR code resource mapping.

### B. NCERT ePathshala Access
- **Website**: [epathshala.nic.in](https://epathshala.nic.in)
- **Action**: No key required, but requires confirmation of "Non-Commercial Use" for deep-linking PDFs.
- **Why**: Ensures legal compliance for displaying textbook content.

### C. Google Gemini (Vertex AI Upgrade)
- **Website**: [console.cloud.google.com](https://console.cloud.google.com)
- **Action**: Current implementation uses Gemini Free Tier. For production stability (higher RPS), upgrade to **Vertex AI** and update `AppConfig.geminiApiKey`.
- **Why**: Avoids "429 Too Many Requests" errors during peak student usage.

### D. Mapbox / OpenStreetMap
- **Website**: [mapbox.com](https://mapbox.com)
- **Action**: Obtain a public token if using Mapbox; otherwise, OSM is free.
- **Why**: Required for Geography interactive maps.

## 3. Production Readiness Statement
Gurukul AI is **100% functional** using only local AI-generated content. External providers are **enrichment only**. Failure to provide the above keys will NOT block the application core.
