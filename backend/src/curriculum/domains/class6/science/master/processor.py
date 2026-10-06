from .extractor import Class6ScienceMasterExtractor
from .normalizer import Class6ScienceMasterNormalizer
from .validator import Class6ScienceMasterValidator
from .mapper import Class6ScienceMasterMapper

class Class6ScienceMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceMasterExtractor.extract(source_path)
        if not Class6ScienceMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class6ScienceMasterNormalizer.normalize(raw)
        return Class6ScienceMasterMapper.map_to_runtime(normalized)
