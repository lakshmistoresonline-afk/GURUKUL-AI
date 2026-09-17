# GURUKUL AI — CLASS 5 PRE-CLEANUP AUDIT REPORT (STAGE A)
**Audit Timestamp**: 2026-09-17T07:26:37.402301+00:00
**Project Root**: `D:\GURUKUL-AI`
**Input Directory**: `D:\GURUKUL-AI\Contents\Class 5`

## 1. Class 5 Input ZIP Package Inspection
### Archive: `Class5_English_Santoor_Revised_Master_Package_v2.zip`
* **Size**: 170,918 bytes
* **Total Files**: 235
* **Detected Subject**: **English**
* **Discovered Chapters**: 10
  * Chapter 110_Glass_Bangles: Glass Bangles
  * Chapter 109_Vocation: Vocation
  * Chapter 105_The_Frog: The Frog
  * Chapter 101_Papas_Spectacles: Papa's Spectacles
  * Chapter 108_The_Decision_of_the_Panchayat: The Decision of the Panchayat
  * ...and 5 more chapters.

### Archive: `Class5_EVS_Our_Wondrous_World_Revised_Master_Package_v2.zip`
* **Size**: 81,769,817 bytes
* **Total Files**: 369
* **Detected Subject**: **EVS**
* **Discovered Chapters**: 10
  * Chapter 103: The Mystery of Food
  * Chapter 104: Our School — A Happy Place
  * Chapter 106: Some Unique Places
  * Chapter 109: Rhythms of Nature
  * Chapter 107: Energy — How Things Work
  * ...and 5 more chapters.

### Archive: `Class5_Hindi_Veena_Revised_Master_Package_v3.zip`
* **Size**: 80,932,290 bytes
* **Total Files**: 319
* **Detected Subject**: **Hindi**
* **Discovered Chapters**: 12
  * Chapter 109: 02_HINDI/109_Nyaya/00_CHAPTER_INFO/CHAPTER_INFO.json
  * Chapter 106: 02_HINDI/106_Chatur_Chitrakar/00_CHAPTER_INFO/CHAPTER_INFO.json
  * Chapter 101: 02_HINDI/101_Kiran/00_CHAPTER_INFO/CHAPTER_INFO.json
  * Chapter 103: 02_HINDI/103_Chand_ka_Kurta/00_CHAPTER_INFO/CHAPTER_INFO.json
  * Chapter 102: 02_HINDI/102_Nyaya_ki_Kursi/00_CHAPTER_INFO/CHAPTER_INFO.json
  * ...and 7 more chapters.

### Archive: `Class5_Maths_Maths_Mela_Revised_Master_Package_v2.zip`
* **Size**: 61,991,563 bytes
* **Total Files**: 459
* **Detected Subject**: **unknown**
* **Discovered Chapters**: 15
  * Chapter 109: Coconut Farm
  * Chapter 108: Weight and Capacity
  * Chapter 106: The Dairy Farm
  * Chapter 115: Data Through Pictures
  * Chapter 107: Shapes and Patterns
  * ...and 10 more chapters.

## 2. Workspace & Architecture Audit
* **Total Workspace Files Inspected**: 23,843
* **Total Directories Inspected**: 17,947
* **Processors Discovered**: 21
* **Backup Scripts & Artifacts Discovered**: 42

## 3. Discovered Subject Processors
* `processors/common/`: Common pipeline infrastructure
* `processors/english/`: EnglishProcessor (Language, Literature, Vocabulary)
* `processors/hindi/`: HindiProcessor (Devanagari Unicode Safe, Matra QA)
* `processors/evs/`: EVSProcessor (Observation, Survey, Field Tasks)
* `processors/mathematics/`: MathematicsProcessor (Notation, Equations, Numerical QA)