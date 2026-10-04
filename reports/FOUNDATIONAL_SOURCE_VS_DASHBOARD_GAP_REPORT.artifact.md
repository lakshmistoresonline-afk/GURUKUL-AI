# GURUKUL AI — FOUNDATIONAL SOURCE VS. DASHBOARD GAP ANALYSIS REPORT

This report provides a strict, gap-by-gap audit comparing the raw data present in `Foundational.json` and `Notes.json` against what is currently surfaced in the dashboard UI.

---

## Gap Analysis Matrix

| Source JSON Key / Path | Present in Source? | Rendered in Dashboard UI? | Identified Gap / Missing Detail |
| :--- | :--- | :--- | :--- |
| **`content.idioms_expressions`** | Yes | Partially (shows title & source context) | Specific figurative definitions, breakdown of idiomatic nuance, and contextual usage sentences from source are omitted from card view. |
| **`content.synonyms` / `antonyms`** | Yes (in vocabulary/glossary) | Partially (shows term & definition) | Explicit synonym pairs and antonym pairs (e.g., `synonym: "Peeked"`, `antonym: "Stared"`) are not rendered as distinct interactive tags on vocabulary cards. |
| **`content.word_forms`** | Yes | Basic card rendering | Morphological variations (noun, verb, adjective, adverb forms) lack dedicated tabular or structured display formatting. |
| **`content.sentence_structure`** | Yes | Basic card rendering | Syntactic breakdown and structural patterns lack deep linguistic annotations. |

---

## Conclusion & Recommendation
While the dashboard successfully renders the foundational module headers, concepts, rules, and examples, incorporating explicit **Synonym / Antonym pills**, **Word Form derivation trees**, and **Idiomatic Meaning breakdowns** will ensure 100% data fidelity without missing a single word.
