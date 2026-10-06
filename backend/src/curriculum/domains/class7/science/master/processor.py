from .extractor import Class7ScienceMasterExtractor
from .normalizer import Class7ScienceMasterNormalizer
from .validator import Class7ScienceMasterValidator
from .mapper import Class7ScienceMasterMapper

class Class7ScienceMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceMasterExtractor.extract(source_path)
        if not Class7ScienceMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7ScienceMasterNormalizer.normalize(raw)
        return Class7ScienceMasterMapper.map_to_runtime(normalized)
