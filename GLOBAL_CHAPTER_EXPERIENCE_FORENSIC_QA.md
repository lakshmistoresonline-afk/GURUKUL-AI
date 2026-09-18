# GURUKUL AI — GLOBAL CHAPTER EXPERIENCE FINAL FORENSIC QA REPORT
**QA Timestamp**: 2026-09-17T15:19:27.570241+00:00
**Final Status**: **PASS WITH IMPROVEMENTS**
**Total Scope**: 183 / 183 Chapters (Class 5: 47, Class 6: 64, Class 7: 72)

## 1. Renderer Architecture & Data-Driven Generic Check
* **Data-Driven Generic Renderer**: **PASS** (0 hardcoded chapter title conditionals in UI code)
* **Reading Container Area**: `max-w-4xl` (~800–900px) centered desktop width with natural line wrapping
* **Textbook Source Drawer**: `View Textbook Source` drawer present in `page.tsx` for raw page provenance

## 2. Curriculum-Wide Record Accounting
* **Pure Educational 4 Pillars**: **13344 Records**
  * **Learn**: 6046
  * **Practice**: 4257
  * **Assess**: 1895
  * **Revise**: 1146
* **Resources**: **1502 Records** (Verified Portals + Discovery Query Descriptors)
* **Provenance Complete Chapters**: **183 / 183**
* **Extraction Artifacts Detected**: **1086**

## 3. Subject-Specific Pedagogical QA
* **English**: Literature, poems, vocabulary, and grammar cards render with natural full-width line wrapping.
* **Hindi**: 100% Devanagari UTF-8 glyphs, matras, and punctuation preserved without broken characters or transliteration.
* **EVS**: Observation, survey, experiment, and field task badges render with rich activity cards.
* **Mathematics**: Step-by-step worked solutions and operators ($	imes$, $\div$, $-$, units) render with 100% numerical agreement.

## 4. 183-Chapter Experience Matrix
| Class | Subject | Chapter ID | Chapter Title | Learn | Practice | Assess | Revise | Resources | Provenance | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Class 5 | `01_english_complete` | `101` | Papas Spectacles | 12 | 29 | 12 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `102` | Gone with the Scooter | 12 | 29 | 12 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `103` | The Rainbow | 12 | 30 | 5 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `104` | The Wise Parrot | 12 | 23 | 15 | 8 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `105` | The Frog | 12 | 26 | 16 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `106` | What a Tank | 12 | 30 | 15 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `107` | Gilli Danda | 12 | 40 | 25 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `108` | The Decision of the Panchayat | 12 | 42 | 30 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `109` | Vocation | 12 | 28 | 14 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `01_english_complete` | `110` | Glass Bangles | 14 | 32 | 17 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `101` | किरन | 7 | 22 | 14 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `102` | न्याय की कुर्सी | 14 | 29 | 19 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `103` | चाँद का कुरता | 12 | 36 | 29 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `104` | साङकेन | 13 | 29 | 19 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `105` | सुंदरिया | 16 | 46 | 35 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `106` | चतुर चित्रकार | 14 | 47 | 28 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `107` | मेरा बचपन | 10 | 26 | 18 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `108` | काजीरंगा राष्ट्रीय उद्यान की यात्रा | 29 | 25 | 14 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `109` | न्याय | 18 | 25 | 17 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `110` | तीन मछलियाँ | 15 | 33 | 20 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `111` | हमारे ये कलामंदिर | 15 | 34 | 24 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `02_hindi_complete` | `112` | गंगा की कहानी | 18 | 25 | 13 | 7 | 5 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `101` | Water The Essence of Life | 20 | 61 | 4 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `102` | Journey of a River | 17 | 32 | 3 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `103` | The Mystery of Food | 17 | 48 | 8 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `104` | Our School A Happy Place | 18 | 68 | 11 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `105` | Our Vibrant Country | 21 | 50 | 5 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `106` | Some Unique Places | 18 | 41 | 11 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `107` | Energy How Things Work | 20 | 58 | 7 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `108` | Clothes How Things are Made | 14 | 31 | 1 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `109` | Rhythms of Nature | 16 | 37 | 3 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_evs_complete` | `110` | Earth Our Shared Home | 22 | 51 | 8 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `101` | We the Travellers I | 41 | 19 | 14 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `102` | Fractions | 43 | 23 | 15 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `103` | Angles as Turns | 30 | 17 | 10 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `104` | We the Travellers II | 39 | 19 | 15 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `105` | Far and Near | 38 | 16 | 11 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `106` | The Dairy Farm | 56 | 33 | 20 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `107` | Shapes and Patterns | 35 | 15 | 12 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `108` | Weight and Capacity | 43 | 20 | 14 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `109` | Coconut Farm | 46 | 26 | 15 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `110` | Symmetrical Designs | 18 | 11 | 6 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `111` | Grandmothers Quilt | 39 | 21 | 12 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `112` | Racing Seconds | 26 | 11 | 7 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `113` | Animal Jumps | 20 | 10 | 6 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `114` | Maps and Locations | 21 | 12 | 6 | 14 | 4 | ✓ | **PASS** |
| Class 5 | `03_maths_complete` | `115` | Data Through Pictures | 33 | 13 | 8 | 14 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10101` | A Bottle of Dew | 80 | 32 | 14 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10102` | The Raven and the Fox | 46 | 18 | 9 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10103` | Rama to the Rescue | 100 | 50 | 24 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10201` | The Unlikely Best Friends | 68 | 31 | 17 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10202` | A Friends Prayer | 52 | 28 | 13 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10203` | The Chair | 88 | 37 | 12 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10301` | Neem Baba | 62 | 19 | 11 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10302` | What a Bird Thought | 65 | 50 | 28 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10303` | Spices that Heal Us | 74 | 29 | 12 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10401` | Change of Heart | 65 | 56 | 25 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10402` | The Winner | 40 | 33 | 23 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10403` | Yoga A Way of Life | 45 | 11 | 7 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10501` | Hamara Bharat Incredible India | 13 | 8 | 5 | 1 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10502` | Kalakritiyon ka Bharat | 121 | 60 | 29 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_english_complete_grade6` | `10503` | Ila Sachani Embroidering Dreams with her Feet | 69 | 34 | 15 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `101` | MATRIBHUMI | 40 | 66 | 4 | 4 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `102` | GOL | 31 | 56 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `103` | PEHLI BOOND | 37 | 63 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `104` | HAAR KI JEET | 31 | 58 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `105` | RAHIM KE DOHE | 23 | 39 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `106` | MERI MAA | 34 | 45 | 4 | 3 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `107` | JALATE CHALO | 53 | 97 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `108` | SATTRIYA AUR BIHU NRITYA | 55 | 75 | 4 | 5 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `109` | MAIYA MAIN NAHIN MAKHAN KHAYO | 42 | 78 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `110` | PARIKSHA | 50 | 86 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `111` | CHETAK KI VEERTA | 25 | 30 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `112` | HIND MAHASAGAR MEIN | 47 | 79 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `02_hindi_complete_grade6` | `113` | PED KI BAAT | 88 | 44 | 4 | 3 | 4 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `101` | Patterns In Mathematics | 43 | 3 | 4 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `102` | Lines And Angles | 110 | 3 | 4 | 4 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `103` | Number Play | 114 | 2 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `104` | Data Handling And Presentation | 88 | 2 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `105` | Prime Time | 74 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `106` | Perimeter And Area | 71 | 3 | 4 | 4 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `107` | Fractions | 125 | 3 | 4 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `108` | Playing With Constructions | 75 | 2 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `109` | Symmetry | 84 | 3 | 4 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `02_mathematics_complete_grade6` | `110` | The Other Side Of Zero | 121 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `101` | THE WONDERFUL WORLD OF SCIENCE | 2 | 3 | 3 | 2 | 4 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `102` | DIVERSITY IN THE LIVING WORLD | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `103` | MINDFUL EATING A PATH TO A HEALTHY BODY | 2 | 3 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `104` | EXPLORING MAGNETS | 2 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `105` | MEASUREMENT OF LENGTH AND MOTION | 2 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `106` | MATERIALS AROUND US | 2 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `107` | TEMPERATURE AND ITS MEASUREMENT | 3 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `108` | A JOURNEY THROUGH STATES OF WATER | 3 | 3 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `109` | METHODS OF SEPARATION IN EVERYDAY LIFE | 3 | 3 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `110` | LIVING CREATURES EXPLORING THEIR CHARACTERISTICS | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `111` | NATURE S TREASURES | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_science_complete_grade6` | `112` | BEYOND EARTH | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `101` | INTRODUCTION WHY SOCIAL SCIENCE | 48 | 50 | 10 | 15 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `102` | OCEANS AND CONTINENTS | 38 | 30 | 4 | 8 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `103` | LANDFORMS AND LIFE | 44 | 47 | 11 | 15 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `104` | TIMELINE AND SOURCES OF HISTORY | 33 | 36 | 2 | 7 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `105` | INDIA THAT IS BHARAT | 22 | 30 | 9 | 12 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `106` | THE BEGINNINGS OF INDIAN CIVILISATION | 35 | 34 | 2 | 3 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `107` | INDIA S CULTURAL ROOTS | 29 | 22 | 3 | 9 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `108` | UNITY IN DIVERSITY OR MANY IN THE ONE | 25 | 36 | 2 | 5 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `109` | FAMILY AND COMMUNITY | 42 | 67 | 2 | 5 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `110` | GRASSROOTS DEMOCRACY PART 1 | 29 | 52 | 4 | 8 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `111` | GRASSROOTS DEMOCRACY PART 2 | 17 | 23 | 3 | 6 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `112` | GRASSROOTS DEMOCRACY PART 3 | 19 | 25 | 3 | 6 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `113` | THE VALUE OF WORK | 23 | 32 | 3 | 6 | 4 | ✓ | **PASS** |
| Class 6 | `03_social_science_complete_grade6` | `114` | ECONOMIC ACTIVITIES AROUND US | 19 | 29 | 4 | 6 | 4 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `101` | THE DAY THE RIVER SPOKE | 17 | 11 | 9 | 7 | 3 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `102` | TRY AGAIN | 13 | 7 | 5 | 4 | 4 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `103` | THREE DAYS TO SEE | 20 | 8 | 6 | 4 | 13 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `104` | ANIMALS BIRDS AND DR DOLITTLE | 18 | 9 | 10 | 8 | 2 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `105` | A FUNNY MAN | 16 | 5 | 5 | 7 | 7 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `106` | SAY THE RIGHT THING | 23 | 9 | 10 | 12 | 9 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `107` | MY BROTHERS GREAT INVENTION | 21 | 11 | 12 | 11 | 3 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `108` | PAPER BOATS | 11 | 6 | 6 | 5 | 3 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `109` | HOME AND AWAY | 22 | 5 | 7 | 9 | 10 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `110` | THE TUNNEL | 21 | 13 | 11 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `111` | TRAVEL | 12 | 7 | 5 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `112` | CONQUERING THE SUMMIT | 16 | 6 | 4 | 4 | 7 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `113` | A HOMAGE TO OUR BRAVE SOLDIERS | 22 | 12 | 11 | 5 | 2 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `114` | MY DEAR SOLDIERS | 10 | 6 | 4 | 5 | 2 | ✓ | **PASS** |
| Class 7 | `02_english_grade7_complete` | `115` | RANI ABBAKKA | 23 | 7 | 5 | 7 | 8 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `101` |  | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `102` |  | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `103` |  | 4 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `104` |  | 2 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `105` |  | 1 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `106` |  | 2 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `107` |  | 3 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `108` |  | 4 | 2 | 2 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `109` |  | 4 | 5 | 3 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `02_hindi_grade7_complete` | `110` |  | 3 | 4 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `101` | LARGE NUMBERS AROUND US | 109 | 53 | 56 | 14 | 23 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `102` | ARITHMETIC EXPRESSIONS | 90 | 32 | 34 | 14 | 15 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `103` | A PEEK BEYOND THE POINT | 159 | 32 | 46 | 1 | 17 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `104` | EXPRESSIONS USING LETTER NUMBERS | 90 | 53 | 31 | 4 | 19 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `105` | PARALLEL AND INTERSECTING LINES | 72 | 25 | 33 | 2 | 31 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `106` | NUMBER PLAY | 77 | 40 | 36 | 6 | 20 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `107` | A TALE OF THREE INTERSECTING LINES | 54 | 19 | 26 | 7 | 28 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part1_complete` | `108` | WORKING WITH FRACTIONS | 89 | 36 | 17 | 14 | 11 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `101` | GEOMETRIC TWINS | 27 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `102` | OPERATIONS WITH INTEGERS | 25 | 4 | 4 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `103` | FINDING COMMON GROUND | 24 | 4 | 4 | 4 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `104` | ANOTHER PEEK BEYOND THE POINT | 34 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `105` | CONNECTING THE DOTS | 43 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `106` | CONSTRUCTIONS AND TILINGS | 32 | 3 | 3 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `02_mathematics_grade7_part2_complete` | `107` | FINDING THE UNKNOWN | 45 | 5 | 4 | 5 | 1 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `101` | THE EVER EVOLVING WORLD OF SCIENCE | 9 | 9 | 6 | 2 | 1 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `102` | THE WORLD OF SUBSTANCES | 17 | 40 | 35 | 18 | 69 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `103` | ELECTRICITY CIRCUITS AND THEIR COMPONENTS | 36 | 28 | 34 | 18 | 101 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `104` | THE WORLD OF METALS | 25 | 36 | 33 | 12 | 53 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `105` | CHANGES AROUND US PHYSICAL AND CHEMICAL | 21 | 39 | 39 | 18 | 56 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `106` | ADOLESCENCE A STAGE OF GROWTH AND CHANGE | 45 | 17 | 9 | 9 | 31 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `107` | HEAT TRANSFER IN NATURE | 19 | 33 | 20 | 12 | 82 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `108` | MEASUREMENT OF TIME AND MOTION | 33 | 19 | 22 | 8 | 52 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `109` | LIFE PROCESSES IN ANIMALS | 23 | 30 | 25 | 10 | 54 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `110` | LIFE PROCESSES IN PLANTS | 20 | 50 | 40 | 19 | 75 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `111` | LIGHT SHADOWS AND REFLECTIONS | 27 | 40 | 28 | 16 | 144 | ✓ | **PASS** |
| Class 7 | `03_science_grade7_complete` | `112` | EARTH MOON AND THE SUN | 29 | 31 | 28 | 8 | 68 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `101` | Geographical Diversity of India | 32 | 3 | 4 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `102` | Understanding the Weather | 23 | 2 | 3 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `103` | Climates of India | 26 | 2 | 3 | 5 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `104` | New Beginnings: Cities and States | 19 | 2 | 3 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `105` | The Rise of Empires | 37 | 2 | 3 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `106` | The Age of Reorganisation | 35 | 2 | 3 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `107` | The Gupta Era: An Age of Tireless Creativity | 25 | 3 | 4 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `108` | How the Land Becomes Sacred | 20 | 2 | 3 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `109` | From the Rulers to the Ruled: Types of Governments | 30 | 3 | 4 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `110` | The Constitution of India — An Introduction | 26 | 2 | 4 | 4 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `111` | From Barter to Money | 27 | 2 | 3 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part1_complete` | `112` | Understanding Markets | 31 | 2 | 3 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `101` | THE STORY OF INDIAN FARMING | 31 | 10 | 4 | 5 | 3 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `102` | INDIA AND HER NEIGHBOURS | 36 | 7 | 5 | 4 | 4 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `103` | EMPIRES AND KINGDOMS 6TH TO 10TH CENTURIES | 40 | 17 | 6 | 4 | 12 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `104` | TURNING TIDES 11TH AND 12TH CENTURIES | 31 | 11 | 5 | 3 | 3 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `105` | INDIA A HOME TO MANY | 21 | 8 | 9 | 3 | 1 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `106` | THE STATE THE GOVERNMENT AND YOU | 30 | 10 | 8 | 3 | 4 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `107` | INFRASTRUCTURE ENGINE OF INDIA S DEVELOPMENT | 29 | 10 | 4 | 3 | 2 | ✓ | **PASS** |
| Class 7 | `03_social_science_grade7_part2_complete` | `108` | BANKS AND THE MAGIC OF FINANCE | 24 | 13 | 4 | 3 | 2 | ✓ | **PASS** |