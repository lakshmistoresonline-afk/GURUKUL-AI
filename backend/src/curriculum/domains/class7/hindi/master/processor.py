from .extractor import Class7HindiMasterExtractor
from .normalizer import Class7HindiMasterNormalizer
from .validator import Class7HindiMasterValidator
from .mapper import Class7HindiMasterMapper

class Class7HindiMasterProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiMasterExtractor.extract(source_path)
        if not Class7HindiMasterValidator.validate(raw):
            raise ValueError("Validation failed for Master")
        normalized = Class7HindiMasterNormalizer.normalize(raw)
        return Class7HindiMasterMapper.map_to_runtime(normalized)
