# User Actions Required: Content Acquisition Checklist

The automated acquisition of external content has failed because these providers do not offer open, authenticated APIs for mass programmatic download. **Manual project owner intervention is REQUIRED.**

## 1. Manual Resource Procurement

| Resource | Source | Destination in `/content_repository/` |
| :--- | :--- | :--- |
| **Class 5/6 PDFs** | [NCERT ePathshala](https://ncert.nic.in/textbook.php) | `/curriculum/class_XX/subject/textbook/` |
| **Explainer Videos** | [DIKSHA](https://diksha.gov.in/) | `/multimedia/videos/mp4/` |
| **Math Simulations** | [GeoGebra](https://www.geogebra.org/) | `/multimedia/simulations/geogebra/` |
| **Science Sims** | [PhET](https://phet.colorado.edu/) | `/multimedia/simulations/phet/` |

## 2. Technical Credentials Needed
If you wish to re-enable automated DIKSHA searching, the Project Owner must:
1.  **Register as a DIKSHA Partner** to obtain an API Key.
2.  **Provide the API Key** to the developers for integration into `AppConfig`.
3.  **Accept the OER License** terms for third-party content.

## 3. Immediate Next Steps
1.  **Download 1 PDF** (e.g., Class 5 Math Chapter 1).
2.  **Save it as `m5_c1_textbook.pdf`** in `/curriculum/class_05/mathematics/textbook/`.
3.  **Run the "Import Wizard"** in the Gurukul AI Content Studio to parse this file.
4.  **Confirm Storage** in the repository.

Without these manual actions, the AI Content Factory is generating lessons based on *general knowledge* of the topics, not the *exact content* of the NCERT textbooks.
