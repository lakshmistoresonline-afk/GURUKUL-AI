import os
import json
import logging
import re
import random
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config.app_config import settings
from ..utils.path_resolver import PathResolver
from ..utils.package_adapter import PackageAdapter

logger = logging.getLogger(__name__)

class MasteryService:
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or os.path.join(settings.PROJECT_ROOT, "mastery_data")
        # Dynamic load based on folders or config would be better, but keeping keys for now
        self.mastery_data = {}
        self.chapter_to_subject = {} # (class_name, chapter_id) -> subject

        # 1. Load Master Indexes to discover subjects for chapters
        for c_id in ["5", "6", "7"]:
            class_key = f"class_{c_id}"
            try:
                index = PathResolver._get_master_index(c_id)
                if index:
                    for ch in index.get("chapters", []):
                        cid = ch.get("chapterId")
                        subj = ch.get("subject")
                        if cid and subj:
                            self.chapter_to_subject[(class_key, cid.lower())] = subj.lower()
            except Exception as e:
                logger.error(f"MasteryService: Error loading master index for Class {c_id}: {e}")

        # 2. Load Mastery Data
        if os.path.exists(self.data_path):
            for f in os.listdir(self.data_path):
                if f.endswith("_chapter_mastery_data.json"):
                    # Filename example: class5_chapter_mastery_data.json
                    c_id_raw = f.split('_')[0]
                    c_num = PathResolver.extract_class_id(c_id_raw)
                    if c_num:
                        c_key = f"class_{c_num}"
                        self.mastery_data[c_key] = self._load_json(os.path.join(self.data_path, f))

        self._index_data()

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            logger.error(f"Mastery data file not found: {path}")
            return {"chapters": []}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading mastery data from {path}: {e}")
            return {"chapters": []}

    def _index_data(self):
        """Creates a lookup index for fast access by chapter_id and maps question IDs to concepts."""
        self.index = {} # class -> subject -> key -> chapter
        self.question_to_concept = {} # (class_name, chapter_id, question_id) -> (concept_id, level)

        # Load title map for canonical ID lookups
        title_map_path = os.path.join(settings.STORAGE_PATH, "chapter_title_map.json")
        title_map = {}
        if os.path.exists(title_map_path):
            with open(title_map_path, "r", encoding="utf-8") as f:
                title_map = json.load(f)

        for class_name, data in self.mastery_data.items():
            self.index[class_name] = {}

            # Support both 'mastery' and 'chapters' keys
            chapters = data.get("mastery") or data.get("chapters") or []

            for chapter in chapters:
                chapter_id = str(chapter.get("chapterId", "")).lower()
                if not chapter_id: continue

                # Try to get subject from source, or mapped index, or infer from chapterId
                subj = chapter.get("source", {}).get("subject", "").lower()
                if not subj:
                    subj = self.chapter_to_subject.get((class_name, chapter_id), "general")

                if subj not in self.index[class_name]:
                    self.index[class_name][subj] = {}

                # Slug or Title as key
                slug = chapter.get("source", {}).get("slug")
                title = chapter.get("source", {}).get("chapterTitle")
                chapter_num = str(chapter.get("source", {}).get("chapterNumber"))

                # Resolve canonical Storage ID (e.g. eemm101)
                storage_id = None
                if title and title.lower() in title_map:
                    storage_id = title_map[title.lower()]["id"]

                # We'll use multiple keys for flexibility
                keys = [slug, title, chapter_num, storage_id, chapter_id]
                for k in keys:
                    if not k: continue
                    self.index[class_name][subj][str(k).lower()] = chapter

        # Map questions - use storage_id as the primary key for mappings if available
                map_key = storage_id or chapter_id or slug or title or chapter_num

                # Support both 'concepts' and 'mappings'
                concepts = chapter.get("concepts") or chapter.get("mappings") or []

                for concept in concepts:
                    c_id = concept.get("conceptId") or concept.get("id")
                    if not c_id: continue

                    # Support both 'assessmentEvidence.questionIdsByLevel' and 'questionMap'
                    evidence = {}
                    if "assessmentEvidence" in concept:
                        evidence = concept["assessmentEvidence"].get("questionIdsByLevel", {})
                    elif "questionMap" in concept:
                        evidence = concept["questionMap"]
                    elif "questionIdsByLevel" in concept:
                        evidence = concept["questionIdsByLevel"]

                    for level, q_ids in evidence.items():
                        for q_id in q_ids:
                            self.question_to_concept[(class_name, map_key, q_id)] = (c_id, level.lower())
                            if storage_id: self.question_to_concept[(class_name, storage_id, q_id)] = (c_id, level.lower())
                            if chapter_id: self.question_to_concept[(class_name, chapter_id, q_id)] = (c_id, level.lower())
                            if slug: self.question_to_concept[(class_name, slug, q_id)] = (c_id, level.lower())

    def identify_weak_concepts(self, student_record: Dict[str, Any], concepts: List[Dict[str, Any]]) -> List[str]:
        """Identifies concepts where the student scored below threshold."""
        weak = []
        perf = student_record.get("conceptPerformance", {})
        for c in concepts:
            c_id = c.get("conceptId") or c.get("id") or c.get("concept_id")
            if not c_id: continue
            c_perf = perf.get(c_id, {})
            # If foundation or application is low
            if c_perf.get("foundation", 0) < 0.7 or c_perf.get("application", 0) < 0.6:
                weak.append(c_id)
        return weak

    def get_concept_for_question(self, class_name: str, chapter_id: str, question_id: str) -> Optional[tuple]:
        """Returns (concept_id, level) for a given question."""
        # Normalize chapter ID for lookup
        norm_chapter_id = PathResolver.normalize_chapter_id(class_name, chapter_id)

        # Use provided class_name, no hardcoded fallbacks
        c_id = PathResolver.extract_class_id(class_name)
        class_key = f"class_{c_id}"

        # 1. Direct lookup via indexed mapping
        result = self.question_to_concept.get((class_key, norm_chapter_id, question_id))
        if result:
            return result

        # Fallback to original chapter_id if different
        if norm_chapter_id != chapter_id:
            result = self.question_to_concept.get((class_key, chapter_id, question_id))
            if result: return result

        # 2. Fallback: try mapping via question metadata if ID lookup fails
        config = self.get_chapter_mastery_config(class_name, "", chapter_id)
        if config:
            # Priority 1: Master Package
            master_path = PathResolver.get_chapter_path(class_key, chapter_id)
            pkg_path = os.path.join(master_path, "package.json") if master_path else None

            # Priority 2: storage/output fallback
            if not pkg_path or not os.path.exists(pkg_path):
                subj = config.get("source", {}).get("subject") or self.chapter_to_subject.get((class_key, chapter_id)) or "general"
                pkg_path = os.path.join(settings.STORAGE_PATH, "output", class_key, subj, chapter_id, "package.json")

            if pkg_path and os.path.exists(pkg_path):
                with open(pkg_path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                    bank = pkg.get("original_data", {}).get("assessment", {}).get("expandedQuestionBank", [])
                    if not bank: bank = pkg.get("content", {}).get("quiz", [])
                    if not bank: bank = pkg.get("original_data", {}).get("aiEnrichment", {}).get("question_bank", [])

                    q_meta = next((q for q in bank if str(q.get("id")) == str(question_id)), None)
                    if q_meta:
                        topic = q_meta.get("topic", "").lower()
                        q_text = q_meta.get("question", "").lower()

                        # Try to match topic or question text with concept names
                        concepts = config.get("concepts") or config.get("mappings") or []
                        for concept in concepts:
                            c_id = concept.get("conceptId") or concept.get("id") or concept.get("concept_id")
                            c_name = (concept.get("conceptName") or concept.get("concept") or concept.get("name") or "").lower()
                            if not c_name: continue

                            # Match if concept name is in topic or question text
                            if (topic and c_name in topic) or (c_name in q_text):
                                level = q_meta.get("level", q_meta.get("difficulty", "foundation")).lower()
                                # 'application' is a common level in the new data
                                if q_meta.get("type") == "application":
                                    level = "application"
                                elif q_meta.get("type") == "reasoning":
                                    level = "mastery"

                                return (c_id, level)

        return None

    def get_questions_for_concept(self, class_name: str, subject: str, chapter_id: str, concept_id: str, limit: int = 2, levels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieves actual question objects for a concept from its chapter package."""
        config = self.get_chapter_mastery_config(class_name, subject, chapter_id)
        if not config: return []

        # Fresh Content Integration: If it's an adapted package, search direct by concept_id
        if "content" in config and "quiz" in config["content"]:
            all_qs = config["content"]["quiz"]
            return [q for q in all_qs if str(q.get("concept_id") or q.get("conceptId")) == str(concept_id)][:limit]

        norm_chapter_id = PathResolver.normalize_chapter_id(class_name, chapter_id, subject=subject)

        # Support both 'concepts' and 'mappings'
        concepts = config.get("concepts") or config.get("mappings") or []
        target_concept = next((c for c in concepts if (c.get("conceptId") == concept_id or c.get("id") == concept_id or c.get("concept_id") == concept_id)), None)
        if not target_concept: return []

        q_ids = []
        # Support both 'assessmentEvidence.questionIdsByLevel' and 'questionMap'
        evidence = {}
        if "assessmentEvidence" in target_concept:
            evidence = target_concept["assessmentEvidence"].get("questionIdsByLevel", {})
        elif "questionMap" in target_concept:
            evidence = target_concept["questionMap"]
        elif "questionIdsByLevel" in target_concept:
            evidence = target_concept["questionIdsByLevel"]

        if levels:
            for lvl in levels:
                q_ids.extend(evidence.get(lvl.lower(), []))
        else:
            for level_ids in evidence.values():
                q_ids.extend(level_ids)

        if not q_ids:
            if levels: # Fallback
                for level_ids in evidence.values(): q_ids.extend(level_ids)

        if not q_ids: return []

        # Load the actual question text from the package
        # Priority 1: Master Package
        master_path = PathResolver.get_chapter_path(class_name, norm_chapter_id, subject=subject)
        package_path = os.path.join(master_path, "package.json") if master_path else None

        # Try original chapter_id if different and master_path failed
        if not package_path and norm_chapter_id != chapter_id:
             master_path = PathResolver.get_chapter_path(class_name, chapter_id, subject=subject)
             package_path = os.path.join(master_path, "package.json") if master_path else None

        # Priority 2: storage/output fallback
        if not package_path or not os.path.exists(package_path):
            package_path = os.path.join(settings.STORAGE_PATH, "output", class_name, subject, norm_chapter_id, "package.json")

        if not os.path.exists(package_path) and norm_chapter_id != chapter_id:
            package_path = os.path.join(settings.STORAGE_PATH, "output", class_name, subject, chapter_id, "package.json")

        if not os.path.exists(package_path): return []

        with open(package_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
            bank = pkg.get("original_data", {}).get("assessment", {}).get("expandedQuestionBank", [])
            if not bank: bank = pkg.get("content", {}).get("quiz", [])
            if not bank: bank = pkg.get("original_data", {}).get("aiEnrichment", {}).get("question_bank", [])

            selected_ids = random.sample(q_ids, min(len(q_ids), limit))
            results = [q for q in bank if str(q.get("id")) in [str(sid) for sid in selected_ids]]
            return results

    def get_chapter_mastery_config(self, class_name: str, subject: str, chapter_id: str) -> Optional[Dict[str, Any]]:
        """Finds and enriches the mastery configuration for a specific chapter."""
        c_id = PathResolver.extract_class_id(class_name)
        class_key = f"class_{c_id}"

        norm_chapter_id = PathResolver.normalize_chapter_id(class_name, chapter_id, subject=subject)

        # Priority: Load from the new chapter-specific content root
        master_path = PathResolver.get_chapter_path(class_name, norm_chapter_id, subject=subject)
        if master_path:
            pkg_path = os.path.join(master_path, "package.json")
            if os.path.exists(pkg_path):
                try:
                    with open(pkg_path, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)
                        # Check if it's an adapted package already or needs adaptation
                        if "components" in raw_data:
                            config = PackageAdapter.adapt(raw_data)
                        else:
                            config = raw_data

                        # Ensure every concept has both 'conceptId' and 'conceptName' for UI compatibility
                        # Use concepts_list from adapted package if available
                        concepts = config.get("concepts_list") or config.get("mappings") or config.get("concepts") or []
                        if isinstance(concepts, list):
                            for c in concepts:
                                if isinstance(c, dict):
                                    cid = c.get("concept_id") or c.get("conceptId") or c.get("id")
                                    cname = c.get("concept_name") or c.get("conceptName") or c.get("name") or c.get("label") or "Concept"

                                    c["conceptId"] = cid
                                    c["conceptName"] = cname

                        # For adapted packages, ensure 'concepts' in the root is the list for backend services
                        # while keeping the string version in 'content' for UI
                        if "concepts_list" in config:
                            config["concepts"] = config["concepts_list"]

                        # Ensure 'source' exists for diagnostic/mastery logic
                        if "source" not in config:
                             metadata_path = os.path.join(master_path, "chapter_metadata.json")
                             if os.path.exists(metadata_path):
                                 with open(metadata_path, "r", encoding="utf-8") as fm:
                                     meta = json.load(fm)
                                     config["source"] = {
                                         "slug": meta.get("id") or norm_chapter_id,
                                         "chapterTitle": meta.get("title") or meta.get("chapter_title"),
                                         "subject": meta.get("subject"),
                                         "chapterNumber": meta.get("chapter_number")
                                     }
                             else:
                                 config["source"] = {"slug": norm_chapter_id, "chapterTitle": "Chapter"}

                        return config
                except Exception as e:
                    logger.error(f"Error loading master package for mastery config: {e}", exc_info=True)

            # Fallback to mastery_map.json if package.json missing
            mastery_map_path = os.path.join(master_path, "mastery_map.json")
            metadata_path = os.path.join(master_path, "chapter_metadata.json")
            if os.path.exists(mastery_map_path):
                try:
                    with open(mastery_map_path, "r", encoding="utf-8") as f:
                        config = json.load(f)
                        # Basic mapping for backward compatibility with expected keys
                        if "concepts" not in config:
                            config["concepts"] = []

                        # Add 'source' key for compatibility with DiagnosticService
                        if "source" not in config and os.path.exists(metadata_path):
                            with open(metadata_path, "r", encoding="utf-8") as fm:
                                meta = json.load(fm)
                                config["source"] = {
                                    "slug": meta.get("id") or norm_chapter_id,
                                    "chapterTitle": meta.get("title") or meta.get("chapter_title"),
                                    "subject": meta.get("subject"),
                                    "chapterNumber": meta.get("chapter_number")
                                }
                        elif "source" not in config:
                            config["source"] = {"slug": norm_chapter_id, "chapterTitle": "Chapter"}

                        return config
                except Exception as e:
                    logger.error(f"Error loading mastery_map from {master_path}: {e}")

        # Fallback to legacy index search (if any remains)
        config = None
        if subject:
            subj_key = subject.lower()
            if subj_key in self.index.get(class_key, {}):
                config = self.index[class_key][subj_key].get(norm_chapter_id)
                if not config and norm_chapter_id != chapter_id:
                    config = self.index[class_key][subj_key].get(chapter_id)

        # 2. Global search across all subjects in this class (fallback)
        if not config:
            for subj_dict in self.index.get(class_key, {}).values():
                if norm_chapter_id in subj_dict:
                    config = subj_dict[norm_chapter_id]
                    break
                if norm_chapter_id != chapter_id and chapter_id in subj_dict:
                    config = subj_dict[chapter_id]
                    break

        # 3. Exhaustive search in original data
        if not config:
             # Handle subject mapping from ID prefixes
             id_subject = subject
             if not id_subject:
                  if "mm" in chapter_id or "gp" in chapter_id: id_subject = "mathematics"
                  elif "ev" in chapter_id: id_subject = "evs"
                  elif "sa" in chapter_id: id_subject = "english"
                  elif "hv" in chapter_id: id_subject = "hindi"
                  elif "pr" in chapter_id: id_subject = "english"

             # Extract number from chapter_id
             num_match = re.search(r'(\d+)$', chapter_id)
             search_num = None
             if num_match:
                 full_num = num_match.group(1)
                 try:
                     if len(full_num) >= 3: search_num = int(full_num[-2:])
                     else: search_num = int(full_num)
                 except: pass

             chapters = self.mastery_data.get(class_key, {}).get("mastery") or self.mastery_data.get(class_key, {}).get("chapters") or []
             for c in chapters:
                 src = c.get("source", {})
                 c_chapter_id = str(c.get("chapterId", "")).lower()

                 if id_subject and src.get("subject", "").lower() == id_subject.lower():
                     if search_num is not None and src.get("chapterNumber") == search_num:
                         config = c
                         break

                 if src.get("slug") == norm_chapter_id or src.get("chapterTitle") == norm_chapter_id or \
                    src.get("slug") == chapter_id or src.get("chapterTitle") == chapter_id or \
                    c_chapter_id == norm_chapter_id or c_chapter_id == chapter_id:
                     config = c
                     break

        # Enrichment Phase
        if config:
            # 1. Ensure 'concepts' key exists (mapped from 'mappings')
            if "concepts" not in config:
                config["concepts"] = config.get("mappings") or []

            # Ensure every concept has both 'conceptId' and 'conceptName' for UI compatibility
            for c in config["concepts"]:
                if "concept_id" in c and "conceptId" not in c:
                    c["conceptId"] = c["concept_id"]
                if "concept_name" in c and "conceptName" not in c:
                    c["conceptName"] = c["concept_name"]

            # 2. Try to populate conceptNames from chapter package if missing
            has_missing_names = any(not c.get("conceptName") and not c.get("concept") for c in config["concepts"])
            if has_missing_names:
                master_path = PathResolver.get_chapter_path(class_name, chapter_id, subject=subject)
                if master_path:
                    pkg_path = os.path.join(master_path, "package.json")
                    if os.path.exists(pkg_path):
                        try:
                            with open(pkg_path, "r", encoding="utf-8") as f:
                                pkg = PackageAdapter.adapt(json.load(f))
                                # In adapted pkg, concepts are in original_data.aiEnrichment.concepts
                                topic_guides = pkg.get("original_data", {}).get("aiEnrichment", {}).get("concepts") or []

                                for i, concept in enumerate(config["concepts"]):
                                    if not concept.get("conceptName") and not concept.get("concept"):
                                        # Match by index or Try to find matching guide
                                        if i < len(topic_guides):
                                            guide = topic_guides[i]
                                            name = guide.get("topic") or guide.get("name") or guide.get("conceptName")
                                            if name:
                                                concept["conceptName"] = name

                                        if not concept.get("conceptName"):
                                            # Fallback to ID-based name
                                            cid = concept.get("conceptId", "")
                                            num = cid.split('_')[-1] if '_' in cid else str(i+1)
                                            concept["conceptName"] = f"Concept {num}"
                        except Exception as e:
                            logger.error(f"Enrichment error: {e}")

        return config

    def calculate_mastery_state(self, student_record: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the mastery status and evidence gathered for a chapter.
        """
        if not config:
            return {"status": "NOT_STARTED", "evidence": {}}

        concept_perf = student_record.get("conceptPerformance", {})
        all_concepts = config.get("concepts") or config.get("mappings") or []

        # Evidence requirements
        evidence = {
            "understand": False,
            "apply": False,
            "analyze": False,
            "transfer": False,
            "teach": False
        }

        # Calculate coverage
        completed_concepts = 0
        total_concepts = len(all_concepts)

        for concept in all_concepts:
            c_id = concept.get("conceptId") or concept.get("concept_id") or concept.get("id")
            if not c_id: continue
            perf = concept_perf.get(c_id, {})

            # Check foundation level (Understand)
            foundation_score = perf.get("foundation", 0)
            if foundation_score >= 0.7:
                completed_concepts += 1

        # Calculate progress
        progress = completed_concepts / total_concepts if total_concepts > 0 else 0


        # 1. Determine Evidence-Based Status (Independent of current status)
        has_any_progress = any(
            any(v > 0 for k, v in p.items() if k in ["foundation", "application", "mastery"])
            for p in concept_perf.values()
        )

        if progress == 1.0:
            status = "ASSESSMENT_READY"
        elif progress >= 0.5:
            status = "PRACTICING"
        elif progress > 0 or has_any_progress:
            status = "LEARNING"
        else:
            status = "NOT_STARTED"

        # 2. Check Understand evidence
        if progress >= 0.8:
            evidence["understand"] = True

        # 3. Check Application evidence
        application_scores = [perf.get("application", 0) for perf in concept_perf.values()]
        if application_scores and sum(application_scores) / len(application_scores) >= 0.6:
            evidence["apply"] = True
            if status == "ASSESSMENT_READY":
                status = "ASSESSING"

        # 4. Check Mastery/Analyze
        analyze_scores = [perf.get("mastery", 0) for perf in concept_perf.values()]
        if not analyze_scores: analyze_scores = [perf.get("hots", 0) for perf in concept_perf.values()]
        if analyze_scores and sum(analyze_scores) / len(analyze_scores) >= 0.5:
            evidence["analyze"] = True

        # 5. Check Transfer
        transfer_scores = [perf.get("challenge", 0) for perf in concept_perf.values()]
        if transfer_scores and sum(transfer_scores) / len(transfer_scores) >= 0.5:
            evidence["transfer"] = True

        # 6. Teach (Feynman)
        if student_record.get("feynman_score", 0) >= 70:
            evidence["teach"] = True

        # Check configuration for required advanced levels
        def get_available_levels(c):
            if "assessmentEvidence" in c:
                return c["assessmentEvidence"].get("availableLevels", [])
            elif "levels" in c:
                return [lvl.lower() for lvl in c["levels"]]
            return []

        has_mastery = any("mastery" in get_available_levels(c) or "hots" in get_available_levels(c) or "analyze" in get_available_levels(c) for c in all_concepts)
        has_challenge = any("challenge" in get_available_levels(c) or "transfer" in get_available_levels(c) for c in all_concepts)

        # 7. Final Mastery Gate
        # Distinguish between Provisional and Stable Mastery
        mastery_possible = progress == 1.0 and evidence["apply"] and evidence["teach"]
        if has_mastery: mastery_possible = mastery_possible and evidence["analyze"]
        if has_challenge: mastery_possible = mastery_possible and evidence["transfer"]

        if mastery_possible:
            # Check if it has been verified through retention review
            if student_record.get("retention_verified"):
                status = "MASTERED_STABLE"
            else:
                status = "MASTERED_PROVISIONAL"
        elif status in ["ASSESSING", "ASSESSMENT_READY", "PRACTICING"] and len(self.identify_weak_concepts(student_record, all_concepts)) > 0:
             if student_record.get("attempts", 0) > 1:
                 status = "NEEDS_REMEDIATION"
        elif status == "ASSESSING" and student_record.get("last_quiz_score", 0) < 0.6:
             status = "NEEDS_REMEDIATION"

        # Backward compatibility for "MASTERED"
        if student_record.get("status") == "MASTERED" and status == "MASTERED_PROVISIONAL":
            # If they were already mastered, we'll keep them as mastered_provisional for now
            # unless they already had a retention verified flag
            pass

        # Retention Signal (Additive)
        if status in ["MASTERED_PROVISIONAL", "MASTERED_STABLE"] and student_record.get("retention_at_risk"):
            status = "MASTERED_AT_RISK"

        return {
            "status": status,
            "progress": round(progress, 2),
            "evidence": evidence,
            "remediation_needed": self.identify_weak_concepts(student_record, all_concepts)
        }

    def process_quiz_results(self, student_record: Dict[str, Any], quiz_results: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates concept performance based on quiz results and returns the updated record.
        """
        concept_perf = student_record.get("conceptPerformance", {})
        class_name = student_record.get("className", "class_5")
        chapter_id = student_record.get("chapterId")

        for res in quiz_results:
            q_id = res.get("question_id")
            is_correct = res.get("is_correct")

            mapping = self.get_concept_for_question(class_name, chapter_id, q_id)
            if mapping:
                c_id, level = mapping

                if c_id not in concept_perf:
                    concept_perf[c_id] = {"conceptId": c_id, "foundation": 0, "application": 0, "mastery": 0}

                # Performance update logic: 50/50 weighted average for simplicity
                current_score = concept_perf[c_id].get(level, 0)
                target_score = 1.0 if is_correct else 0.0
                new_score = (current_score * 0.5) + (target_score * 0.5)
                concept_perf[c_id][level] = round(new_score, 2)

        student_record["conceptPerformance"] = concept_perf

        # Calculate overall score for this quiz attempt
        total_q = len(quiz_results)
        correct_q = sum(1 for r in quiz_results if r.get("is_correct"))
        attempt_score = correct_q / total_q if total_q > 0 else 0
        student_record["last_quiz_score"] = attempt_score

        # Calculate new state
        new_state = self.calculate_mastery_state(student_record, config)

        # Update record
        student_record["status"] = new_state["status"]
        student_record["progress"] = new_state["progress"]
        student_record["evidence"] = new_state["evidence"]
        student_record["attempts"] = student_record.get("attempts", 0) + 1

        return {
            "updated_record": student_record,
            "new_state": new_state,
            "weak_concepts": new_state["remediation_needed"]
        }
