from .extractor import Class5HindiFoundationalExtractor
from .normalizer import Class5HindiFoundationalNormalizer
from .validator import Class5HindiFoundationalValidator
from .mapper import Class5HindiFoundationalMapper

class Class5HindiFoundationalProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiFoundationalExtractor.extract(source_path)
        if not Class5HindiFoundationalValidator.validate(raw):
            raise ValueError("Validation failed for Foundational")
        normalized = Class5HindiFoundationalNormalizer.normalize(raw)
        return Class5HindiFoundationalMapper.map_to_runtime(normalized)
