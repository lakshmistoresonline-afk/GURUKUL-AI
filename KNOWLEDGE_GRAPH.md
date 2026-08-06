# Knowledge Graph & AI Schema Design

## 1. Concept Node Structure
Each concept in the Gurukul AI Knowledge Graph is represented as a node with the following attributes:

| Field | Type | Description |
|---|---|---|
| `id` | String (UUID) | Unique identifier for the concept. |
| `subject` | String | e.g., Mathematics, EVS, English. |
| `class` | Int | Target class (5-12). |
| `chapter` | String | Name/ID of the chapter. |
| `topic` | String | Main topic category. |
| `subtopic` | String | Specific sub-topic. |
| `difficulty` | Enum | Beginner, Intermediate, Advanced. |
| `bloom_level` | Enum | Remember, Understand, Apply, Analyze, Evaluate, Create. |
| `exam_weightage`| Int | Estimated importance for examinations (1-10). |
| `est_study_time` | Duration | Estimated time to master (in minutes). |
| `prerequisites` | List<ID> | Concepts that must be learned before this one. |
| `dependencies` | List<ID> | Concepts that depend on this one. |
| `related` | List<ID> | Soft associations with other concepts. |
| `learning_objs` | List<String>| Specific learning goals. |
| `examples` | List<Object> | Practical examples (text/media). |
| `misconceptions` | List<Object> | Common student errors and explanations. |
| `revision_freq` | Interval | Recommended days between revisions. |

## 2. Student Progress (Edge/Mastery)
The relationship between a `Student` and a `Concept` tracks the learning journey:

| Field | Type | Description |
|---|---|---|
| `mastery_score` | Float | 0.0 to 1.0 based on assessments. |
| `learning_status`| Enum | Not Started, In Progress, Mastered, Needs Revision. |
| `last_reviewed` | Timestamp | Date of last interaction. |
| `attempts` | Int | Number of times assessed. |
| `time_spent` | Duration | Cumulative time spent on this concept. |

## 3. AI Module Integration
### AI Tutor (Gemini)
- **Context Injection:** When a student asks a question, the AI Tutor receives the relevant `Concept` metadata and the student's `Mastery Score`.
- **Constraint:** The AI is instructed to stay within the boundaries of the NCERT curriculum and the specific `Learning Objectives`.

### Adaptive Learning Engine
- **Logic:** If `mastery_score` < 0.6, recommend foundational `prerequisites` or alternative `examples`.
- **Spaced Repetition:** Uses `revision_freq` and `last_reviewed` to trigger revision sessions.

### Weakness Detection
- Identifies concepts where `attempts` is high but `mastery_score` remains low.
- Correlates performance across `related` concepts to find underlying gaps.
