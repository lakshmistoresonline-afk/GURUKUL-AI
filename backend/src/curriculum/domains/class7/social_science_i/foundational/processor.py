from .extractor import Class7SocialscienceiFoundationalExtractor
from .normalizer import Class7SocialscienceiFoundationalNormalizer
from .validator import Class7SocialscienceiFoundationalValidator
from .mapper import Class7SocialscienceiFoundationalMapper

class Class7SocialscienceiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiFoundationalExtractor.extract(source_path)
        if not Class7SocialscienceiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7SocialscienceiFoundationalNormalizer.normalize(raw)
        return Class7SocialscienceiFoundationalMapper.map_to_runtime(normalized)
