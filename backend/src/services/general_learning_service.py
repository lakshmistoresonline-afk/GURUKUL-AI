import json
import os
import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, time

from ..config.app_config import settings

logger = logging.getLogger(__name__)

class GeneralLearningService:
    def __init__(self, srs_service):
        self.srs_service = srs_service
        self.content: List[Dict[str, Any]] = []
        self.index: Dict[str, Dict[str, Any]] = {} # id -> item
        self.by_class: Dict[str, List[str]] = {} # class_id -> list of ids
        self.by_type: Dict[str, List[str]] = {} # type -> list of ids
        self._load_data()

    def _load_data(self):
        data_path = settings.GENERAL_LEARNING_DATA_PATH
        if not os.path.exists(data_path):
            logger.error(f"General Learning data not found at {data_path}")
            return

        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.content = data.get('content', [])
            from ..utils.path_resolver import PathResolver
            for item in self.content:
                # Normalize classId to class_N
                c_id_raw = item.get('classId')
                c_num = PathResolver.extract_class_id(str(c_id_raw))
                class_key = f"class_{c_num}"
                item['class_key'] = class_key

                # Infer type if missing
                if 'type' not in item:
                    item_id = item.get('id', '')
                    if '_vocab_' in item_id: item['type'] = 'english_vocabulary'
                    elif '_gk_' in item_id: item['type'] = 'general_knowledge'
                    elif '_sci_' in item_id: item['type'] = 'science_facts'
                    elif '_math_' in item_id: item['type'] = 'maths_quick_practice'
                    elif '_geo_' in item_id: item['type'] = 'india_and_world'
                    elif '_life_' in item_id: item['type'] = 'life_skills'
                    elif '_logic_' in item_id: item['type'] = 'logic_and_reasoning'
                    else: item['type'] = 'unknown'

                self.index[item['id']] = item

                if class_key not in self.by_class: self.by_class[class_key] = []
                self.by_class[class_key].append(item['id'])

                i_type = item['type']
                if i_type not in self.by_type: self.by_type[i_type] = []
                self.by_type[i_type].append(item['id'])

            logger.info(f"GeneralLearningService: Loaded {len(self.content)} items.")
        except Exception as e:
            logger.error(f"Error loading General Learning data: {e}")

    async def get_summary(self, student_id: str, class_name: str) -> Dict[str, Any]:
        """Returns a summary of progress for the student's class."""
        # Extract class number
        try:
            c_num = int(class_name.split('_')[1])
        except:
            c_num = 6

        # 1. Get all items available for this class
        class_items = [
            item for item in self.content
            if item.get('class_key') == class_name or c_num in item.get('availableGrades', [])
        ]
        class_item_ids = [item['id'] for item in class_items]

        if not class_item_ids:
            return {"error": "No content for this class"}

        # 2. Get progress from SRS (as a proxy for learned items)
        # Note: Brain Boost might not be SRS eligible, we'd need separate tracking if strict.
        # For now, let's query SRSItems for this user.
        async with self.srs_service.AsyncSession() as session:
            from ..models.srs import SRSItem
            from sqlalchemy import select
            stmt = select(SRSItem.content_id).where(
                SRSItem.student_id == student_id,
                SRSItem.content_id.in_(class_item_ids)
            )
            res = await session.execute(stmt)
            learned_ids = set(res.scalars().all())

        # 3. Categorize
        categories = {
            "english_vocabulary": {"total": 0, "learned": 0},
            "general_knowledge": {"total": 0, "learned": 0},
            "science_facts": {"total": 0, "learned": 0},
            "maths_quick_practice": {"total": 0, "learned": 0},
            "india_and_world": {"total": 0, "learned": 0},
            "life_skills": {"total": 0, "learned": 0},
            "logic_and_reasoning": {"total": 0, "learned": 0}
        }

        for item_id in class_item_ids:
            item = self.index[item_id]
            i_type = item['type']
            if i_type in categories:
                categories[i_type]["total"] += 1
                if item_id in learned_ids:
                    categories[i_type]["learned"] += 1

        return {
            "classId": class_name,
            "categories": categories,
            "overall_progress": round(len(learned_ids) / len(class_item_ids) * 100, 1) if class_item_ids else 0
        }

    async def get_daily_set(self, student_id: str, class_name: str) -> List[Dict[str, Any]]:
        """Generates the 5 Vocab, 3 GK, 1 Brain Boost daily set."""
        # 1. Get due reviews
        due_items = await self.srs_service.get_due_items(student_id, limit=20)
        due_ids = [i['content_id'] for i in due_items if i['content_id'] in self.index]

        # Filter by class
        due_ids = [i for i in due_ids if self.index[i]['class_key'] == class_name]

        # 2. Categorize due items
        due_by_type = {cat: [] for cat in [
            "english_vocabulary", "general_knowledge", "science_facts",
            "maths_quick_practice", "india_and_world", "life_skills", "logic_and_reasoning"
        ]}
        for i_id in due_ids:
            i_type = self.index[i_id]['type']
            if i_type in due_by_type:
                due_by_type[i_type].append(i_id)

        # 3. Fill the quota
        daily_set_ids = []
        quotas = {
            "english_vocabulary": 3,
            "general_knowledge": 2,
            "science_facts": 1,
            "maths_quick_practice": 1,
            "india_and_world": 1,
            "life_skills": 1,
            "logic_and_reasoning": 1
        }

        # Get set of all learned IDs to find new ones
        async with self.srs_service.AsyncSession() as session:
            from ..models.srs import SRSItem
            from sqlalchemy import select
            stmt = select(SRSItem.content_id).where(SRSItem.student_id == student_id)
            res = await session.execute(stmt)
            all_learned = set(res.scalars().all())

        for i_type, quota in quotas.items():
            # Add due items first
            selected = due_by_type[i_type][:quota]
            daily_set_ids.extend(selected)

            remaining = quota - len(selected)
            if remaining > 0:
                # Add new items (not in all_learned)
                class_type_ids = [i for i in self.by_class.get(class_name, []) if self.index[i]['type'] == i_type]
                new_items = [i for i in class_type_ids if i not in all_learned and i not in daily_set_ids]

                if len(new_items) >= remaining:
                    daily_set_ids.extend(random.sample(new_items, remaining))
                else:
                    daily_set_ids.extend(new_items)
                    # If still quota left, just add random learned ones to fill up?
                    # For now, stay with what we have.

        # 4. Return full items
        return [self.index[i_id] for i_id in daily_set_ids]

    def get_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        return self.index.get(content_id)

    def get_all_by_type(self, i_type: str, class_name: str) -> List[Dict[str, Any]]:
        # Extract class number if class_name is class_N
        try:
            c_num = int(class_name.split('_')[1])
        except:
            c_num = 6

        return [
            item for item in self.content
            if item['type'] == i_type and (item.get('class_key') == class_name or c_num in item.get('availableGrades', []))
        ]
