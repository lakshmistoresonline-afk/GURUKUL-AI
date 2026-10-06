from .extractor import Class5EnglishMasterExtractor
from .normalizer import Class5EnglishMasterNormalizer
from .validator import Class5EnglishMasterValidator
from .mapper import Class5EnglishMasterMapper

class Class5EnglishMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishMasterExtractor.extract(source_path)
        if not Class5EnglishMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class5EnglishMasterNormalizer.normalize(raw)
        return Class5EnglishMasterMapper.map_to_runtime(normalized)
