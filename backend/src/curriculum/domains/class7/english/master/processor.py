from .extractor import Class7EnglishMasterExtractor
from .normalizer import Class7EnglishMasterNormalizer
from .validator import Class7EnglishMasterValidator
from .mapper import Class7EnglishMasterMapper

class Class7EnglishMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishMasterExtractor.extract(source_path)
        if not Class7EnglishMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7EnglishMasterNormalizer.normalize(raw)
        return Class7EnglishMasterMapper.map_to_runtime(normalized)
