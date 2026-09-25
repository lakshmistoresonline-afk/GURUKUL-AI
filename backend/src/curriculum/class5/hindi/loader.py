import os
from typing import Dict, Any, Optional
from ...common.json_reader import JsonReader

class Class5HindiLoader:
    CONTENTS_DIR = r"D:\GURUKUL\Contents\Class 5\Hindi"

    @classmethod
    def load_all_files(cls) -> Dict[str, Any]:
        files = ["Notes.json", "Master.json", "Hindi Master.json", "Flashcards.json", "Mindmaps.json", "Quiz.json"]
        loaded = {}
        for f in files:
            fpath = os.path.join(cls.CONTENTS_DIR, f)
            data = JsonReader.read_json_file(fpath)
            if data:
                loaded[f] = data
        return loaded
