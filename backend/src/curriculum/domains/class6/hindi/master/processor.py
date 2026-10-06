from .extractor import Class6HindiMasterExtractor
from .normalizer import Class6HindiMasterNormalizer
from .validator import Class6HindiMasterValidator
from .mapper import Class6HindiMasterMapper

class Class6HindiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiMasterExtractor.extract(source_path)
        if not Class6HindiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class6HindiMasterNormalizer.normalize(raw)
        return Class6HindiMasterMapper.map_to_runtime(normalized)
