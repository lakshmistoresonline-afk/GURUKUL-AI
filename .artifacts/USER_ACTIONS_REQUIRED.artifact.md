# User Actions Required - External Provider Integration

The following actions are required from the Project Owner to complete Step 12:

## 1. DIKSHA (National Teachers Portal)
- **Task**: Obtain API Credentials for Sunbird/DIKSHA portal.
- **Requirement**: Official partnership or API key for search/ingestion.
- **Status**: Currently using Stubs in `DikshaProvider`.

## 2. NCERT ePathshala
- **Task**: Provide a stable CDN or mirror for Textbook PDFs.
- **Requirement**: Current links in `NcertEpathshalaProvider` are logic-based; need verified file paths.
- **Status**: Functional but needs "Master Download" validation.

## 3. GeoGebra & PhET
- **Task**: Verify Whitelisting of Gurukul AI domain/bundle ID.
- **Requirement**: Ensure HTML5 embeds are allowed without cross-origin restrictions.
- **Status**: Verified in WebView, but needs production testing.

## 4. Firebase Configuration
- **Task**: Update `google-services.json` for all flavors (Dev/Prod).
- **Requirement**: Ensure `com-ncert-projectgurukul-e5e60` has appropriate quotas for high-volume Firestore usage.
