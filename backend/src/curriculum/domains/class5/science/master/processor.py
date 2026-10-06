from .extractor import Class5ScienceMasterExtractor
from .normalizer import Class5ScienceMasterNormalizer
from .validator import Class5ScienceMasterValidator
from .mapper import Class5ScienceMasterMapper

class Class5ScienceMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceMasterExtractor.extract(source_path)
        if not Class5ScienceMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class5ScienceMasterNormalizer.normalize(raw)
        return Class5ScienceMasterMapper.map_to_runtime(normalized)
