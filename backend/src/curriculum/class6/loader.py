import os
from typing import Dict, Any
from ..common.json_reader import JsonReader

class Class6SubjectLoader:
    CONTENTS_ROOT = r"D:\GURUKUL\Contents\Class 6"

    @classmethod
    def load_all_files(cls, subject: str) -> Dict[str, Any]:
        subj_dir = os.path.join(cls.CONTENTS_ROOT, subject)
        files = ["Notes.json", "Master.json", "Flashcards.json", "Mindmaps.json", "Quiz.json", "Overview.json", "Question Papers.json"]
        loaded = {}
        if not os.path.exists(subj_dir):
            return loaded
        for f in files:
            fpath = os.path.join(subj_dir, f)
            data = JsonReader.read_json_file(fpath)
            if data:
                loaded[f] = data
        return loaded
