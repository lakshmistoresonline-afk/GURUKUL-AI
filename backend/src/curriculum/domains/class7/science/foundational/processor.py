from .extractor import Class7ScienceFoundationalExtractor
from .normalizer import Class7ScienceFoundationalNormalizer
from .validator import Class7ScienceFoundationalValidator
from .mapper import Class7ScienceFoundationalMapper

class Class7ScienceFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceFoundationalExtractor.extract(source_path)
        if not Class7ScienceFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7ScienceFoundationalNormalizer.normalize(raw)
        return Class7ScienceFoundationalMapper.map_to_runtime(normalized)
