# Known Issues & Technical Debt

## Technical Debt
1. **QuML Player:** The current assessment engine uses a simplified model. Full QuML 3.0 schema support needs a dedicated parser.
2. **Neo4j Integration:** The knowledge graph is currently simulated in Firestore. For Classes 7-12, a dedicated Graph DB is recommended for complex relationship queries.
3. **Voice Tutor:** Voice-to-text integration is prototyped but needs fine-tuning for different Indian accents.
4. **Project Structure:** The repository uses a non-standard `app/` directory instead of the standard Flutter `android/` directory.
5. **Build CLI:** The `flutter` command-line tool is currently unavailable in the environment, preventing full Quality Gate verification.
6. **Assessment Session Expiry:** Incomplete sessions in `LocalStorageService` do not currently have a TTL (Time-To-Live).
7. **AI Hint Limits:** There is no rate-limiting or penalty for requesting excessive AI hints during assessments.

## Known Issues
- **Offline Sync:** If multiple devices edit the same user profile simultaneously, the last-write-wins policy applies in Firestore.
- **AI Latency:** Gemini API response times can vary depending on network conditions and free-tier traffic.
- **H5P Support:** Full interactive H5P packages require a webview-based player which is partially implemented.
