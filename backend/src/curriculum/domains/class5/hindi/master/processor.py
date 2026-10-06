from .extractor import Class5HindiMasterExtractor
from .normalizer import Class5HindiMasterNormalizer
from .validator import Class5HindiMasterValidator
from .mapper import Class5HindiMasterMapper

class Class5HindiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiMasterExtractor.extract(source_path)
        if not Class5HindiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class5HindiMasterNormalizer.normalize(raw)
        return Class5HindiMasterMapper.map_to_runtime(normalized)
