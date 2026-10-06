from .extractor import Class6EnglishMasterExtractor
from .normalizer import Class6EnglishMasterNormalizer
from .validator import Class6EnglishMasterValidator
from .mapper import Class6EnglishMasterMapper

class Class6EnglishMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishMasterExtractor.extract(source_path)
        if not Class6EnglishMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class6EnglishMasterNormalizer.normalize(raw)
        return Class6EnglishMasterMapper.map_to_runtime(normalized)
