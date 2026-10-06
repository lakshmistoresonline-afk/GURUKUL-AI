from .extractor import Class7HindiFoundationalExtractor
from .normalizer import Class7HindiFoundationalNormalizer
from .validator import Class7HindiFoundationalValidator
from .mapper import Class7HindiFoundationalMapper

class Class7HindiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiFoundationalExtractor.extract(source_path)
        if not Class7HindiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class7HindiFoundationalNormalizer.normalize(raw)
        return Class7HindiFoundationalMapper.map_to_runtime(normalized)
