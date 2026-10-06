from .extractor import Class7SocialscienceiiFoundationalExtractor
from .normalizer import Class7SocialscienceiiFoundationalNormalizer
from .validator import Class7SocialscienceiiFoundationalValidator
from .mapper import Class7SocialscienceiiFoundationalMapper

class Class7SocialscienceiiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiFoundationalExtractor.extract(source_path)
        if not Class7SocialscienceiiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7SocialscienceiiFoundationalNormalizer.normalize(raw)
        return Class7SocialscienceiiFoundationalMapper.map_to_runtime(normalized)
